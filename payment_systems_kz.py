#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Платежные системы для Казахстана - заглушки и интеграции
"""

from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, Optional
import uuid

class PaymentProvider(ABC):
    """Абстрактный провайдер платежей"""
    
    @abstractmethod
    def create_payment(self, amount: float, description: str, order_id: str) -> Dict:
        pass
    
    @abstractmethod
    def check_payment_status(self, payment_id: str) -> Dict:
        pass

class PaymentStub(PaymentProvider):
    """Заглушка для тестирования платежей"""
    
    def __init__(self):
        self.payments = {}
    
    def create_payment(self, amount: float, description: str, order_id: str) -> Dict:
        payment_id = str(uuid.uuid4())[:8]
        
        payment_data = {
            'payment_id': payment_id,
            'amount': amount,
            'currency': 'KZT',
            'description': description,
            'order_id': order_id,
            'status': 'pending',
            'payment_url': f"https://test-payment.kz/pay/{payment_id}",
            'created_at': datetime.now().isoformat()
        }
        
        self.payments[payment_id] = payment_data
        return payment_data
    
    def check_payment_status(self, payment_id: str) -> Dict:
        if payment_id in self.payments:
            # Имитируем случайный успех оплаты
            import random
            if random.choice([True, False]):
                self.payments[payment_id]['status'] = 'paid'
                self.payments[payment_id]['paid_at'] = datetime.now().isoformat()
            
            return self.payments[payment_id]
        
        return {'error': 'Payment not found'}
    
    def simulate_payment_success(self, payment_id: str):
        """Ручная имитация успешной оплаты"""
        if payment_id in self.payments:
            self.payments[payment_id]['status'] = 'paid'
            self.payments[payment_id]['paid_at'] = datetime.now().isoformat()

class KaspiPayStub(PaymentProvider):
    """Заглушка для Kaspi Pay (популярно в Казахстане)"""
    
    def create_payment(self, amount: float, description: str, order_id: str) -> Dict:
        return {
            'payment_id': f"kaspi_{uuid.uuid4().hex[:8]}",
            'amount': amount,
            'currency': 'KZT', 
            'qr_code': f"kaspi://pay?amount={amount}&merchant=test",
            'payment_url': f"https://kaspi.kz/pay?id={order_id}",
            'status': 'pending'
        }
    
    def check_payment_status(self, payment_id: str) -> Dict:
        return {'status': 'paid', 'method': 'kaspi_pay'}

class BankCenterCreditStub(PaymentProvider):
    """Заглушка для БанкЦентрКредит"""
    
    def __init__(self, merchant_id: str = "test_merchant"):
        self.merchant_id = merchant_id
        self.secret_key = "test_secret_key"
    
    def create_payment(self, amount: float, description: str, order_id: str) -> Dict:
        """Создает платеж в стиле казахстанского банка"""
        payment_data = {
            'payment_id': f"bcc_{uuid.uuid4().hex[:12]}",
            'merchant_id': self.merchant_id,
            'amount': int(amount * 100),  # в тиынах
            'currency': 'KZT',
            'description': description,
            'order_id': order_id,
            'payment_url': f"https://ecommerce.bcc.kz/payment?id={order_id}",
            'status': 'created',
            'methods': ['card', 'kaspi', 'qr_code'],
            'created_at': datetime.now().isoformat()
        }
        
        return payment_data
    
    def check_payment_status(self, payment_id: str) -> Dict:
        return {
            'payment_id': payment_id,
            'status': 'success',  # success, pending, failed
            'amount': 5000,
            'currency': 'KZT',
            'payment_method': 'card',
            'transaction_id': f"txn_{uuid.uuid4().hex[:8]}"
        }

# === УПРАВЛЕНИЕ ПЛАТЕЖАМИ В БОТЕ ===

class BotPaymentManager:
    """Менеджер платежей для бота"""
    
    def __init__(self, provider: PaymentProvider):
        self.provider = provider
        self.pending_payments = {}
    
    def create_test_package_payment(self, package_type: str, company_name: str, contact_info: str) -> Dict:
        """Создает платеж за пакет тестирований"""
        
        packages = {
            'basic': {'tests': 10, 'price': 15000, 'name': 'Базовый'},
            'standard': {'tests': 50, 'price': 60000, 'name': 'Стандартный'}, 
            'premium': {'tests': 100, 'price': 100000, 'name': 'Премиум'}
        }
        
        if package_type not in packages:
            return {'error': 'Неизвестный тип пакета'}
        
        package = packages[package_type]
        order_id = f"order_{uuid.uuid4().hex[:8]}"
        
        description = f"Пакет тестирований '{package['name']}' для {company_name}"
        
        payment = self.provider.create_payment(
            amount=package['price'],
            description=description,
            order_id=order_id
        )
        
        # Сохраняем информацию о заказе
        self.pending_payments[order_id] = {
            'company_name': company_name,
            'contact_info': contact_info,
            'package_type': package_type,
            'tests_count': package['tests'],
            'payment_data': payment
        }
        
        return {
            'order_id': order_id,
            'payment_url': payment['payment_url'],
            'amount': package['price'],
            'currency': 'KZT',
            'tests_count': package['tests']
        }
    
    def check_and_activate_package(self, order_id: str) -> Optional[Dict]:
        """Проверяет оплату и активирует пакет"""
        if order_id not in self.pending_payments:
            return None
        
        order_data = self.pending_payments[order_id]
        payment_id = order_data['payment_data']['payment_id']
        
        status = self.provider.check_payment_status(payment_id)
        
        if status.get('status') in ['paid', 'success']:
            # Активируем пакет тестирований
            from password_management import SimplePasswordManager
            
            pm = SimplePasswordManager()
            password = pm.generate_company_password(
                order_data['company_name'], 
                order_data['tests_count']
            )
            
            # Удаляем из ожидающих
            del self.pending_payments[order_id]
            
            return {
                'activated': True,
                'company_name': order_data['company_name'],
                'password': password,
                'tests_count': order_data['tests_count'],
                'payment_info': status
            }
        
        return {'activated': False, 'status': status.get('status', 'pending')}

# === ИНТЕГРАЦИЯ С БОТОМ ===

async def handle_payment_flow(bot, message, payment_manager: BotPaymentManager):
    """Обработка потока оплаты в боте"""
    
    # 1. Выбор пакета
    keyboard = [
        ["💰 Базовый - 10 тестов (15,000 ₸)"],
        ["💎 Стандартный - 50 тестов (60,000 ₸)"],
        ["🏆 Премиум - 100 тестов (100,000 ₸)"]
    ]
    await message.reply("Выберите пакет тестирований:", reply_markup=keyboard)
    
    # 2. Создание платежа (после выбора пакета)
    payment_info = payment_manager.create_test_package_payment(
        package_type='standard',
        company_name='ТОО Тест',
        contact_info='+7 123 456 7890'
    )
    
    # 3. Отправка ссылки на оплату
    await message.reply(
        f"💳 Оплата пакета 'Стандартный'\n\n"
        f"💰 Сумма: {payment_info['amount']:,} ₸\n"
        f"📊 Количество тестов: {payment_info['tests_count']}\n\n"
        f"🔗 Ссылка для оплаты: {payment_info['payment_url']}\n\n"
        f"После оплаты нажмите /check_payment_{payment_info['order_id']}"
    )

# === ВОПРОСЫ ДЛЯ БАНКА ===

BANK_QUESTIONS = """
🏦 Вопросы для БанкЦентрКредит:

1. 💳 ПЛАТЕЖНЫЕ МЕТОДЫ:
   - Поддерживаете ли интернет-эквайринг?
   - Kaspi Pay интеграция есть?
   - QR-код платежи доступны?
   - Комиссия за транзакции?

2. 🔌 ТЕХНИЧЕСКАЯ ИНТЕГРАЦИЯ:
   - REST API для платежей?
   - Тестовая среда (sandbox)?
   - Документация для разработчиков?
   - Webhook уведомления?

3. 📋 ДОКУМЕНТЫ И ПРОЦЕСС:
   - Требования к регистрации бизнеса?
   - Сроки подключения эквайринга?
   - Минимальные обороты?
   - Техподдержка для интеграции?

4. 💰 ТАРИФЫ:
   - Абонентская плата?
   - Процент с транзакции?
   - Лимиты на сумму платежа?
   - Время зачисления средств?
"""

if __name__ == "__main__":
    print("=== ДЕМО ПЛАТЕЖНОЙ СИСТЕМЫ ===")
    
    # Тестируем заглушку
    payment_stub = PaymentStub()
    bot_payment = BotPaymentManager(payment_stub)
    
    # Создаем платеж
    payment_info = bot_payment.create_test_package_payment(
        'standard', 
        'ТОО Тест Компания',
        '+7 123 456 7890'
    )
    
    print(f"Создан платеж: {payment_info}")
    
    # Имитируем успешную оплату
    order_id = payment_info['order_id']
    payment_stub.simulate_payment_success(
        bot_payment.pending_payments[order_id]['payment_data']['payment_id']
    )
    
    # Проверяем и активируем
    result = bot_payment.check_and_activate_package(order_id)
    print(f"Результат активации: {result}")
    
    print("\n" + BANK_QUESTIONS)