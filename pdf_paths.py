#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Утилита для стандартизации путей сохранения PDF отчетов
"""

from pathlib import Path
from datetime import datetime

def get_docs_pdf_path(filename_prefix: str = "report", participant_name: str = None) -> Path:
    """
    Создает стандартизированный путь для сохранения PDF в папку docs/
    
    Args:
        filename_prefix: префикс имени файла
        participant_name: имя участника (опционально)
    
    Returns:
        Path: полный путь к файлу PDF в папке docs/
    """
    # Создаем папку docs/ если не существует
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    
    # Генерируем временную метку
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # Формируем имя файла
    if participant_name:
        # Очищаем имя от недопустимых символов
        clean_name = "".join(c for c in participant_name if c.isalnum() or c in " -_").strip()
        clean_name = clean_name.replace(" ", "_")
        filename = f"{timestamp}_{filename_prefix}_{clean_name}.pdf"
    else:
        filename = f"{timestamp}_{filename_prefix}.pdf"
    
    return docs_dir / filename

def get_docs_dir() -> Path:
    """Возвращает путь к папке docs/, создавая ее при необходимости"""
    docs_dir = Path("docs")
    docs_dir.mkdir(exist_ok=True)
    return docs_dir

if __name__ == "__main__":
    # Тест функций
    print("🧪 Тест функций управления путями PDF:")
    
    # Тест с именем участника
    path1 = get_docs_pdf_path("demo", "Иван Иванович")
    print(f"   С именем: {path1}")
    
    # Тест без имени
    path2 = get_docs_pdf_path("test")
    print(f"   Без имени: {path2}")
    
    # Тест папки
    docs = get_docs_dir()
    print(f"   Папка docs: {docs}")
    
    print(f"✅ Все пути ведут в docs/")