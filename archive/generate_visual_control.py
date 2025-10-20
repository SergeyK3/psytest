#!/usr/bin/env python3
"""
Генерация PDF отчета с комбинированной диаграммой PAEI для визуального контроля
"""

from enhanced_pdf_report_v2 import EnhancedPDFReportV2
from pathlib import Path
from datetime import datetime

def generate_visual_control_report():
    """Создает PDF отчет для визуального контроля комбинированной диаграммы PAEI"""
    
    print('🚀 Создание PDF отчета с комбинированной диаграммой PAEI для Google Drive')
    print('=' * 70)

    # Создаем генератор
    generator = EnhancedPDFReportV2()

    # Тестовые данные с акцентом на PAEI как на изображении
    test_data = {
        'participant_name': 'Визуальный Контроль PAEI',
        'test_date': datetime.now().strftime('%d.%m.%Y'),
        'paei_scores': {'P': 8, 'A': 5, 'E': 7, 'I': 4},  # Как на изображении
        'disc_scores': {'D': 6, 'I': 5, 'S': 4, 'C': 7},
        'hexaco_scores': {'H': 3.5, 'E': 3.2, 'X': 4.1, 'A': 3.8, 'C': 4.0, 'O': 3.6},
        'soft_skills_scores': {
            'Лидерство': 7, 
            'Коммуникация': 8, 
            'Адаптивность': 6, 
            'Критическое мышление': 7, 
            'Креативность': 6
        },
        'ai_interpretations': {
            'overall': 'Профиль демонстрирует сильные управленческие качества с выраженным фокусом на результат.',
            'paei': 'Ярко выраженный тип Производителя с элементами Предпринимателя. Высокая ориентация на достижение результатов.',
            'disc': 'Сбалансированный профиль с умеренным доминированием и высокой компетентностью.',
            'hexaco': 'Стабильная личность с хорошими показателями добросовестности и открытости.',
            'soft_skills': 'Сильные коммуникативные навыки и лидерский потенциал.'
        }
    }

    # Путь для выходного файла
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    output_path = Path('temp_charts') / f'paei_combined_visual_control_{timestamp}.pdf'

    try:
        # Генерируем отчет
        pdf_path, gdrive_link = generator.generate_enhanced_report_with_gdrive(
            out_path=output_path,
            **test_data
        )
        
        print(f'✅ PDF создан: {pdf_path}')
        print(f'📁 Размер файла: {pdf_path.stat().st_size / 1024:.1f} KB')
        
        if gdrive_link:
            print(f'🔗 Google Drive ссылка: {gdrive_link}')
        else:
            print('⚠️  Google Drive: загрузка не удалась, файл остался локально')
            
        # Проверяем созданные диаграммы
        paei_combined = Path('temp_charts/paei_combined.png')
        if paei_combined.exists():
            print(f'📊 Комбинированная диаграмма PAEI: {paei_combined.stat().st_size / 1024:.1f} KB')
        
        print('\n🎯 Результат:')
        print(f'  📄 PDF файл: {pdf_path}')
        if gdrive_link:
            print(f'  🔗 Google Drive: {gdrive_link}')
        print('  📊 Особенности: комбинированная диаграмма PAEI (столбиковая + круговая)')
        
        return pdf_path, gdrive_link
        
    except Exception as e:
        print(f'❌ Ошибка: {e}')
        import traceback
        traceback.print_exc()
        return None, None

if __name__ == "__main__":
    generate_visual_control_report()