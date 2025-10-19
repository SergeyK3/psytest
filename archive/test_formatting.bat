@echo off
REM Скрипт для быстрого тестирования форматирования отчетов

echo ==========================================
echo   БЫСТРОЕ ТЕСТИРОВАНИЕ ФОРМАТИРОВАНИЯ
echo ==========================================
echo.

:menu
echo Выберите тип отчета:
echo 1. Пользовательский отчет (краткий)
echo 2. Полный отчет (с деталями вопросов)  
echo 3. Оба отчета
echo 4. Выход
echo.

set /p choice="Ваш выбор (1-4): "

if "%choice%"=="1" (
    echo Генерация пользовательского отчета...
    python test_report_formatting.py user
    goto menu
)

if "%choice%"=="2" (
    echo Генерация полного отчета...
    python test_report_formatting.py full
    goto menu
)

if "%choice%"=="3" (
    echo Генерация обоих отчетов...
    python test_report_formatting.py both
    goto menu
)

if "%choice%"=="4" (
    echo До свидания!
    exit
)

echo Неверный выбор. Попробуйте еще раз.
goto menu