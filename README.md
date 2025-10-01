# PsyTest

Психологическое тестирование (PAEI → DISC → HEXACO).  
Проект реализован на Python с использованием **Streamlit**, **pandas**, **matplotlib**, **python-docx**, **reportlab**.  
Поддерживается генерация отчётов (DOCX/PDF) и визуализация профилей (радар-чарты).

---

## Запуск CLI

Для запуска приложения в консольном режиме:
```powershell
python -m psytest.cli_main

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

