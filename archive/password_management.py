#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Простая система управления паролями для тестирования
Эволюция от простого к сложному
"""

from datetime import datetime, timedelta
from typing import Dict, List, Optional
import json
import os

class SimplePasswordManager:
    """Простая система паролей для старта"""
    
    def __init__(self, data_file: str = "passwords.json"):
        self.data_file = data_file
        self.passwords: Dict[str, dict] = self._load_data()
    
    def _load_data(self) -> dict:
        """Загружает данные о паролях из файла"""
        if os.path.exists(self.data_file):
            with open(self.data_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def _save_data(self):
        """Сохраняет данные в файл"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.passwords, f, ensure_ascii=False, indent=2)
    
    # === ЭТАП 1: РУЧНОЕ УПРАВЛЕНИЕ (MVP) ===
    
    def create_simple_password(self, password: str, company_name: str, tests_limit: int = 10):
        """Создает простой пароль для группы"""
        self.passwords[password] = {
            "company_name": company_name,
            "tests_limit": tests_limit,
            "used_tests": 0,
            "created_at": datetime.now().isoformat(),
            "reports": [],
            "active": True
        }
        self._save_data()
        print(f"✅ Создан пароль '{password}' для {company_name} (лимит: {tests_limit} тестов)")
    
    def check_password(self, password: str) -> Optional[dict]:
        """Проверяет пароль и возвращает информацию"""
        if password in self.passwords:
            data = self.passwords[password]
            if data["active"] and data["used_tests"] < data["tests_limit"]:
                return data
        return None
    
    def use_test(self, password: str, employee_name: str, report_path: str) -> bool:
        """Отмечает использование теста"""
        if password in self.passwords:
            data = self.passwords[password]
            if data["used_tests"] < data["tests_limit"]:
                data["used_tests"] += 1
                data["reports"].append({
                    "employee_name": employee_name,
                    "report_path": report_path,
                    "completed_at": datetime.now().isoformat()
                })
                self._save_data()
                return True
        return False
    
    # === ЭТАП 2: АВТОГЕНЕРАЦИЯ (РОСТ) ===
    
    def generate_company_password(self, company_name: str, tests_limit: int = 10) -> str:
        """Генерирует уникальный пароль для компании"""
        import secrets
        import string
        
        # Простой читаемый пароль: COMPANY123
        base = company_name.upper().replace(" ", "")[:7]
        suffix = ''.join(secrets.choice(string.digits) for _ in range(3))
        password = f"{base}{suffix}"
        
        # Проверяем уникальность
        while password in self.passwords:
            suffix = ''.join(secrets.choice(string.digits) for _ in range(3))
            password = f"{base}{suffix}"
        
        self.create_simple_password(password, company_name, tests_limit)
        return password
    
    # === ЭТАП 3: РАСШИРЕННОЕ УПРАВЛЕНИЕ (МАСШТАБ) ===
    
    def set_password_expiry(self, password: str, days: int = 365):
        """Устанавливает срок действия пароля"""
        if password in self.passwords:
            expires_at = datetime.now() + timedelta(days=days)
            self.passwords[password]["expires_at"] = expires_at.isoformat()
            self._save_data()
    
    def deactivate_password(self, password: str, reason: str = ""):
        """Деактивирует пароль"""
        if password in self.passwords:
            self.passwords[password]["active"] = False
            self.passwords[password]["deactivated_at"] = datetime.now().isoformat()
            self.passwords[password]["deactivation_reason"] = reason
            self._save_data()
    
    # === СТАТИСТИКА И ОТЧЕТЫ ===
    
    def get_password_stats(self, password: str) -> dict:
        """Возвращает статистику по паролю"""
        if password in self.passwords:
            data = self.passwords[password]
            return {
                "company": data["company_name"],
                "used": data["used_tests"],
                "limit": data["tests_limit"],
                "remaining": data["tests_limit"] - data["used_tests"],
                "reports_count": len(data["reports"]),
                "last_used": data["reports"][-1]["completed_at"] if data["reports"] else None
            }
        return {}
    
    def get_all_reports_for_password(self, password: str) -> List[dict]:
        """Возвращает все отчеты по паролю"""
        if password in self.passwords:
            return self.passwords[password]["reports"]
        return []
    
    def admin_overview(self) -> dict:
        """Общая статистика для админа"""
        total_passwords = len(self.passwords)
        active_passwords = sum(1 for p in self.passwords.values() if p["active"])
        total_tests_used = sum(p["used_tests"] for p in self.passwords.values())
        total_reports = sum(len(p["reports"]) for p in self.passwords.values())
        
        return {
            "total_passwords": total_passwords,
            "active_passwords": active_passwords,
            "total_tests_used": total_tests_used,
            "total_reports": total_reports,
            "companies": [p["company_name"] for p in self.passwords.values()]
        }

# === ИНТЕГРАЦИЯ С БОТОМ ===

class BotPasswordIntegration:
    """Интеграция системы паролей с ботом"""
    
    def __init__(self):
        self.password_manager = SimplePasswordManager()
    
    async def handle_employee_login(self, password: str, user_id: int) -> tuple:
        """Обрабатывает вход сотрудника"""
        password_data = self.password_manager.check_password(password)
        
        if password_data:
            remaining = password_data["tests_limit"] - password_data["used_tests"]
            return True, f"✅ Добро пожаловать в {password_data['company_name']}!\nОсталось тестов: {remaining}"
        else:
            return False, "❌ Неверный пароль или превышен лимит тестирований"
    
    async def complete_employee_test(self, password: str, employee_name: str, report_path: str):
        """Завершает тест сотрудника"""
        success = self.password_manager.use_test(password, employee_name, report_path)
        
        if success:
            # Отправляем отчет сотруднику
            # Добавляем отчет в Google Drive для компании
            stats = self.password_manager.get_password_stats(password)
            return f"✅ Тест завершен!\nОсталось тестов: {stats['remaining']}"
        else:
            return "❌ Ошибка при сохранении результатов"
    
    async def admin_get_password_reports(self, password: str) -> str:
        """Возвращает все отчеты по паролю для админа"""
        reports = self.password_manager.get_all_reports_for_password(password)
        stats = self.password_manager.get_password_stats(password)
        
        if not reports:
            return f"📋 Пароль '{password}' ({stats['company']}): тесты не проводились"
        
        result = f"📊 Отчеты по паролю '{password}' ({stats['company']}):\n\n"
        result += f"Использовано: {stats['used']}/{stats['limit']} тестов\n\n"
        
        for i, report in enumerate(reports, 1):
            result += f"{i}. {report['employee_name']}\n"
            result += f"   📅 {report['completed_at'][:16]}\n"
            result += f"   📄 {report['report_path']}\n\n"
        
        return result

# === ПРИМЕРЫ ИСПОЛЬЗОВАНИЯ ===

def demo_password_evolution():
    """Демонстрация эволюции системы паролей"""
    
    pm = SimplePasswordManager()
    
    print("=== ЭТАП 1: Ручное создание паролей ===")
    # Вы создаете пароль вручную
    pm.create_simple_password("TESTCOMP2025", "ООО Тест Компания", 5)
    pm.create_simple_password("INNOVATE123", "Инновейт Групп", 10)
    
    print("\n=== Сотрудники проходят тесты ===")
    # Сотрудники используют пароли
    pm.use_test("TESTCOMP2025", "Иванов Иван", "report_ivanov.pdf")
    pm.use_test("TESTCOMP2025", "Петров Петр", "report_petrov.pdf")
    
    print("\n=== Проверка статистики ===")
    stats = pm.get_password_stats("TESTCOMP2025")
    print(f"Статистика: {stats}")
    
    print("\n=== ЭТАП 2: Автогенерация (в будущем) ===")
    # Автоматическая генерация паролей
    auto_password = pm.generate_company_password("Новая Компания", 15)
    print(f"Сгенерирован пароль: {auto_password}")
    
    print("\n=== ЭТАП 3: Управление (масштаб) ===")
    # Расширенное управление
    pm.set_password_expiry("TESTCOMP2025", 30)  # 30 дней
    
    print("\n=== Общая статистика ===")
    overview = pm.admin_overview()
    print(f"Админ обзор: {overview}")

if __name__ == "__main__":
    demo_password_evolution()