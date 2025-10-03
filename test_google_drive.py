"""
Тест Google Drive интеграции
Этот файл поможет проверить работу загрузки PDF отчетов в Google Drive
"""

import sys
import os
from pathlib import Path

# Добавляем корневую директорию в путь для импортов
root_dir = Path(__file__).parent
sys.path.append(str(root_dir))

def test_google_drive_integration():
    """Тестирует интеграцию с Google Drive"""
    
    print("🚀 Начинаем тест Google Drive интеграции...")
    
    # Проверяем наличие файла с credentials
    credentials_path = root_dir / "google_drive_credentials.json"
    if not credentials_path.exists():
        print("❌ Файл google_drive_credentials.json не найден!")
        print("📖 Следуйте инструкциям в docs/google_drive_setup.md")
        return False
    
    print("✅ Файл credentials найден")
    
    try:
        # Импортируем класс для создания отчетов
        from enhanced_pdf_report_v2 import EnhancedPDFReportV2
        from datetime import datetime
        from pathlib import Path
        print("✅ Импорт EnhancedPDFReportV2 успешен")
        
        # Подготавливаем правильные параметры для Google Drive теста
        participant_name = "Тест GoogleDrive"
        test_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        paei_scores = {
            'Производитель': 8,
            'Администратор': 6, 
            'Предприниматель': 4,
            'Интегратор': 7
        }
        
        disc_scores = {
            'D (Доминирование)': 8,
            'I (Влияние)': 6,
            'S (Постоянство)': 4, 
            'C (Соответствие)': 7
        }
        
        hexaco_scores = {
            'Честность-Смирение': 7,
            'Эмоциональность': 6,
            'Экстраверсия': 8,
            'Приятность': 5,
            'Сознательность': 7,
            'Открытость опыту': 6
        }
        
        soft_skills_scores = {
            'Коммуникация': 8,
            'Лидерство': 7,
            'Командная работа': 6,
            'Адаптивность': 9,
            'Критическое мышление': 5
        }
        
        ai_interpretations = {
            'overall': 'Комплексная интерпретация для тестирования Google Drive интеграции',
            'disc': 'Тестовая DISC интерпретация с высоким D и низким S',
            'paei': 'Тестовая PAEI интерпретация - выраженный Производитель', 
            'hexaco': 'Тестовая HEXACO интерпретация - высокая Экстраверсия',
            'soft_skills': 'Тестовая интерпретация soft skills - сильная Адаптивность'
        }
        
        # Путь для сохранения файла
        out_path = Path("test_gdrive_report.pdf")
        
        print("📊 Тестовые данные подготовлены")
        
        # Создаем генератор отчетов
        report_generator = EnhancedPDFReportV2()
        print("✅ Генератор отчетов создан")
        
        # Генерируем отчет с загрузкой в Google Drive
        print("📤 Создаем отчет и загружаем в Google Drive...")
        result = report_generator.generate_enhanced_report_with_gdrive(
            participant_name=participant_name,
            test_date=test_date,
            paei_scores=paei_scores,
            disc_scores=disc_scores,
            hexaco_scores=hexaco_scores,
            soft_skills_scores=soft_skills_scores,
            ai_interpretations=ai_interpretations,
            out_path=out_path,
            upload_to_gdrive=True
        )
        
        if result:
            local_path, gdrive_link = result
            print(f"🎉 УСПЕХ!")
            print(f"📁 Локальный файл: {local_path}")
            print(f"☁️ Google Drive: {gdrive_link}")
            print(f"📧 Вы можете поделиться ссылкой: {gdrive_link}")
            return True
        else:
            print("❌ Ошибка при создании отчета")
            return False
            
    except ImportError as e:
        print(f"❌ Ошибка импорта: {e}")
        print("💡 Возможно, нужно установить Google API библиотеки:")
        print("   pip install google-api-python-client google-auth google-auth-oauthlib google-auth-httplib2")
        return False
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        print("💡 Проверьте настройки Google Drive API в docs/google_drive_setup.md")
        return False

def test_basic_pdf_generation():
    """Тестирует базовое создание PDF без Google Drive"""
    
    print("\n📄 Тестируем базовое создание PDF...")
    
    try:
        from enhanced_pdf_report_v2 import EnhancedPDFReportV2
        from datetime import datetime
        
        # Подготавливаем правильные параметры
        participant_name = "Тест Базовый PDF"
        test_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # Правильный формат данных для методов
        paei_scores = {
            'Производитель': 5,
            'Администратор': 5, 
            'Предприниматель': 5,
            'Интегратор': 5
        }
        
        disc_scores = {
            'D (Доминирование)': 5,
            'I (Влияние)': 5,
            'S (Постоянство)': 5, 
            'C (Соответствие)': 5
        }
        
        hexaco_scores = {
            'Честность-Смирение': 5,
            'Эмоциональность': 5,
            'Экстраверсия': 5,
            'Приятность': 5,
            'Сознательность': 5,
            'Открытость опыту': 5
        }
        
        soft_skills_scores = {
            'Коммуникация': 5,
            'Лидерство': 5,
            'Командная работа': 5,
            'Адаптивность': 5,
            'Критическое мышление': 5
        }
        
        ai_interpretations = {
            'overall': 'Тестовая интерпретация для проверки функциональности',
            'disc': 'Тестовая DISC интерпретация',
            'paei': 'Тестовая PAEI интерпретация', 
            'hexaco': 'Тестовая HEXACO интерпретация',
            'soft_skills': 'Тестовая интерпретация soft skills'
        }
        
        # Путь для сохранения файла
        from pathlib import Path
        out_path = Path("test_basic_report.pdf")
        
        report_generator = EnhancedPDFReportV2()
        
        # Генерируем PDF с правильными параметрами
        pdf_path = report_generator.generate_enhanced_report(
            participant_name=participant_name,
            test_date=test_date,
            paei_scores=paei_scores,
            disc_scores=disc_scores,
            hexaco_scores=hexaco_scores,
            soft_skills_scores=soft_skills_scores,
            ai_interpretations=ai_interpretations,
            out_path=out_path
        )
        
        if pdf_path and os.path.exists(pdf_path):
            print(f"✅ Базовый PDF создан: {pdf_path}")
            return True
        else:
            print("❌ Ошибка при создании базового PDF")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при создании базового PDF: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Тестирование системы отчетов\n")
    
    # Сначала тестируем базовую функциональность
    basic_success = test_basic_pdf_generation()
    
    if basic_success:
        print("\n" + "="*50)
        # Если базовый тест прошел, тестируем Google Drive
        gdrive_success = test_google_drive_integration()
        
        if gdrive_success:
            print("\n🎊 Все тесты прошли успешно!")
            print("💼 Система готова к использованию с Google Drive")
        else:
            print("\n⚠️ Базовая функциональность работает, но есть проблемы с Google Drive")
            print("📖 Проверьте настройки в docs/google_drive_setup.md")
    else:
        print("\n❌ Базовая функциональность не работает")
        print("🔧 Проверьте установку зависимостей и структуру проекта")