#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Быстрая проверка исправлений диаграмм
"""

import sys
from pathlib import Path
sys.path.append('.')

def quick_chart_test():
    """Быстрая проверка исправленных диаграмм"""
    
    print("🔧 ПРОВЕРКА ИСПРАВЛЕНИЙ")
    print("=" * 40)
    
    # Тестовые данные
    soft_data = {
        "Коммуникация": 4.2,
        "Работа в команде": 3.8, 
        "Лидерство": 4.5,
        "Критическое мышление": 3.9,
        "Управление временем": 4.1,
        "Стрессоустойчивость": 3.7,
        "Восприимчивость к критике": 4.3,  # ✨
        "Адаптивность": 4.0,
        "Решение проблем": 4.4,
        "Креативность": 3.6
    }
    
    hexaco_data = {'H': 4.2, 'E': 3.8, 'X': 4.1, 'A': 3.9, 'C': 4.3, 'O': 3.7}
    
    try:
        from enhanced_pdf_report_v2 import EnhancedCharts
        
        # Создаем папку
        test_dir = Path("quick_test")
        test_dir.mkdir(exist_ok=True)
        
        print("\n📊 Создание диаграмм...")
        
        # Soft Skills диаграммы (должны быть 5-балльная шкала)
        soft_labels = list(soft_data.keys())
        soft_values = list(soft_data.values())
        
        radar_path = test_dir / "soft_radar_5scale.png"
        EnhancedCharts.create_minimalist_radar(
            soft_labels, soft_values, "Soft Skills", radar_path
        )
        print(f"✅ Soft Skills радар: {radar_path}")
        
        # HEXACO диаграмма (должна быть 5-балльная шкала) 
        hexaco_labels = list(hexaco_data.keys())
        hexaco_values = list(hexaco_data.values())
        
        hexaco_path = test_dir / "hexaco_radar_5scale.png"
        EnhancedCharts.create_hexaco_radar(
            hexaco_labels, hexaco_values, "HEXACO", hexaco_path
        )
        print(f"✅ HEXACO радар: {hexaco_path}")
        
        print(f"\n🎯 РЕЗУЛЬТАТ:")
        print(f"📁 Диаграммы созданы в: {test_dir}")
        print("✅ Проверьте что шкала диаграмм идет от 0 до 5 (а не до 8 или 10)")
        print("✅ На Soft Skills диаграмме должно быть: 'Восприимчивость к критике'")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    quick_chart_test()