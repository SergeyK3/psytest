#!/usr/bin/env python3
"""
Быстрый тест для проверки появления раздела рекомендаций по команде в PDF
"""

import os
from pathlib import Path
import PyPDF2

def test_pdf_has_team_recommendations():
    """Проверяем, есть ли раздел с рекомендациями по команде в PDF"""
    
    print("🔍 ПОИСК РЕКОМЕНДАЦИЙ ПО КОМАНДЕ В PDF ОТЧЕТАХ")
    print("=" * 60)
    
    # Ищем последние созданные PDF файлы
    docs_folder = Path("docs")
    if not docs_folder.exists():
        print("❌ Папка docs не найдена")
        return False
    
    # Находим все PDF файлы с сегодняшней датой
    today = "2025-10-24"
    pdf_files = list(docs_folder.glob(f"{today}*.pdf"))
    
    if not pdf_files:
        print(f"❌ PDF файлы с датой {today} не найдены")
        return False
    
    print(f"📁 Найдено {len(pdf_files)} PDF файлов:")
    for pdf_file in pdf_files:
        print(f"   • {pdf_file.name}")
    
    # Проверяем каждый PDF файл
    team_keywords = [
        'рекомендации по подбору', 'подбор кандидатов', 'подбору команды',
        'disc-компенсация', 'paei-дополнение', 'hexaco-баланс', 'soft skills-синергия',
        'команду', 'специалистов', 'баланса команды'
    ]
    
    for pdf_file in pdf_files:
        print(f"\n📄 Анализируем {pdf_file.name}:")
        
        try:
            with open(pdf_file, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                all_text = ""
                
                for page_num, page in enumerate(reader.pages):
                    text = page.extract_text()
                    all_text += text
                    print(f"   📃 Страница {page_num + 1}: {len(text)} символов")
                
                # Ищем ключевые слова
                all_text_lower = all_text.lower()
                found_keywords = []
                
                for keyword in team_keywords:
                    if keyword in all_text_lower:
                        found_keywords.append(keyword)
                
                if found_keywords:
                    print(f"   ✅ Найдены ключевые слова команд: {found_keywords}")
                    
                    # Ищем конкретные разделы
                    if 'рекомендации по подбору' in all_text_lower:
                        print("   🎯 НАЙДЕН РАЗДЕЛ: 'Рекомендации по подбору команды'")
                        return True
                else:
                    print("   ⚠️  Ключевые слова команд НЕ найдены")
                    
        except Exception as e:
            print(f"   ❌ Ошибка чтения PDF: {e}")
    
    return False

if __name__ == "__main__":
    success = test_pdf_has_team_recommendations()
    if success:
        print("\n🎊 УСПЕХ: Раздел рекомендаций по команде найден в PDF!")
    else:
        print("\n❌ ПРОБЛЕМА: Раздел рекомендаций по команде не найден в PDF")
        print("   Возможно, изменения не применились или нужно перезапустить бота")