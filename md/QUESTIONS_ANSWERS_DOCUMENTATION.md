# Модуль questions_answers_section.py - Документация

## Назначение
Модуль предназначен для создания приложения к PDF отчетам с детализацией вопросов и ответов всех психологических тестов. **ВАЖНО**: Приложение включается только в полные отчеты, загружаемые на Google Drive, и НЕ отправляется пользователям в Telegram.

## Структура модуля

### Основные функции

#### `get_all_questions()`
Загружает все вопросы из промпт-файлов:
- **PAEI**: 5 вопросов из `data/prompts/adizes_user.txt`
- **DISC**: 8 вопросов из `data/prompts/disc_user.txt`  
- **Soft Skills**: 9 вопросов из `data/prompts/soft_user.txt`
- **HEXACO**: 6 вопросов из `data/prompts/hexaco_user.txt`

#### Парсеры вопросов:
- `parse_paei_questions()` - PAEI с вариантами ответов P/A/E/I
- `parse_disc_questions()` - DISC с категориями D/I/S/C
- `parse_soft_skills_questions()` - Soft Skills с названиями навыков
- `parse_hexaco_questions()` - HEXACO с факторами H/E/X/A/C/O

### Класс QuestionAnswerSection

#### Методы генерации разделов:
- `generate_paei_questions_section()` - Раздел PAEI с выделением выбранных ответов
- `generate_disc_questions_section()` - Раздел DISC с оценками 1-5
- `generate_soft_skills_questions_section()` - Раздел навыков с интерпретацией уровней
- `generate_hexaco_questions_section()` - Раздел HEXACO с описанием факторов
- `generate_complete_questions_section()` - Полное приложение для всех тестов

## Интеграция с PDF генератором

### В enhanced_pdf_report_v2.py:
```python
# Для пользователей Telegram (БЕЗ приложения)
generator = EnhancedPDFReportV2(include_questions_section=False)

# Для Google Drive (С приложением)  
generator = EnhancedPDFReportV2(include_questions_section=True)
```

### В telegram_test_bot.py:
```python
# Пользовательский отчет без вопросов
pdf_generator_user = EnhancedPDFReportV2(include_questions_section=False)

# Отчет для Google Drive с вопросами
pdf_generator_gdrive = EnhancedPDFReportV2(include_questions_section=True)
```

## Структура данных

### Формат вопросов PAEI:
```python
{
    'question': 'Текст вопроса',
    'answers': {
        'P': 'Вариант Producer',
        'A': 'Вариант Administrator', 
        'E': 'Вариант Entrepreneur',
        'I': 'Вариант Integrator'
    }
}
```

### Формат вопросов DISC:
```python
{
    'question': 'Текст вопроса',
    'category': 'D|I|S|C',
    'question_id': '1.1|2.2|...'
}
```

### Формат вопросов Soft Skills:
```python
{
    'question': 'Текст вопроса',
    'skill': 'Название навыка'
}
```

### Формат вопросов HEXACO:
```python
{
    'question': 'Текст вопроса', 
    'dimension': 'H|E|X|A|C|O'
}
```

## Результат в PDF

### Структура приложения:
1. **Заголовок**: "ПРИЛОЖЕНИЕ: ДЕТАЛИЗАЦИЯ ВОПРОСОВ И ОТВЕТОВ"
2. **Описание назначения**: Контроль и проверка корректности интерпретации
3. **Разделы по тестам**:
   - PAEI с методикой подсчета (+1 балл за выбор)
   - DISC с оценками по шкале 1-5
   - Soft Skills с интерпретацией уровней
   - HEXACO с описанием факторов

### Особенности отображения:
- **PAEI**: Выделение выбранного ответа жирным шрифтом + указание начисленного балла
- **DISC/Soft Skills/HEXACO**: Ответ пользователя с интерпретацией уровня
- Методика подсчета для каждого теста
- Итоговые баллы в начале каждого раздела

## Тестирование

### Файлы для тестирования:
- `test_questions_simple.py` - Простой тест загрузки без ReportLab
- `test_report_formatting.py full` - Полный тест с генерацией PDF

### Команда тестирования:
```bash
python test_questions_simple.py
python test_report_formatting.py full
```

## Статус

✅ **Готово к продакшену**: Все тесты проходят, интеграция с PDF работает
✅ **Google Drive**: Отчеты с приложением загружаются корректно  
✅ **Telegram**: Пользователи получают краткие отчеты без приложения

Последнее обновление: 20 октября 2025 г.