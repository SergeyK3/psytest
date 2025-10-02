#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Модуль для автоматического сохранения отчетов в локальную папку docs/reports/
"""
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any
import re

class ReportArchiver:
    """Класс для автоматического архивирования отчетов"""
    
    def __init__(self, base_dir: Path = None):
        """
        Инициализация архиватора отчетов
        
        Args:
            base_dir: Базовая директория проекта (по умолчанию текущая)
        """
        if base_dir is None:
            base_dir = Path(__file__).parent.parent
        
        self.base_dir = Path(base_dir)
        self.reports_dir = self.base_dir / "docs" / "reports"
        
        # Создаем папку если её нет
        self.reports_dir.mkdir(parents=True, exist_ok=True)
    
    def save_report(self, source_path: Path, test_type: str, 
                   user_name: str = "User", additional_info: Dict[str, Any] = None) -> Path:
        """
        Сохраняет отчет в архивную папку с информативным именем
        
        Args:
            source_path: Путь к исходному файлу отчета
            test_type: Тип теста (DISC, PAEI, HEXACO, etc.)
            user_name: Имя пользователя (анонимизированное)
            additional_info: Дополнительная информация для имени файла
            
        Returns:
            Путь к сохраненному файлу
        """
        if not source_path.exists():
            raise FileNotFoundError(f"Исходный файл не найден: {source_path}")
        
        # Формируем временную метку
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        
        # Очищаем имя пользователя от небезопасных символов
        safe_user_name = re.sub(r'[^\w\-_.]', '_', user_name)[:20]
        
        # Формируем имя файла
        filename_parts = [timestamp, test_type.upper(), safe_user_name]
        
        # Добавляем дополнительную информацию если есть
        if additional_info:
            for key, value in additional_info.items():
                safe_value = re.sub(r'[^\w\-_.]', '_', str(value))[:10]
                filename_parts.append(f"{key}_{safe_value}")
        
        # Создаем финальное имя файла
        filename = "_".join(filename_parts) + source_path.suffix
        destination = self.reports_dir / filename
        
        # Копируем файл
        shutil.copy2(source_path, destination)
        
        # Логируем сохранение
        print(f"📁 Отчет сохранен: {destination.name}")
        
        return destination
    
    def save_telegram_report(self, source_path: Path, user_id: int, 
                           test_type: str, user_name: str = None) -> Path:
        """
        Специальный метод для сохранения отчетов из Telegram бота
        
        Args:
            source_path: Путь к PDF файлу
            user_id: ID пользователя Telegram
            test_type: Тип теста
            user_name: Имя пользователя (если доступно)
            
        Returns:
            Путь к сохраненному файлу
        """
        # Анонимизируем пользователя
        if user_name:
            display_name = user_name.split()[0] if user_name.split() else "User"
        else:
            display_name = f"TgUser{str(user_id)[-4:]}"  # Последние 4 цифры ID
        
        additional_info = {
            "tg": str(user_id)[-4:],  # Последние 4 цифры для идентификации
            "v": "balanced"  # Версия с сбалансированными диаграммами
        }
        
        return self.save_report(source_path, test_type, display_name, additional_info)
    
    def get_report_stats(self) -> Dict[str, Any]:
        """
        Получает статистику сохраненных отчетов
        
        Returns:
            Словарь со статистикой
        """
        reports = list(self.reports_dir.glob("*.pdf"))
        
        # Подсчитываем по типам тестов
        test_types = {}
        dates = []
        
        for report in reports:
            # Парсим имя файла: YYYY-MM-DD_HH-MM-SS_TYPE_User...
            parts = report.stem.split("_")
            if len(parts) >= 3:
                test_type = parts[2]
                test_types[test_type] = test_types.get(test_type, 0) + 1
                
                # Извлекаем дату
                if len(parts) >= 2:
                    try:
                        date_str = f"{parts[0]}_{parts[1]}"
                        date = datetime.strptime(date_str, "%Y-%m-%d_%H-%M-%S")
                        dates.append(date)
                    except ValueError:
                        pass
        
        stats = {
            "total_reports": len(reports),
            "test_types": test_types,
            "date_range": {
                "first": min(dates).strftime("%Y-%m-%d %H:%M") if dates else None,
                "last": max(dates).strftime("%Y-%m-%d %H:%M") if dates else None
            },
            "reports_today": len([d for d in dates if d.date() == datetime.now().date()]),
            "storage_path": str(self.reports_dir)
        }
        
        return stats
    
    def cleanup_old_reports(self, days_to_keep: int = 30) -> int:
        """
        Удаляет старые отчеты
        
        Args:
            days_to_keep: Количество дней для хранения
            
        Returns:
            Количество удаленных файлов
        """
        cutoff_date = datetime.now().timestamp() - (days_to_keep * 24 * 60 * 60)
        reports = list(self.reports_dir.glob("*.pdf"))
        deleted_count = 0
        
        for report in reports:
            if report.stat().st_mtime < cutoff_date:
                report.unlink()
                deleted_count += 1
                print(f"🗑️ Удален старый отчет: {report.name}")
        
        return deleted_count

# Глобальный экземпляр для использования в других модулях
report_archiver = ReportArchiver()

def save_report_copy(source_path: Path, test_type: str, user_info: Dict[str, Any]) -> Optional[Path]:
    """
    Удобная функция для сохранения копии отчета
    
    Args:
        source_path: Путь к исходному отчету
        test_type: Тип теста
        user_info: Информация о пользователе
        
    Returns:
        Путь к сохраненной копии или None при ошибке
    """
    try:
        if "telegram_id" in user_info:
            return report_archiver.save_telegram_report(
                source_path, 
                user_info["telegram_id"], 
                test_type,
                user_info.get("name")
            )
        else:
            return report_archiver.save_report(
                source_path,
                test_type,
                user_info.get("name", "User"),
                user_info
            )
    except Exception as e:
        print(f"⚠️ Не удалось сохранить копию отчета: {e}")
        return None

def print_report_stats():
    """Выводит статистику сохраненных отчетов"""
    stats = report_archiver.get_report_stats()
    
    print(f"\n📊 СТАТИСТИКА ОТЧЕТОВ:")
    print(f"Всего отчетов: {stats['total_reports']}")
    print(f"Сегодня создано: {stats['reports_today']}")
    
    if stats['test_types']:
        print(f"По типам тестов:")
        for test_type, count in stats['test_types'].items():
            print(f"  • {test_type}: {count}")
    
    if stats['date_range']['first']:
        print(f"Период: {stats['date_range']['first']} - {stats['date_range']['last']}")
    
    print(f"Папка: {stats['storage_path']}")

if __name__ == "__main__":
    print("📁 СИСТЕМА АРХИВИРОВАНИЯ ОТЧЕТОВ")
    print("=" * 50)
    
    # Показываем текущую статистику
    print_report_stats()
    
    # Демонстрируем функциональность
    print(f"\n📂 Папка для отчетов готова: {report_archiver.reports_dir}")
    print("✅ Система настроена для автоматического сохранения отчетов")