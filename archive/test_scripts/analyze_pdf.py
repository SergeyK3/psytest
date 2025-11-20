#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Анализ содержимого созданного PDF отчёта
"""

import os
from pathlib import Path

# Найдём последний созданный отчёт
docs_folder = Path("docs")
if docs_folder.exists():
    # Ищем последние PDF файлы
    pdf_files = list(docs_folder.glob("*.pdf"))
    if pdf_files:
        # Сортируем по времени изменения
        latest_pdf = max(pdf_files, key=lambda f: f.stat().st_mtime)
        print(f"📁 Последний созданный PDF: {latest_pdf}")
        print(f"📏 Размер файла: {latest_pdf.stat().st_size} байт")
        print(f"🕐 Время создания: {latest_pdf.stat().st_mtime}")
        
        # Попробуем извлечь текст из PDF для анализа
        try:
            import PyPDF2
            with open(latest_pdf, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text_content = ""
                for page in reader.pages:
                    text_content += page.extract_text()
                
                print(f"\n🔍 Анализ содержимого PDF:")
                print(f"📄 Количество страниц: {len(reader.pages)}")
                print(f"📝 Общий объём текста: {len(text_content)} символов")
                
                # Ищем секции DISC
                if "DISC" in text_content:
                    print("✅ Секция DISC найдена в PDF")
                    
                    # Ищем "Интерпретация DISC"
                    if "Интерпретация DISC" in text_content:
                        print("✅ Заголовок 'Интерпретация DISC' найден")
                        
                        # Извлечём фрагмент с DISC интерпретацией
                        disc_start = text_content.find("Интерпретация DISC")
                        if disc_start != -1:
                            # Берём 800 символов после заголовка
                            disc_fragment = text_content[disc_start:disc_start + 800]
                            print(f"\n📋 Фрагмент DISC интерпретации:")
                            print("=" * 50)
                            print(disc_fragment)
                            print("=" * 50)
                    else:
                        print("❌ Заголовок 'Интерпретация DISC' НЕ найден")
                        
                        # Ищем любые упоминания о доминировании, влиянии и т.д.
                        disc_keywords = ["Доминирование", "Влияние", "Устойчивость", "Соответствие правилам"]
                        found_keywords = [kw for kw in disc_keywords if kw in text_content]
                        if found_keywords:
                            print(f"✅ Найдены DISC ключевые слова: {found_keywords}")
                        else:
                            print("❌ DISC ключевые слова НЕ найдены")
                else:
                    print("❌ Секция DISC НЕ найдена в PDF")
                    
                # Ищем секции Soft Skills
                if "Soft Skills" in text_content:
                    print("✅ Секция Soft Skills найдена в PDF")
                    
                    # Проверяем на нумерацию
                    if any(f"{i}." in text_content for i in range(1, 11)):
                        print("⚠️  Возможна нумерация в Soft Skills (найдены цифры с точками)")
                    else:
                        print("✅ Нумерация в Soft Skills НЕ обнаружена")
                else:
                    print("❌ Секция Soft Skills НЕ найдена в PDF")
                    
        except ImportError:
            print("❌ PyPDF2 не установлен. Для анализа PDF установите: pip install PyPDF2")
        except Exception as e:
            print(f"❌ Ошибка при анализе PDF: {e}")
    else:
        print("❌ PDF файлы не найдены в папке docs")
else:
    print("❌ Папка docs не найдена")