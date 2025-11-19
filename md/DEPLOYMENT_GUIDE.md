# Инструкция для развертывания бота

## Минимальные требования (бот работает без Google Drive):

1. Установить зависимости:

   ```bash
   pip install -r requirements.txt
   ```

1. Настроить переменные окружения или в коде:

   - Telegram Bot Token

1. Запустить:

   ```bash
   python telegram_test_bot.py
   ```

## Для полной функциональности с Google Drive:

1. Выполнить минимальные требования
1. Создать OAuth credentials в Google Cloud Console
1. Скачать oauth_credentials.json в корень проекта
1. При первом запуске пройти OAuth авторизацию
1. Бот автоматически создаст папку в Google Drive

## Проверка работоспособности:

```bash
# Тест базовой функциональности
python test_google_drive.py

# Тест OAuth (если настроен)
python oauth_google_drive.py
```

## Файлы для .gitignore (уже настроено):

- google_drive_credentials.json
- oauth_credentials.json
- token.json
