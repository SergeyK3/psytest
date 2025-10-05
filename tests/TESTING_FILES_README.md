# 🧪 TESTS - Тестовые и отладочные скрипты

Папка содержит все тестовые, отладочные и вспомогательные скрипты проекта PsychTest.

## 📋 Структура папки

### 🔧 Отладочные файлы (debug_*.py)
- `debug_enhanced_patch.py` - отладка улучшенного PDF генератора
- `debug_enhanced_test.py` - тестирование enhanced PDF функций
- `debug_page_numbers.py` - отладка нумерации страниц
- `debug_question_7.py` - отладка конкретного вопроса
- `debug_soft_parsing.py` - отладка парсинга soft skills
- `debug_log.txt` - лог файл отладки

### 🎯 Демонстрационные файлы (demo_*.py)
- `demo_improvements.py` - демонстрация улучшений
- `demo_paei_combined.py` - демо комбинированных PAEI тестов
- `pure_canvas_demo.py` - демо чистого canvas

### 📊 Тестовые файлы (test_*.py)
- `test_adizes_parsing.py` - тест парсинга Адизеса
- `test_ai_with_new_format.py` - тест ИИ с новым форматом
- `test_answer_parsing.py` - тест парсинга ответов
- `test_auto_gdrive.py` - тест автоматической загрузки в Google Drive
- `test_bot_integration.py` - тест интеграции с ботом
- `test_bot_simulation.py` - симуляция работы бота
- `test_canvas_issue.py` - тест проблем с canvas
- `test_concurrent_users.py` - тест одновременных пользователей
- `test_corrected_format.py` - тест исправленного формата
- `test_description_quality.py` - тест качества описаний
- `test_detailed_descriptions.py` - тест детальных описаний
- `test_disc_parsing.py` - тест парсинга DISC
- `test_disc_pie_chart.py` - тест круговых диаграмм DISC
- `test_enhanced_gdrive.py` - тест улучшенной Google Drive интеграции
- `test_enhanced_v2_output.py` - тест вывода enhanced v2
- `test_exit_buttons.py` - тест кнопок выхода
- `test_exit_functionality.py` - тест функционала выхода
- `test_final_enhanced.py` - финальный тест enhanced версии
- `test_first_question.py` - тест первого вопроса
- `test_fixed_format.py` - тест исправленного формата
- `test_fixed_handlers.py` - тест исправленных обработчиков
- `test_gdrive_only.py` - тест сохранения только в Google Drive
- `test_google_drive.py` - тест Google Drive функций
- `test_logic_consistency.py` - тест логической согласованности
- `test_paei_combined.py` - тест комбинированного PAEI
- `test_page_format_final.py` - финальный тест формата страниц
- `test_page_numbering.py` - тест нумерации страниц
- `test_page_numbers.py` - тест номеров страниц
- `test_pdf_with_indents.py` - тест PDF с отступами
- `test_position_numbering.py` - тест позиционной нумерации
- `test_prompt_format.py` - тест формата промптов
- `test_question_loading.py` - тест загрузки вопросов
- `test_soft_skills_parsing.py` - тест парсинга soft skills
- `test_upload_debug_pdf.py` - тест загрузки отладочного PDF
- `test_v4_working.py` - тест рабочей версии v4
- `test_working_v4.py` - тест working v4

### 👁️ Визуальные тесты (visual_*.py)
- `visual_numbering_check.py` - визуальная проверка нумерации
- `visual_positioning_test.py` - тест визуального позиционирования

### 🔧 Вспомогательные файлы
- `minimal_enhanced_test.py` - минимальный enhanced тест
- `quick_visual_test.py` - быстрый визуальный тест
- `simple_enhanced_test.py` - простой enhanced тест
- `simple_file_sharing.py` - простой файлообмен
- `simple_soft_test.py` - простой soft skills тест
- `study_enhanced_signatures.py` - изучение enhanced подписей
- `temp_delete.py` - временный файл для удаления
- `working_enhanced_report.py` - рабочий enhanced отчет
- `working_numbering_solution.py` - рабочее решение нумерации
- `working_pdf_generator.py` - рабочий PDF генератор

## 📝 Правила размещения

**ВСЕГДА размещайте в папке `tests/`:**
- Файлы с префиксами: `test_`, `debug_`, `demo_`, `visual_`, `quick_`, `simple_`, `minimal_`, `pure_`, `temp_`, `working_`, `study_`
- Временные и экспериментальные скрипты
- Отладочные логи и файлы
- Вспомогательные утилиты для разработки

## 🎯 Назначение папки

Эта папка содержит весь вспомогательный код для:
- 🧪 Тестирования функций
- 🐛 Отладки проблем  
- 📊 Демонстрации возможностей
- 🔍 Визуальной проверки
- ⚡ Быстрого прототипирования

**Основной код проекта остается в корне - только рабочие, production-ready файлы!**