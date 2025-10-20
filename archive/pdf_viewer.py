#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Утилита для открытия PDF файлов из проекта
"""

import os
import subprocess
from pathlib import Path

def open_pdf(filename):
    """Открывает PDF файл правильным способом"""
    
    if not os.path.exists(filename):
        print(f"❌ Файл {filename} не найден!")
        return False
    
    try:
        # Для Windows - правильная команда открытия PDF
        subprocess.run(['cmd', '/c', 'start', '', filename], shell=False, check=True)
        print(f"📖 Открыт PDF: {filename}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка открытия: {e}")
        return False
    except Exception as e:
        print(f"⚠️ Не удалось открыть PDF: {e}")
        print(f"📁 Откройте файл вручную: {os.path.abspath(filename)}")
        return False

def list_pdf_files():
    """Показывает все PDF файлы в проекте"""
    
    pdf_files = list(Path('.').glob('*.pdf'))
    
    if not pdf_files:
        print("📭 PDF файлы не найдены")
        return []
    
    print("📄 Доступные PDF файлы:")
    for i, pdf_file in enumerate(pdf_files, 1):
        size = pdf_file.stat().st_size
        size_kb = size / 1024
        print(f"  {i}. {pdf_file.name} ({size_kb:.1f} KB)")
    
    return pdf_files

def main():
    """Главная функция - показывает меню выбора PDF"""
    
    print("🔍 PDF Viewer - Утилита просмотра PDF файлов")
    print("=" * 50)
    
    pdf_files = list_pdf_files()
    
    if not pdf_files:
        return
    
    print("\nВыберите файл для открытия:")
    print("0. Выход")
    
    try:
        choice = input("\nВведите номер файла: ").strip()
        
        if choice == "0":
            print("👋 До свидания!")
            return
        
        file_index = int(choice) - 1
        
        if 0 <= file_index < len(pdf_files):
            selected_file = pdf_files[file_index]
            open_pdf(str(selected_file))
        else:
            print("❌ Неверный номер файла!")
            
    except ValueError:
        print("❌ Пожалуйста, введите число!")
    except KeyboardInterrupt:
        print("\n👋 До свидания!")

if __name__ == "__main__":
    main()