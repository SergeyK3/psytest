#!/usr/bin/env python3
"""
Тест новой круговой диаграммы DISC
"""

import sys
from pathlib import Path

# Добавляем путь для импорта
sys.path.append('.')
sys.path.append('./src')

from enhanced_pdf_report import EnhancedCharts

def test_disc_pie_chart():
    """Тестируем создание круговой диаграммы DISC"""
    
    print("🔄 Тестирование круговой диаграммы DISC...")
    
    # Тестовые данные DISC (сырые баллы без нормализации)
    disc_scores = {
        "D (Доминантность)": 8,
        "I (Влияние)": 5,
        "S (Стабильность)": 3,
        "C (Точность)": 6
    }
    
    # Создаем диаграмму
    output_path = Path("temp_charts/test_disc_pie.png")
    output_path.parent.mkdir(exist_ok=True)
    
    try:
        result_path = EnhancedCharts.create_pie_chart(
            labels=list(disc_scores.keys()),
            values=list(disc_scores.values()),
            title="DISC - Модель поведения",
            out_path=output_path
        )
        
        print(f"✅ Диаграмма создана: {result_path}")
        print(f"📊 Данные: {disc_scores}")
        print(f"📈 Общая сумма: {sum(disc_scores.values())} баллов")
        
        # Проверяем проценты
        total = sum(disc_scores.values())
        print("\n📋 Распределение:")
        for label, value in disc_scores.items():
            percentage = (value / total) * 100
            print(f"   {label}: {value} баллов ({percentage:.1f}%)")
            
        print(f"\n🎯 Файл сохранен в: {result_path.absolute()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Ошибка при создании диаграммы: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_disc_pie_chart()