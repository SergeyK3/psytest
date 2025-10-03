# Папка Tests - Централизованное тестирование

**Дата создания:** 3 октября 2025 г.  
**Статус:** ✅ Организована

## Обзор

Централизованная папка для всех тестовых файлов и папок проекта психологического тестирования. Содержит 32 Python теста и 15 папок с тестовыми данными.

## Структура тестов

### 🐍 Python тесты (32 файла)

#### Интеграционные тесты
- `test_ai_integration.py` - тесты AI интерпретатора
- `test_bot_integration.py` - интеграция Telegram бота
- `test_bot_connection.py` - тесты подключения бота

#### PDF генерация
- `test_comprehensive_pdf.py` - базовые PDF отчеты
- `test_comprehensive_pdf_v2.py` - улучшенные PDF отчеты v2
- `test_pdf_enhanced.py` - расширенные PDF функции
- `test_pdf_v2.py` - PDF версии 2
- `test_cyrillic_pdf.py` - поддержка кириллицы
- `test_font_comparison.py` - сравнение шрифтов

#### Диаграммы и визуализация
- `test_charts.py` - базовые диаграммы
- `test_embedded_charts.py` - встроенные диаграммы
- `test_paei_disc_bar_charts.py` - столбиковые диаграммы PAEI/DISC
- `test_updated_charts_system.py` - обновленная система диаграмм

#### Нормализация и масштабирование
- `test_normalization.py` - базовая нормализация
- `test_scale_normalization.py` - нормализация шкал
- `test_pdf_normalization.py` - нормализация в PDF
- `test_selective_normalization.py` - селективная нормализация
- `test_telegram_normalization.py` - нормализация в Telegram
- `test_rounding_validation.py` - валидация округления

#### Система отчетов
- `test_report_archiver.py` - архивирование отчетов
- `test_scenarios.py` - тестовые сценарии
- `test_normalized_report_demo.py` - демо нормализованных отчетов
- `test_selective_demo.py` - селективные демо

#### API и промпты
- `test_api_prompts.py` - API промпты
- `test_comprehensive_prompts.py` - комплексные промпты
- `test_improved_prompts.py` - улучшенные промпты
- `test_prompt_loading.py` - загрузка промптов

#### Финальные версии
- `test_final_balanced_system.py` - финальная сбалансированная система
- `test_final_updates.py` - финальные обновления
- `test_final_version.py` - финальная версия
- `test_improved_structure.py` - улучшенная структура
- `test_unified_scoring.py` - единая система оценок

### 📂 Тестовые папки (15 папок)

#### Выходные данные тестов
- `test_pdf_output/` - выходные PDF файлы
- `test_pdf_v2_output/` - выходные PDF v2
- `test_charts_output/` - выходные диаграммы
- `test_reports/` - тестовые отчеты

#### Специализированные тесты
- `test_balanced_charts/` - сбалансированные диаграммы
- `test_balanced_integration/` - сбалансированная интеграция
- `test_embedded_charts/` - встроенные диаграммы
- `test_normalization_methods/` - методы нормализации
- `test_normalized_pdf/` - нормализованные PDF
- `test_updated_charts/` - обновленные диаграммы

#### Итерации разработки
- `test_final_updates/` - финальные обновления
- `test_final_version/` - финальная версия
- `test_improved_structure/` - улучшенная структура
- `test_unified_scoring/` - единая система оценок
- `test_charts_analysis/` - анализ диаграмм

### 📄 Документация
- `TEST_SCENARIOS_README.md` - описание тестовых сценариев

## Запуск тестов

### Отдельные тесты
```bash
# Запуск конкретного теста
python tests/test_charts.py

# Запуск PDF тестов
python tests/test_comprehensive_pdf_v2.py

# Запуск нормализации
python tests/test_scale_normalization.py
```

### Массовый запуск
```bash
# Запуск всех тестов в папке (если есть pytest)
pytest tests/

# Ручной запуск всех Python тестов
for file in tests/test_*.py; do python "$file"; done
```

## Организация проекта

**До реорганизации:**
- Тестовые файлы были разбросаны по корневой папке
- Сложно было найти нужный тест
- Загроможденность основной структуры проекта

**После реорганизации:**
- ✅ Все тесты в одной папке `tests/`
- ✅ Четкая структура и навигация
- ✅ Легко найти и запустить нужный тест
- ✅ Чистая корневая папка проекта

## Совместимость

**Обратная совместимость:**
- ✅ Все существующие тесты сохраняют функциональность
- ✅ Импорты автоматически корректируются Python
- ✅ Относительные пути в тестах работают корректно

**Будущие тесты:**
- 🎯 Все новые тесты создавать в папке `tests/`
- 🎯 Следовать соглашению именования `test_*.py`
- 🎯 Группировать связанные тесты в подпапки при необходимости

## Статистика

- **📊 Всего тестов:** 32 Python файла
- **📂 Тестовых папок:** 15 директорий  
- **💾 Общий размер:** ~200 KB Python кода
- **🎯 Покрытие:** Все основные модули системы

---

**🎉 Структура тестов централизована и готова к использованию!**