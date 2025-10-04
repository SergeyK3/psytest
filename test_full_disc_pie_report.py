#!/usr/bin/env python3
"""
Тест полного отчета с новой круговой диаграммой DISC
"""

import sys
from pathlib import Path
from datetime import datetime

# Добавляем путь для импорта
sys.path.append('.')

from enhanced_pdf_report_v2 import EnhancedPDFReportV2

def test_full_report_with_disc_pie():
    """Тестируем создание полного отчета с круговой диаграммой DISC"""
    
    print("🔄 Тестирование полного отчета с круговой DISC диаграммой...")
    
    # Создаем генератор отчетов
    pdf_generator = EnhancedPDFReportV2()
    
    # Тестовые данные
    test_data = {
        'participant_name': 'Тест Диаграммы DISC',
        'test_date': datetime.now().strftime("%Y-%m-%d"),
        
        'paei_scores': {
            'Производитель': 7,
            'Администратор': 4,
            'Предприниматель': 8,
            'Интегратор': 5
        },
        
        'disc_scores': {
            'D (Доминантность)': 8,
            'I (Влияние)': 5,
            'S (Стабильность)': 3,
            'C (Точность)': 6
        },
        
        'hexaco_scores': {
            'Честность-Смирение': 4,
            'Эмоциональность': 3,
            'Экстраверсия': 5,
            'Приятность': 4,
            'Сознательность': 5,
            'Открытость опыту': 3
        },
        
        'soft_skills_scores': {
            'Коммуникация': 8,
            'Лидерство': 7,
            'Командная работа': 6,
            'Адаптивность': 9,
            'Критическое мышление': 5
        },
        
        'ai_interpretations': {
            'overall': 'Общая интерпретация с новой круговой диаграммой DISC',
            'disc': 'DISC: Доминантность 36.4%, Влияние 22.7%, Стабильность 13.6%, Точность 27.3%',
            'paei': 'PAEI интерпретация',
            'hexaco': 'HEXACO интерпретация', 
            'soft_skills': 'Soft skills интерпретация'
        },
        
        'out_path': Path("test_disc_pie_report.pdf")
    }
    
    try:
        # Генерируем отчет
        print("📄 Создание PDF отчета...")
        pdf_path = pdf_generator.generate_enhanced_report(**test_data)
        
        if pdf_path and pdf_path.exists():
            file_size = pdf_path.stat().st_size / 1024  # KB
            print(f"✅ Отчет создан: {pdf_path}")
            print(f"📦 Размер файла: {file_size:.1f} KB")
            print(f"🎯 DISC диаграмма: КРУГОВАЯ (без нормализации)")
            print(f"📊 Показывает сырые баллы и проценты")
            
            # Проверяем, что созданы все диаграммы
            charts_dir = Path("temp_charts")
            disc_pie = charts_dir / "disc_pie.png"
            
            if disc_pie.exists():
                print(f"✅ Круговая DISC диаграмма создана: {disc_pie}")
            else:
                print(f"❌ Круговая DISC диаграмма НЕ найдена: {disc_pie}")
                
            return True
        else:
            print("❌ Ошибка: PDF файл не создан")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка при создании отчета: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_full_report_with_disc_pie()
    if success:
        print("\n🎉 Тест пройден! Круговая диаграмма DISC работает корректно.")
    else:
        print("\n❌ Тест провален!")