#!/bin/bash

# Скрипт управления systemd сервисом для Psychology Test Bot
# Использование: ./manage_service.sh [start|stop|restart|status|enable|disable|install|uninstall|logs]

SERVICE_NAME="psychtest-bot"
SERVICE_FILE="psychtest-bot.service"
SYSTEMD_PATH="/etc/systemd/system"

case "$1" in
    install)
        echo "🔧 Установка сервиса..."
        sudo cp $SERVICE_FILE $SYSTEMD_PATH/
        sudo systemctl daemon-reload
        echo "✅ Сервис установлен в $SYSTEMD_PATH/$SERVICE_FILE"
        echo "💡 Для включения автозапуска выполните: ./manage_service.sh enable"
        ;;
    uninstall)
        echo "🗑️ Удаление сервиса..."
        sudo systemctl stop $SERVICE_NAME 2>/dev/null
        sudo systemctl disable $SERVICE_NAME 2>/dev/null
        sudo rm -f $SYSTEMD_PATH/$SERVICE_FILE
        sudo systemctl daemon-reload
        echo "✅ Сервис удален"
        ;;
    start)
        echo "🚀 Запуск сервиса..."
        sudo systemctl start $SERVICE_NAME
        ;;
    stop)
        echo "⏹️ Остановка сервиса..."
        sudo systemctl stop $SERVICE_NAME
        ;;
    restart)
        echo "🔄 Перезапуск сервиса..."
        sudo systemctl restart $SERVICE_NAME
        ;;
    status)
        echo "📊 Статус сервиса:"
        sudo systemctl status $SERVICE_NAME
        ;;
    enable)
        echo "✅ Включение автозапуска..."
        sudo systemctl enable $SERVICE_NAME
        echo "🎯 Сервис будет автоматически запускаться при загрузке системы"
        ;;
    disable)
        echo "❌ Отключение автозапуска..."
        sudo systemctl disable $SERVICE_NAME
        ;;
    logs)
        echo "📋 Логи сервиса (последние 50 строк):"
        sudo journalctl -u $SERVICE_NAME -n 50 --no-pager
        ;;
    logs-follow)
        echo "📋 Мониторинг логов в реальном времени (Ctrl+C для выхода):"
        sudo journalctl -u $SERVICE_NAME -f
        ;;
    *)
        echo "🤖 Psychology Test Bot - Управление сервисом"
        echo ""
        echo "Использование: $0 {install|uninstall|start|stop|restart|status|enable|disable|logs|logs-follow}"
        echo ""
        echo "Команды:"
        echo "  install      - Установить сервис в systemd"
        echo "  uninstall    - Удалить сервис из systemd"
        echo "  start        - Запустить бота"
        echo "  stop         - Остановить бота"
        echo "  restart      - Перезапустить бота"
        echo "  status       - Показать статус сервиса"
        echo "  enable       - Включить автозапуск при загрузке"
        echo "  disable      - Отключить автозапуск"
        echo "  logs         - Показать последние логи"
        echo "  logs-follow  - Мониторинг логов в реальном времени"
        echo ""
        echo "Пример быстрой установки:"
        echo "  $0 install"
        echo "  $0 enable"
        echo "  $0 start"
        exit 1
        ;;
esac

# Показываем статус после выполнения команды (кроме logs)
if [[ "$1" != "logs" && "$1" != "logs-follow" && "$1" != "status" ]]; then
    echo ""
    echo "📊 Текущий статус:"
    sudo systemctl is-active $SERVICE_NAME --quiet && echo "✅ Сервис запущен" || echo "❌ Сервис остановлен"
    sudo systemctl is-enabled $SERVICE_NAME --quiet && echo "✅ Автозапуск включен" || echo "❌ Автозапуск отключен"
fi