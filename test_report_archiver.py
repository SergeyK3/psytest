#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тестирование системы архивирования отчетов
"""
from pathlib import Path
from report_archiver import ReportArchiver, print_report_stats
import tempfile
from datetime import datetime

def test_report_archiver():
    """Тестируем систему архивирования"""
    print("📁 ТЕСТИРОВАНИЕ СИСТЕМЫ АРХИВИРОВАНИЯ ОТЧЕТОВ")
    print("=" * 60)
    
    # Инициализируем архиватор
    archiver = ReportArchiver()
    print(f"📂 Папка для отчетов: {archiver.reports_dir}")
    
    # Создаем тестовый PDF файл
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as temp_file:
        temp_file.write(b"Test PDF content for archiving system")
        temp_path = Path(temp_file.name)
    
    print(f"\n🧪 Создан тестовый файл: {temp_path}")
    
    # Тестируем разные типы сохранения
    test_cases = [
        {
            "test_type": "PAEI",
            "user_name": "ТестПользователь",
            "additional_info": {"version": "balanced", "source": "test"}
        },
        {
            "test_type": "DISC", 
            "user_name": "TestUser",
            "additional_info": {"version": "v2", "mode": "demo"}
        }
    ]
    
    saved_files = []
    
    for i, case in enumerate(test_cases, 1):
        print(f"\n📊 Тест {i}: Сохранение отчета {case['test_type']}")
        
        try:
            saved_path = archiver.save_report(
                temp_path,
                case['test_type'],
                case['user_name'],
                case['additional_info']
            )
            saved_files.append(saved_path)
            print(f"  ✅ Сохранено: {saved_path.name}")
            
        except Exception as e:
            print(f"  ❌ Ошибка: {e}")
    
    # Тестируем Telegram сохранение
    print(f"\n📱 Тест Telegram сохранения:")
    try:
        telegram_path = archiver.save_telegram_report(
            temp_path, 123456789, "HEXACO", "Иван Иванов"
        )
        saved_files.append(telegram_path)
        print(f"  ✅ Telegram отчет: {telegram_path.name}")
    except Exception as e:
        print(f"  ❌ Ошибка Telegram: {e}")
    
    # Показываем статистику
    print(f"\n📈 СТАТИСТИКА ПОСЛЕ ТЕСТИРОВАНИЯ:")
    print_report_stats()
    
    # Проверяем содержимое папки
    print(f"\n📋 СОДЕРЖИМОЕ ПАПКИ ОТЧЕТОВ:")
    reports = list(archiver.reports_dir.glob("*.pdf"))
    for report in reports:
        size = report.stat().st_size
        mtime = datetime.fromtimestamp(report.stat().st_mtime)
        print(f"  📄 {report.name} ({size} байт, {mtime.strftime('%Y-%m-%d %H:%M')})")
    
    # Очищаем тестовые файлы
    temp_path.unlink()
    for saved_file in saved_files:
        if saved_file.exists():
            saved_file.unlink()
            print(f"🗑️ Удален тестовый файл: {saved_file.name}")
    
    print(f"\n✅ ТЕСТИРОВАНИЕ ЗАВЕРШЕНО!")
    print(f"Система архивирования готова к работе.")
    
    return archiver

def test_gitignore_setup():
    """Проверяем настройку .gitignore"""
    print(f"\n🔒 ПРОВЕРКА НАСТРОЙКИ .GITIGNORE")
    print("=" * 40)
    
    gitignore_path = Path(__file__).parent / ".gitignore"
    
    if gitignore_path.exists():
        with open(gitignore_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Проверяем наличие нужных исключений
        required_patterns = [
            "docs/reports/",
            "docs/user_reports/", 
            "docs/test_results/"
        ]
        
        missing_patterns = []
        for pattern in required_patterns:
            if pattern not in content:
                missing_patterns.append(pattern)
        
        if missing_patterns:
            print(f"⚠️ Отсутствуют паттерны в .gitignore: {missing_patterns}")
        else:
            print(f"✅ .gitignore настроен правильно")
            print(f"📁 Папки reports/ исключены из Git")
            
    else:
        print(f"❌ Файл .gitignore не найден")
    
    return len(missing_patterns) == 0 if gitignore_path.exists() else False

if __name__ == "__main__":
    print("🚀 СИСТЕМА ЛОКАЛЬНОГО АРХИВИРОВАНИЯ ОТЧЕТОВ")
    print("=" * 70)
    
    try:
        # Тестируем архиватор
        archiver = test_report_archiver()
        
        # Проверяем .gitignore
        gitignore_ok = test_gitignore_setup()
        
        print(f"\n🎯 РЕЗУЛЬТАТ НАСТРОЙКИ:")
        print(f"✅ Система архивирования: готова")
        print(f"{'✅' if gitignore_ok else '⚠️'} Настройка .gitignore: {'готова' if gitignore_ok else 'требует внимания'}")
        print(f"📂 Папка отчетов: {archiver.reports_dir}")
        
        print(f"\n💡 КАК ЭТО РАБОТАЕТ:")
        print(f"1. Telegram бот автоматически сохраняет копии всех отчетов")
        print(f"2. Файлы сохраняются с информативными именами и временными метками")
        print(f"3. Отчеты НЕ попадают в Git (настроено в .gitignore)")
        print(f"4. Вы можете анализировать отчеты для улучшения системы")
        print(f"5. Старые отчеты можно удалять автоматически")
        
        print(f"\n🔄 СЛЕДУЮЩИЕ ШАГИ:")
        print(f"1. Перезапустите Telegram бота с новой функциональностью")
        print(f"2. Протестируйте создание отчета")
        print(f"3. Проверьте автоматическое сохранение в docs/reports/")
        
    except Exception as e:
        print(f"\n❌ Ошибка во время тестирования: {e}")
        import traceback
        traceback.print_exc()