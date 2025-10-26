#!/bin/bash
# Скрипт управления PsychTest Telegram Bot

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

SERVICE_NAME="psychtest-bot"
SERVICE_FILE="psychtest-bot.service"
INSTALL_PATH="/etc/systemd/system/$SERVICE_FILE"
CURRENT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Функция для вывода цветного текста
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Проверка прав администратора
check_sudo() {
    if [[ $EUID -eq 0 ]]; then
        print_error "Не запускайте этот скрипт от root! Используйте sudo для отдельных команд."
        exit 1
    fi
}

# Установка сервиса
install_service() {
    print_status "Установка systemd сервиса..."
    
    # Проверяем наличие файла сервиса
    if [[ ! -f "$CURRENT_DIR/$SERVICE_FILE" ]]; then
        print_error "Файл $SERVICE_FILE не найден в текущей директории!"
        exit 1
    fi
    
    # Обновляем пути в файле сервиса
    print_status "Обновление путей в конфигурации сервиса..."
    sed "s|/home/sergei/MyApps/PsychTest|$CURRENT_DIR|g" "$CURRENT_DIR/$SERVICE_FILE" > "/tmp/$SERVICE_FILE"
    
    # Устанавливаем пользователя
    CURRENT_USER=$(whoami)
    sed -i "s|User=sergei|User=$CURRENT_USER|g" "/tmp/$SERVICE_FILE"
    sed -i "s|Group=sergei|Group=$CURRENT_USER|g" "/tmp/$SERVICE_FILE"
    
    # Копируем файл сервиса
    sudo cp "/tmp/$SERVICE_FILE" "$INSTALL_PATH"
    sudo chmod 644 "$INSTALL_PATH"
    
    # Перезагружаем systemd
    sudo systemctl daemon-reload
    
    # Включаем автозапуск
    sudo systemctl enable "$SERVICE_NAME"
    
    print_success "Сервис успешно установлен и включен для автозапуска!"
    print_status "Файл сервиса: $INSTALL_PATH"
    print_status "Рабочая директория: $CURRENT_DIR"
    print_status "Пользователь: $CURRENT_USER"
}

# Удаление сервиса
uninstall_service() {
    print_status "Удаление systemd сервиса..."
    
    # Останавливаем сервис если он запущен
    if systemctl is-active --quiet "$SERVICE_NAME"; then
        sudo systemctl stop "$SERVICE_NAME"
        print_status "Сервис остановлен"
    fi
    
    # Отключаем автозапуск
    if systemctl is-enabled --quiet "$SERVICE_NAME"; then
        sudo systemctl disable "$SERVICE_NAME"
        print_status "Автозапуск отключен"
    fi
    
    # Удаляем файл сервиса
    if [[ -f "$INSTALL_PATH" ]]; then
        sudo rm "$INSTALL_PATH"
        print_status "Файл сервиса удален"
    fi
    
    # Перезагружаем systemd
    sudo systemctl daemon-reload
    sudo systemctl reset-failed
    
    print_success "Сервис успешно удален!"
}

# Запуск сервиса
start_service() {
    print_status "Запуск сервиса $SERVICE_NAME..."
    sudo systemctl start "$SERVICE_NAME"
    print_success "Сервис запущен!"
}

# Остановка сервиса
stop_service() {
    print_status "Остановка сервиса $SERVICE_NAME..."
    sudo systemctl stop "$SERVICE_NAME"
    print_success "Сервис остановлен!"
}

# Перезапуск сервиса
restart_service() {
    print_status "Перезапуск сервиса $SERVICE_NAME..."
    sudo systemctl restart "$SERVICE_NAME"
    print_success "Сервис перезапущен!"
}

# Статус сервиса
status_service() {
    print_status "Статус сервиса $SERVICE_NAME:"
    echo
    systemctl status "$SERVICE_NAME" --no-pager -l
    echo
    print_status "Автозапуск: $(systemctl is-enabled $SERVICE_NAME 2>/dev/null || echo 'отключен')"
    print_status "Активность: $(systemctl is-active $SERVICE_NAME 2>/dev/null || echo 'неактивен')"
}

# Просмотр логов
logs_service() {
    print_status "Логи сервиса $SERVICE_NAME (последние 50 строк):"
    echo
    journalctl -u "$SERVICE_NAME" -n 50 --no-pager
    echo
    print_status "Для просмотра логов в реальном времени: journalctl -u $SERVICE_NAME -f"
}

# Просмотр логов в реальном времени
follow_logs() {
    print_status "Логи сервиса $SERVICE_NAME в реальном времени (Ctrl+C для выхода):"
    echo
    journalctl -u "$SERVICE_NAME" -f
}

# Проверка зависимостей
check_dependencies() {
    print_status "Проверка зависимостей..."
    
    # Проверка Python
    if ! command -v python3 &> /dev/null; then
        print_error "Python3 не установлен!"
        exit 1
    fi
    
    # Проверка pip
    if ! command -v pip3 &> /dev/null; then
        print_warning "pip3 не найден, устанавливаем..."
        sudo apt update && sudo apt install -y python3-pip
    fi
    
    # Проверка requirements.txt
    if [[ -f "$CURRENT_DIR/requirements.txt" ]]; then
        print_status "Установка Python зависимостей..."
        pip3 install -r "$CURRENT_DIR/requirements.txt" --user
    else
        print_warning "Файл requirements.txt не найден"
    fi
    
    # Проверка .env файла
    if [[ ! -f "$CURRENT_DIR/.env" ]]; then
        print_warning "Файл .env не найден! Создайте его с необходимыми переменными окружения."
    fi
    
    print_success "Проверка зависимостей завершена!"
}

# Справка
show_help() {
    echo -e "${BLUE}PsychTest Telegram Bot - Управление systemd сервисом${NC}"
    echo
    echo "Использование: $0 [КОМАНДА]"
    echo
    echo "Команды:"
    echo "  install    - Установить и включить сервис"
    echo "  uninstall  - Удалить сервис"
    echo "  start      - Запустить сервис"
    echo "  stop       - Остановить сервис"
    echo "  restart    - Перезапустить сервис"
    echo "  status     - Показать статус сервиса"
    echo "  logs       - Показать логи сервиса"
    echo "  follow     - Показать логи в реальном времени"
    echo "  deps       - Проверить и установить зависимости"
    echo "  help       - Показать эту справку"
    echo
    echo "Примеры:"
    echo "  $0 install    # Установить сервис"
    echo "  $0 status     # Проверить статус"
    echo "  $0 logs       # Посмотреть логи"
    echo "  $0 follow     # Логи в реальном времени"
}

# Основная логика
main() {
    check_sudo
    
    case "${1:-help}" in
        install)
            check_dependencies
            install_service
            ;;
        uninstall)
            uninstall_service
            ;;
        start)
            start_service
            ;;
        stop)
            stop_service
            ;;
        restart)
            restart_service
            ;;
        status)
            status_service
            ;;
        logs)
            logs_service
            ;;
        follow)
            follow_logs
            ;;
        deps)
            check_dependencies
            ;;
        help|--help|-h)
            show_help
            ;;
        *)
            print_error "Неизвестная команда: $1"
            echo
            show_help
            exit 1
            ;;
    esac
}

# Запуск
main "$@"