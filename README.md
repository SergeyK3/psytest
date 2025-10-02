# PsyTest

Психологическое тестирование (PAEI → DISC → HEXACO).  
Проект реализован на Python с использованием **Streamlit**, **pandas**, **matplotlib**, **python-docx**, **reportlab**.  
Поддерживается генерация отчётов (DOCX/PDF) и визуализация профилей (радар-чарты).

Поддерживается два режима интерпретации результатов:
- **Статические интерпретации** из CSV файлов (по умолчанию)
- **AI интерпретации** с помощью OpenAI GPT-3.5 (опционально)

---

## Настройка

### Базовая установка
```powershell
pip install -e .
```

### Настройка AI интерпретаций (опционально)
1. Скопируйте `.env.example` в `.env`
2. Получите API ключ OpenAI на https://platform.openai.com/api-keys
3. Укажите ключ в файле `.env`:
```
OPENAI_API_KEY=your_actual_api_key_here
USE_AI_INTERPRETATIONS=true
```

---

## Запуск

### Веб-интерфейс (Streamlit)
```powershell
streamlit run src/psytest/web_app.py
```

### CLI
```powershell
python -m psytest.cli_main
```

---

## Структура проекта
psytest/
├─ src/
│  └─ psytest/
│     ├─ __init__.py
│     ├─ cli_main.py          # запуск из командной строки
│     ├─ web_app.py           # веб-интерфейс (Streamlit)
│     ├─ bank.py              # загрузка банка вопросов
│     ├─ scoring.py           # функции подсчёта результатов
│     ├─ charts.py            # построение радар-чартов
│     ├─ report.py            # генерация отчёта DOCX
│     ├─ report_pdf.py        # генерация отчёта PDF
│     └─ ...
├─ data/
│  ├─ bank/                   # CSV-файлы с вопросами (PAEI, DISC, HEXACO)
│  └─ interpretations/        # интерпретации по шкалам
├─ templates/
│  └─ report_template.docx    # шаблон для DOCX отчёта
├─ requirements.txt
└─ README.md

