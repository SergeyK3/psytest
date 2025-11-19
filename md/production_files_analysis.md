# 🚀 Production Deployment Files Analysis

## ✅ НЕОБХОДИМЫЕ файлы для production:

### 🤖 Основной функционал:

- `telegram_test_bot.py` - главный файл Telegram бота
- `enhanced_pdf_report_v2.py` - генерация PDF отчетов
- `oauth_google_drive.py` - интеграция с Google Drive
- `scale_normalizer.py` - нормализация данных
- `pdf_paths.py` - пути к PDF файлам

### 📁 Структуры данных:

- `data/` - папка с данными (schema.sql, interpretations/, prompts/, bank/)
- `templates/` - шаблоны для PDF
- `temp_charts/` - временные диаграммы (создается автоматически)

### ⚙️ Конфигурация:

- `requirements.txt` - Python зависимости (минимизированный)
- `.env.example` - пример переменных окружения
- `README.md` - документация для deployment
- `DEPLOYMENT_GUIDE.md` - руководство по развертыванию

### 🔐 Credentials (создаются при deployment):

- `google_drive_credentials.json` - Google API credentials
- `oauth_credentials.json` - OAuth токены
- `token.json` - Google Drive токены
- `.env` - переменные окружения

## ❌ НЕ НУЖНЫЕ файлы для production:

### 🧪 Тестирование:

- `test_*.py` - все тестовые файлы
- `tests/` - папка с тестами
- `analyze_*.py` - скрипты анализа
- `generate_test_reports.py`

### 🔧 Разработка:

- `demo_improvements.py`
- `bot_architecture_proposal.py`
- `bot_main.py` (старая версия)
- `examples/` - примеры кода
- `docs/` - документация разработки
- `comparison_before_after/`
- `comprehensive_test_reports/`

### 🗑️ Временные файлы:

- `__pycache__/` - кэш Python
- `*.pyc` - скомпилированные файлы
- `out_report.docx` - тестовый отчет
- `test_*.pdf` - тестовые PDF
- `psytest_full.zip` - архив

### 🏗️ Dev dependencies:

- `src/` - исходники разработки
- `setup.cfg`, `pyproject.toml` - настройки пакета
- `.venv/` - виртуальное окружение

## 📦 Минимальная структура production:

```
production-deploy/
├── telegram_test_bot.py           # Основной бот
├── enhanced_pdf_report_v2.py      # PDF генератор
├── oauth_google_drive.py          # Google Drive
├── scale_normalizer.py            # Нормализация
├── pdf_paths.py                   # Пути файлов
├── requirements.txt               # Минимальные зависимости
├── .env.example                   # Пример конфигурации
├── README.md                      # Deployment инструкция
├── DEPLOYMENT_GUIDE.md            # Подробное руководство
├── data/                          # Данные приложения
│   ├── schema.sql
│   ├── interpretations/
│   ├── prompts/
│   └── bank/
├── templates/                     # Шаблоны PDF
│   └── report_template.docx
└── deploy/                        # Deployment конфиги
    ├── Dockerfile
    ├── docker-compose.yml
    ├── psytest.service           # systemd service
    └── nginx.conf                # если нужен веб-интерфейс
```

## 🎯 Результат:

Размер production ветки: ~2-3 MB вместо ~50+ MB с тестами и dev файлами
