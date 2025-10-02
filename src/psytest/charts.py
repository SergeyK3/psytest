
from math import pi, log, sqrt
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple

# Сбалансированная цветовая палитра для печати
PRINT_COLORS = {
    'primary': '#2C3E50',      # Глубокий синий-серый
    'secondary': '#34495E',     # Средний серый
    'light': '#BDC3C7',        # Светло-серый для сетки
    'accent': '#3498DB',        # Яркий синий для акцентов
    'fill': '#ECF0F1',          # Очень светлый для заливки
    'background': '#FFFFFF'     # Белый фон
}

def normalize_chart_values(values: List[float], method: str = "adaptive") -> Tuple[List[float], float, str]:
    """
    Нормализует значения для сбалансированных диаграмм
    
    Args:
        values: Исходные значения
        method: Метод нормализации ('adaptive', 'sqrt', 'log', 'minmax', 'none')
        
    Returns:
        Нормализованные значения, новый максимум, описание метода
    """
    if not values or len(values) == 0:
        return values, 10, "пустые_данные"
    
    max_val = max(values)
    min_val = min(v for v in values if v > 0) if any(v > 0 for v in values) else 1
    ratio = max_val / min_val if min_val > 0 else float('inf')
    
    if method == "none" or ratio <= 2.0:
        # Хорошо сбалансированные данные или принудительно без нормализации
        return values, max(max_val, 10), "без_нормализации"
    
    elif method == "adaptive":
        if ratio > 8.0:
            # Очень высокий дисбаланс - используем логарифм
            normalized = [log(v + 1, 2) if v > 0 else 0 for v in values]
            return normalized, max(normalized), "адаптивный_логарифм"
        elif ratio > 4.0:
            # Средний дисбаланс - квадратный корень
            normalized = [sqrt(v) if v >= 0 else 0 for v in values]
            return normalized, max(normalized), "адаптивный_корень"
        else:
            # Небольшой дисбаланс - мягкая нормализация
            mean_val = sum(values) / len(values)
            normalized = [v * 0.7 + mean_val * 0.3 for v in values]
            return normalized, max(normalized), "адаптивная_мягкая"
    
    elif method == "sqrt":
        normalized = [sqrt(v) if v >= 0 else 0 for v in values]
        return normalized, max(normalized), "квадратный_корень"
    
    elif method == "log":
        normalized = [log(v + 1, 2) if v > 0 else 0 for v in values]
        return normalized, max(normalized), "логарифм"
    
    elif method == "minmax":
        # Нормализация к диапазону 2-8 (избегаем крайних значений)
        old_range = max_val - min_val
        if old_range == 0:
            return [5.0] * len(values), 8.0, "константа"
        
        new_min, new_max = 2.0, 8.0
        new_range = new_max - new_min
        normalized = [new_min + (v - min_val) * new_range / old_range for v in values]
        return normalized, new_max, "минмакс_2-8"
    
    # По умолчанию возвращаем исходные значения
    return values, max(max_val, 10), "исходные"

def make_radar(labels, values, out_path: Path, title: str = "", max_value: int = 100, 
               normalize: bool = True, normalize_method: str = "adaptive"):
    """
    Создает сбалансированную радарную диаграмму, оптимизированную для печати
    
    Args:
        labels: Названия осей
        values: Значения для каждой оси
        out_path: Путь для сохранения файла
        title: Заголовок диаграммы
        max_value: Максимальное значение шкалы (игнорируется при normalize=True)
        normalize: Применять ли нормализацию для баланса
        normalize_method: Метод нормализации
    """
    # Нормализуем значения если требуется
    if normalize:
        norm_values, max_norm, method_used = normalize_chart_values(values, normalize_method)
        actual_max = max_norm * 1.1
        display_values = norm_values
        
        # Добавляем информацию о нормализации в заголовок
        if method_used not in ["без_нормализации", "исходные"] and title:
            title = f"{title} (норм: {method_used})"
    else:
        display_values = values
        actual_max = max_value
        method_used = "отключена"
    
    # Настройка matplotlib для качественной печати
    plt.rcParams.update({
        'font.size': 10,
        'font.family': 'sans-serif',
        'axes.linewidth': 1.0,
        'grid.linewidth': 0.6,
        'lines.linewidth': 2.0,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.15
    })
    
    N = len(labels)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    vals = list(display_values) + display_values[:1]
    
    # Создание фигуры
    fig = plt.figure(figsize=(5, 5), facecolor=PRINT_COLORS['background'])
    ax = plt.subplot(111, polar=True)
    
    # Настройка полярных осей
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    
    # Установка меток осей
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels, fontsize=10, color=PRINT_COLORS['primary'])
    
    # Улучшенная радиальная сетка
    if actual_max <= 4:
        tick_step = 1
    elif actual_max <= 8:
        tick_step = 2
    else:
        tick_step = max(1, int(actual_max / 4))
        
    ax.set_ylim(0, actual_max)
    ticks = np.arange(0, actual_max, tick_step)
    ax.set_yticks(ticks)
    ax.set_yticklabels([f'{t:.1f}' for t in ticks], 
                      fontsize=8, color=PRINT_COLORS['secondary'])
    
    # Улучшенная стилизация сетки
    ax.grid(True, color=PRINT_COLORS['light'], linewidth=0.6, alpha=0.8)
    ax.set_facecolor(PRINT_COLORS['background'])
    
    # Рисование диаграммы с улучшенным стилем
    line = ax.plot(angles, vals, color=PRINT_COLORS['accent'], linewidth=2.5, 
                  marker='o', markersize=6, markerfacecolor=PRINT_COLORS['accent'], 
                  markeredgecolor=PRINT_COLORS['background'], markeredgewidth=2)
    
    # Заливка области
    ax.fill(angles, vals, color=PRINT_COLORS['accent'], alpha=0.15)
    
    # Заголовок
    if title:
        plt.title(title, pad=25, fontsize=11, fontweight='bold', 
                 color=PRINT_COLORS['primary'])
    
    # Сохранение
    fig.savefig(out_path, format='png', bbox_inches='tight', 
                pad_inches=0.15, facecolor=PRINT_COLORS['background'], 
                edgecolor='none')
    plt.close(fig)
    return out_path

def make_bar_chart(labels, values, out_path: Path, title: str = "", 
                   max_value: int = 100, horizontal: bool = False,
                   normalize: bool = True, normalize_method: str = "adaptive"):
    """
    Создает сбалансированную столбчатую диаграмму для печати
    
    Args:
        labels: Названия категорий
        values: Значения для каждой категории
        out_path: Путь для сохранения файла
        title: Заголовок диаграммы
        max_value: Максимальное значение шкалы (игнорируется при normalize=True)
        horizontal: Горизонтальная ориентация
        normalize: Применять ли нормализацию для баланса
        normalize_method: Метод нормализации
    """
    # Нормализуем значения если требуется
    if normalize:
        norm_values, max_norm, method_used = normalize_chart_values(values, normalize_method)
        actual_max = max_norm * 1.15
        display_values = norm_values
        
        # Добавляем информацию о нормализации в заголовок
        if method_used not in ["без_нормализации", "исходные"] and title:
            title = f"{title} (норм: {method_used})"
    else:
        display_values = values
        actual_max = max_value * 1.15
        method_used = "отключена"
    
    plt.rcParams.update({
        'font.size': 10,
        'font.family': 'sans-serif',
        'axes.linewidth': 1.0,
        'figure.dpi': 300,
        'savefig.dpi': 300,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.2
    })
    
    # Создание фигуры
    if horizontal:
        fig, ax = plt.subplots(figsize=(7, 5), facecolor=PRINT_COLORS['background'])
    else:
        fig, ax = plt.subplots(figsize=(8, 6), facecolor=PRINT_COLORS['background'])
    
    if horizontal:
        bars = ax.barh(labels, display_values, color=PRINT_COLORS['accent'], 
                      edgecolor=PRINT_COLORS['background'], linewidth=1.5)
        ax.set_xlim(0, actual_max)
        ax.set_xlabel('Значение', fontsize=11, color=PRINT_COLORS['primary'])
        
        # Добавление значений на столбцы
        for i, (bar, norm_value, orig_value) in enumerate(zip(bars, display_values, values)):
            if normalize and method_used not in ["без_нормализации", "исходные"]:
                text = f'{orig_value:.1f} ({norm_value:.1f})'
            else:
                text = f'{orig_value:.1f}'
            ax.text(norm_value + actual_max*0.02, bar.get_y() + bar.get_height()/2, 
                   text, va='center', ha='left', 
                   fontsize=9, color=PRINT_COLORS['primary'])
    else:
        bars = ax.bar(labels, display_values, color=PRINT_COLORS['accent'], 
                     edgecolor=PRINT_COLORS['background'], linewidth=1.5)
        ax.set_ylim(0, actual_max)
        ax.set_ylabel('Значение', fontsize=11, color=PRINT_COLORS['primary'])
        
        # Поворот меток для лучшей читаемости
        ax.tick_params(axis='x', rotation=0, labelsize=10, pad=8)
        
        # Добавление значений на столбцы
        for bar, norm_value, orig_value in zip(bars, display_values, values):
            if normalize and method_used not in ["без_нормализации", "исходные"]:
                text = f'{orig_value:.1f}\n({norm_value:.1f})'
            else:
                text = f'{orig_value:.1f}'
            ax.text(bar.get_x() + bar.get_width()/2, norm_value + actual_max*0.02, 
                   text, ha='center', va='bottom', 
                   fontsize=9, color=PRINT_COLORS['primary'])
    
    # Улучшенная стилизация
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_color(PRINT_COLORS['secondary'])
    ax.spines['bottom'].set_color(PRINT_COLORS['secondary'])
    ax.tick_params(colors=PRINT_COLORS['secondary'])
    ax.set_facecolor(PRINT_COLORS['background'])
    
    # Улучшенная сетка
    ax.grid(True, alpha=0.4, color=PRINT_COLORS['light'], linewidth=0.6)
    ax.set_axisbelow(True)
    
    # Заголовок
    if title:
        ax.set_title(title, fontsize=12, fontweight='bold', 
                    color=PRINT_COLORS['primary'], pad=20)
    
    # Настройка размещения
    try:
        plt.tight_layout(pad=1.5)
    except:
        plt.subplots_adjust(bottom=0.15, left=0.12, right=0.95, top=0.9)
    
    # Сохранение
    fig.savefig(out_path, format='png', bbox_inches='tight', 
                pad_inches=0.25, facecolor=PRINT_COLORS['background'], 
                edgecolor='none')
    plt.close(fig)
    return out_path
