#!/usr/bin/env python3
"""
Проверяем конкретный PDF на наличие раздела рекомендаций по команде
"""

import PyPDF2
from pathlib import Path

def check_pdf_for_teams(pdf_path):
    """Проверяем конкретный PDF файл"""
    
    print(f"🔍 АНАЛИЗ PDF: {pdf_path}")
    print("=" * 60)
    
    try:
        with open(pdf_path, 'rb') as file:
            reader = PyPDF2.PdfReader(file)
            
            print(f"📄 Количество страниц: {len(reader.pages)}")
            
            # Собираем весь текст
            all_text = ""
            for page_num, page in enumerate(reader.pages):
                text = page.extract_text()
                all_text += text
                print(f"   📃 Страница {page_num + 1}: {len(text)} символов")
            
            # Ищем ключевые слова
            team_keywords = [
                'рекомендации по подбору команды',
                'рекомендации по подбору',
                'подбор кандидатов',
                'подбору команды',
                'команду',
                'специалистов',
                'disc-компенсация',
                'paei-дополнение',
                'hexaco-баланс',
                'soft skills-синергия'
            ]
            
            all_text_lower = all_text.lower()
            
            print(f"\n📊 РЕЗУЛЬТАТЫ ПОИСКА:")
            print("-" * 40)
            
            found_any = False
            for keyword in team_keywords:
                if keyword in all_text_lower:
                    print(f"   ✅ НАЙДЕНО: '{keyword}'")
                    found_any = True
                else:
                    print(f"   ❌ НЕТ: '{keyword}'")
            
            if not found_any:
                print("\n⚠️  НИ ОДНО КЛЮЧЕВОЕ СЛОВО НЕ НАЙДЕНО!")
                
                # Покажем содержимое для отладки
                print("\n📝 СОДЕРЖИМОЕ PDF (первые 1000 символов):")
                print("-" * 40)
                print(all_text[:1000])
                print("\n...")
                
                # Ищем разделы
                sections = []
                for line in all_text.split('\n'):
                    if line.strip() and (line.isupper() or 'АНАЛИЗ' in line.upper() or 'ЗАКЛЮЧЕНИЕ' in line.upper()):
                        sections.append(line.strip())
                
                if sections:
                    print(f"\n📑 НАЙДЕННЫЕ РАЗДЕЛЫ ({len(sections)}):")
                    print("-" * 40)
                    for i, section in enumerate(sections[:20]):  # Показываем первые 20
                        print(f"   {i+1}. {section}")
            else:
                print(f"\n🎊 УСПЕХ: Найдено {sum(1 for k in team_keywords if k in all_text_lower)} ключевых слов!")
            
            return found_any
            
    except Exception as e:
        print(f"❌ ОШИБКА чтения PDF: {e}")
        return False

if __name__ == "__main__":
    # Проверяем последний созданный файл
    pdf_path = Path("archive/charts/final_test_adizes_markdown.pdf")
    
    if pdf_path.exists():
        success = check_pdf_for_teams(pdf_path)
        if success:
            print("\n🎉 ЗАКЛЮЧЕНИЕ: Раздел рекомендаций по команде найден!")
        else:
            print("\n❌ ЗАКЛЮЧЕНИЕ: Раздел рекомендаций по команде НЕ найден!")
    else:
        print(f"❌ ФАЙЛ НЕ НАЙДЕН: {pdf_path}")
        print("   Возможно, путь неверный или файл не существует")