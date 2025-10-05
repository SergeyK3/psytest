#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ВИЗУАЛЬНЫЙ ТЕСТ ПОЗИЦИОНИРОВАНИЯ НУМЕРАЦИИ СТРАНИЦ

Создает простой PDF с нумерацией в разных позициях для проверки:
1. Правильности расчетов координат
2. Видимости шрифта Arial с кириллицей
3. Размещения относительно краев страницы
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import red, blue, green, black
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

def register_arial_font():
    """Регистрируем Arial для поддержки кириллицы"""
    try:
        # Пробуем зарегистрировать Arial из системы Windows
        arial_path = "C:/Windows/Fonts/arial.ttf"
        if os.path.exists(arial_path):
            pdfmetrics.registerFont(TTFont('Arial', arial_path))
            print("✅ Arial успешно зарегистрирован")
            return True
        else:
            print("⚠️ Arial не найден, используем Helvetica")
            return False
    except Exception as e:
        print(f"⚠️ Ошибка регистрации Arial: {e}")
        return False

def create_position_test_pdf(filename: str):
    """
    Создает тестовый PDF с нумерацией в разных позициях
    """
    print(f"📄 Создаем тестовый PDF: {filename}")
    
    # Регистрируем Arial
    arial_available = register_arial_font()
    font_name = "Arial" if arial_available else "Helvetica"
    
    c = canvas.Canvas(filename, pagesize=A4)
    
    # === СТРАНИЦА 1: Тест всех углов ===
    print("📝 Страница 1: Тест позиций во всех углах")
    
    # Рисуем границы страницы для ориентации
    c.setStrokeColor(black)
    c.setLineWidth(0.5)
    c.rect(0, 0, A4[0], A4[1])  # Внешняя граница
    c.rect(20*mm, 20*mm, A4[0]-40*mm, A4[1]-40*mm)  # Внутренняя граница (рабочая область)
    
    # Настройки шрифта для нумерации
    c.setFont(font_name, 12)
    
    # === ТЕСТ ВСЕХ 4 УГЛОВ ===
    
    # 1. ПРАВЫЙ ВЕРХНИЙ УГОЛ (основная позиция)
    x_top_right = A4[0] - 15*mm
    y_top_right = A4[1] - 10*mm
    c.setFillColor(red)
    c.drawRightString(x_top_right, y_top_right, "Стр. 1 из 3 (ПРАВЫЙ ВЕРХ)")
    print(f"🔴 Правый верх: ({x_top_right:.1f}, {y_top_right:.1f})")
    
    # 2. ЛЕВЫЙ ВЕРХНИЙ УГОЛ
    x_top_left = 15*mm
    y_top_left = A4[1] - 10*mm
    c.setFillColor(blue)
    c.drawString(x_top_left, y_top_left, "Стр. 1 из 3 (ЛЕВЫЙ ВЕРХ)")
    print(f"🔵 Левый верх: ({x_top_left:.1f}, {y_top_left:.1f})")
    
    # 3. ПРАВЫЙ НИЖНИЙ УГОЛ
    x_bottom_right = A4[0] - 15*mm
    y_bottom_right = 10*mm
    c.setFillColor(green)
    c.drawRightString(x_bottom_right, y_bottom_right, "Стр. 1 из 3 (ПРАВЫЙ НИЗ)")
    print(f"🟢 Правый низ: ({x_bottom_right:.1f}, {y_bottom_right:.1f})")
    
    # 4. ЛЕВЫЙ НИЖНИЙ УГОЛ
    x_bottom_left = 15*mm
    y_bottom_left = 10*mm
    c.setFillColor(black)
    c.drawString(x_bottom_left, y_bottom_left, "Стр. 1 из 3 (ЛЕВЫЙ НИЗ)")
    print(f"⚫ Левый низ: ({x_bottom_left:.1f}, {y_bottom_left:.1f})")
    
    # Центр страницы для справки
    center_x = A4[0] / 2
    center_y = A4[1] / 2
    c.setFillColor(black)
    c.setFont(font_name, 16)
    c.drawCentredString(center_x, center_y, f"ЦЕНТР СТРАНИЦЫ")
    c.drawCentredString(center_x, center_y - 20, f"Используется шрифт: {font_name}")
    
    # Переходим на следующую страницу
    c.showPage()
    
    # === СТРАНИЦА 2: Тест размеров шрифта ===
    print("📝 Страница 2: Тест размеров шрифта")
    
    c.setFillColor(red)
    sizes = [8, 10, 12, 14, 16, 18]
    for i, size in enumerate(sizes):
        c.setFont(font_name, size)
        y_pos = A4[1] - 50*mm - (i * 30)
        x_pos = A4[0] - 15*mm
        c.drawRightString(x_pos, y_pos, f"Стр. 2 из 3 (размер {size})")
        print(f"📏 Размер {size}: позиция ({x_pos:.1f}, {y_pos:.1f})")
    
    c.showPage()
    
    # === СТРАНИЦА 3: Финальный тест с рекомендуемыми настройками ===
    print("📝 Страница 3: Финальные настройки")
    
    # ФИНАЛЬНЫЕ РЕКОМЕНДУЕМЫЕ НАСТРОЙКИ
    final_font_size = 10
    final_x = A4[0] - 15*mm  # 15мм от правого края
    final_y = A4[1] - 10*mm  # 10мм от верхнего края
    
    c.setFont(font_name, final_font_size)
    c.setFillColor(black)
    c.drawRightString(final_x, final_y, "Стр. 3 из 3")
    
    # Показываем координаты и расчеты
    c.setFont(font_name, 8)
    info_y = A4[1] - 40*mm
    c.drawString(20*mm, info_y, f"ФИНАЛЬНЫЕ НАСТРОЙКИ:")
    c.drawString(20*mm, info_y - 10, f"• Шрифт: {font_name}, размер: {final_font_size}")
    c.drawString(20*mm, info_y - 20, f"• X позиция: A4[0] - 15*mm = {final_x:.1f} points")
    c.drawString(20*mm, info_y - 30, f"• Y позиция: A4[1] - 10*mm = {final_y:.1f} points")
    c.drawString(20*mm, info_y - 40, f"• A4 размеры: {A4[0]:.1f} x {A4[1]:.1f} points")
    c.drawString(20*mm, info_y - 50, f"• 1 мм = {1*mm:.3f} points")
    
    print(f"✅ Финальные настройки: шрифт {font_name} {final_font_size}, позиция ({final_x:.1f}, {final_y:.1f})")
    
    c.save()
    print(f"💾 PDF сохранен: {filename}")

def test_font_positioning():
    """Главная функция тестирования"""
    print("🚀 НАЧИНАЕМ ВИЗУАЛЬНЫЙ ТЕСТ ПОЗИЦИОНИРОВАНИЯ")
    print("=" * 60)
    
    # Создаем тестовый PDF
    test_file = "visual_positioning_test.pdf"
    create_position_test_pdf(test_file)
    
    # Проверяем размер файла
    if os.path.exists(test_file):
        file_size = os.path.getsize(test_file)
        print(f"📊 Размер созданного файла: {file_size} байт")
        
        if file_size > 5000:  # Больше 5KB означает успешное создание
            print("✅ PDF создан успешно!")
            print("👀 ОТКРОЙТЕ ФАЙЛ ДЛЯ ВИЗУАЛЬНОЙ ПРОВЕРКИ:")
            print(f"   {os.path.abspath(test_file)}")
        else:
            print("⚠️ Файл слишком маленький, возможны проблемы")
    else:
        print("❌ Файл не создан!")

if __name__ == "__main__":
    test_font_positioning()