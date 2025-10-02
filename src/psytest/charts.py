
from math import pi
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

# Минималистичная цветовая палитра для печати
PRINT_COLORS = {
    'primary': '#2C2C2C',      # Темно-серый для линий
    'secondary': '#666666',     # Средний серый для сетки
    'light': '#E0E0E0',        # Светло-серый для фона
    'accent': '#4A4A4A',       # Акцентный серый
    'fill': '#F5F5F5'          # Очень светлый для заливки
}

def make_radar(labels, values, out_path: Path, title: str = "", max_value: int = 100):
    """
    Создает минималистичную радарную диаграмму, оптимизированную для печати
    
    Args:
        labels: Названия осей
        values: Значения для каждой оси
        out_path: Путь для сохранения файла
        title: Заголовок диаграммы
        max_value: Максимальное значение шкалы
    """
    # Настройка matplotlib для качественной печати
    plt.rcParams.update({
        'font.size': 9,
        'font.family': 'sans-serif',
        'axes.linewidth': 0.8,
        'grid.linewidth': 0.5,
        'lines.linewidth': 1.5,
        'patch.linewidth': 0.5,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.1
    })
    
    N = len(labels)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    vals = list(values) + values[:1]
    
    # Создание фигуры с оптимальным размером для PDF
    fig = plt.figure(figsize=(4, 4), facecolor='white')
    ax = plt.subplot(111, polar=True)
    
    # Настройка полярных осей
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    
    # Установка меток осей
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=8, color=PRINT_COLORS['primary'])
    
    # Настройка радиальной сетки
    ax.set_ylim(0, max_value)
    ax.set_yticks(range(0, max_value + 1, max_value // 4))
    ax.set_yticklabels([str(i) for i in range(0, max_value + 1, max_value // 4)], 
                       fontsize=7, color=PRINT_COLORS['secondary'])
    
    # Стилизация сетки
    ax.grid(True, color=PRINT_COLORS['secondary'], linewidth=0.5, alpha=0.7)
    ax.set_facecolor('white')
    
    # Рисование диаграммы
    line = ax.plot(angles, vals, color=PRINT_COLORS['primary'], linewidth=2, marker='o', 
                   markersize=4, markerfacecolor=PRINT_COLORS['primary'], 
                   markeredgecolor='white', markeredgewidth=1)
    
    # Заливка области
    ax.fill(angles, vals, color=PRINT_COLORS['primary'], alpha=0.1)
    
    # Добавление заголовка если необходимо
    if title:
        plt.title(title, pad=20, fontsize=10, fontweight='bold', 
                 color=PRINT_COLORS['primary'])
    
    # Сохранение с высоким качеством
    fig.savefig(out_path, format='png', bbox_inches='tight', 
                pad_inches=0.1, facecolor='white', edgecolor='none')
    plt.close(fig)
    return out_path

def make_bar_chart(labels, values, out_path: Path, title: str = "", 
                   max_value: int = 100, horizontal: bool = False):
    """
    Создает минималистичную столбчатую диаграмму для печати
    
    Args:
        labels: Названия категорий
        values: Значения для каждой категории
        out_path: Путь для сохранения файла
        title: Заголовок диаграммы
        max_value: Максимальное значение шкалы
        horizontal: Горизонтальная ориентация
    """
    plt.rcParams.update({
        'font.size': 9,
        'font.family': 'sans-serif',
        'axes.linewidth': 0.8,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.2  # Увеличиваем отступы
    })
    
    # Создание фигуры с достаточным пространством для меток
    if horizontal:
        fig, ax = plt.subplots(figsize=(6, 5), facecolor='white')
    else:
        # Увеличиваем высоту для вертикальных диаграмм с повернутыми метками
        fig, ax = plt.subplots(figsize=(7, 5), facecolor='white')
    
    if horizontal:
        bars = ax.barh(labels, values, color=PRINT_COLORS['primary'], 
                       edgecolor='white', linewidth=1)
        ax.set_xlim(0, max_value)
        ax.set_xlabel('Значение', fontsize=9, color=PRINT_COLORS['primary'])
        
        # Добавление значений на столбцы
        for i, (bar, value) in enumerate(zip(bars, values)):
            ax.text(value + max_value*0.02, bar.get_y() + bar.get_height()/2, 
                   f'{value}', va='center', ha='left', 
                   fontsize=8, color=PRINT_COLORS['primary'])
    else:
        bars = ax.bar(labels, values, color=PRINT_COLORS['primary'], 
                      edgecolor='white', linewidth=1)
        ax.set_ylim(0, max_value * 1.15)  # Увеличиваем место для меток
        ax.set_ylabel('Значение', fontsize=9, color=PRINT_COLORS['primary'])
        
        # Поворот меток для лучшей читаемости с увеличенным отступом
        ax.tick_params(axis='x', rotation=45, labelsize=8, pad=8)
        
        # Добавление значений на столбцы
        for bar, value in zip(bars, values):
            ax.text(bar.get_x() + bar.get_width()/2, value + max_value*0.02, 
                   f'{value}', ha='center', va='bottom', 
                   fontsize=8, color=PRINT_COLORS['primary'])
    
    # Стилизация
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(PRINT_COLORS['secondary'])
    ax.spines['bottom'].set_color(PRINT_COLORS['secondary'])
    ax.tick_params(colors=PRINT_COLORS['secondary'])
    ax.set_facecolor('white')
    
    # Сетка
    ax.grid(True, alpha=0.3, color=PRINT_COLORS['secondary'], linewidth=0.5)
    ax.set_axisbelow(True)
    
    # Заголовок
    if title:
        ax.set_title(title, fontsize=10, fontweight='bold', 
                    color=PRINT_COLORS['primary'], pad=15)
    
    # Настраиваем размещение элементов с обработкой исключений
    try:
        plt.tight_layout(pad=1.0)
    except:
        # Если tight_layout не работает, используем subplots_adjust
        plt.subplots_adjust(bottom=0.2, left=0.1, right=0.95, top=0.9)
    
    fig.savefig(out_path, format='png', bbox_inches='tight', 
                pad_inches=0.2, facecolor='white', edgecolor='none')
    plt.close(fig)
    return out_path
