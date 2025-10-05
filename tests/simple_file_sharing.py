"""
Простое решение: сохранение файлов локально с генерацией публичных ссылок
"""

import os
import shutil
from pathlib import Path
from datetime import datetime
from typing import Optional

def create_simple_file_sharing_solution():
    """
    Простое решение вместо Google Drive:
    1. Сохраняем файлы в локальной папке reports/
    2. Генерируем уникальные имена файлов
    3. Возвращаем локальный путь для обмена
    """
    
    # Создаем папку для отчетов если не существует
    reports_dir = Path("reports")
    reports_dir.mkdir(exist_ok=True)
    
    # Создаем структуру по годам/месяцам
    now = datetime.now()
    year_month_dir = reports_dir / str(now.year) / f"{now.month:02d}"
    year_month_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Создана локальная структура: {year_month_dir}")
    return year_month_dir

def save_report_locally(source_file: str, participant_name: str) -> str:
    """
    Сохраняет отчет в локальной структуре папок
    
    Args:
        source_file: Путь к исходному PDF файлу
        participant_name: Имя участника
    
    Returns:
        Путь к сохраненному файлу
    """
    
    try:
        # Создаем структуру папок
        reports_dir = create_simple_file_sharing_solution()
        
        # Генерируем уникальное имя файла
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        safe_name = "".join(c for c in participant_name if c.isalnum() or c in (' ', '-', '_')).strip()
        safe_name = safe_name.replace(' ', '_')
        
        filename = f"report_{safe_name}_{timestamp}.pdf"
        destination = reports_dir / filename
        
        # Копируем файл в новое место
        shutil.copy2(source_file, destination)
        
        print(f"📄 Отчет сохранен: {destination}")
        print(f"📧 Для передачи клиенту: {destination.absolute()}")
        
        return str(destination.absolute())
        
    except Exception as e:
        print(f"❌ Ошибка сохранения: {e}")
        return source_file  # Возвращаем исходный файл

if __name__ == "__main__":
    # Тест простого решения
    print("🧪 Тестирование локального сохранения...")
    
    # Создаем тестовый файл
    test_file = "test_local.pdf"
    with open(test_file, 'w') as f:
        f.write("Тестовый PDF файл")
    
    # Сохраняем с помощью нашего решения
    result = save_report_locally(test_file, "Тест Пользователь")
    
    print(f"✅ Результат: {result}")
    
    # Удаляем тестовый файл
    os.remove(test_file)