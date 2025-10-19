
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

# Профессиональная палитра для психологических тестов
# Основана на принципах психологии цвета и читаемости при печати
PSYCH_COLORS = {
    # PAEI цвета - спокойные профессиональные тона
    'PAEI': {
        'P': '#2E4A66',      # Глубокий синий (Производитель - стабильность, надежность)
        'A': '#5B9BD5',      # Средний синий (Администратор - организованность, порядок)  
        'E': '#4F81BD',      # Яркий синий (Предприниматель - инновации, динамика)
        'I': '#8FAADC'       # Светлый синий (Интегратор - гармония, объединение)
    },
    
    # DISC цвета - спокойная палитра в стиле PAEI (оттенки синего)
    'DISC': {
        'D': '#2E4A66',      # Глубокий синий (Доминирование - сила, решительность)
        'I': '#4F81BD',      # Средний синий (Влияние - общительность, энтузиазм)
        'S': '#5B9BD5',      # Яркий синий (Постоянство - стабильность, поддержка)
        'C': '#8FAADC'       # Светлый синий (Соответствие - точность, анализ)
    },
    
    # HEXACO цвета - гармоничная градация
    'HEXACO': {
        'H': '#8064A2',      # Фиолетовый (Честность-Скромность)
        'E': '#C55A5A',      # Кораллово-красный (Эмоциональность)
        'X': '#4F81BD',      # Синий (Экстраверсия)
        'A': '#70AD47',      # Зеленый (Доброжелательность)
        'C': '#E5B845',      # Желтый (Добросовестность)
        'O': '#9BBB59'       # Оливковый (Открытость опыту)
    },
    
    # Soft Skills цвета - мягкие тона
    'SOFT_SKILLS': [
        '#4F81BD',  # Синий
        '#70AD47',  # Зеленый
        '#E5B845',  # Желтый
        '#C55A5A',  # Красный
        '#8064A2',  # Фиолетовый
        '#5B9BD5',  # Голубой
        '#9BBB59',  # Оливковый
        '#2E4A66',  # Темно-синий
        '#8FAADC',  # Светло-синий
        '#B85450'   # Темно-красный
    ]
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
    if actual_max <= 5:
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

def make_pie_chart(labels, values, out_path: Path, title: str = "") -> Path:
    """
    Создает круговую диаграмму для печати
    
    Args:
        labels: Названия категорий
        values: Значения для каждой категории (без нормализации)
        out_path: Путь для сохранения файла
        title: Заголовок диаграммы
    """
    # Подготовка данных
    total = sum(values)
    percentages = [(value / total) * 100 for value in values]
    
    # Цвета для DISC
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4']
    
    # Создание диаграммы
    fig, ax = plt.subplots(figsize=(10, 8))
    
    # Настройка matplotlib для качественной печати
    plt.rcParams.update({
        'font.size': 12,
        'axes.titlesize': 14,
        'axes.labelsize': 12,
        'xtick.labelsize': 11,
        'ytick.labelsize': 11,
        'legend.fontsize': 11,
        'figure.titlesize': 16
    })
    
    # Создание круговой диаграммы с отключенными автоподписями
    wedges, texts, autotexts = ax.pie(
        values,
        labels=None,  # Убираем внешние лейблы
        colors=colors[:len(labels)],
        autopct='',  # Отключаем автоматические проценты - они мешают тексту
        startangle=90,
        wedgeprops={'linewidth': 2, 'edgecolor': 'white'}
    )
    
    # Добавляем текст внутри сегментов с улучшенным позиционированием
    for i, (wedge, label, value, percentage) in enumerate(zip(wedges, labels, values, percentages)):
        # Вычисляем угол для размещения текста
        angle = (wedge.theta2 + wedge.theta1) / 2
        
        # Размещаем текст ближе к краю сегмента, но не слишком близко
        radius_factor = 0.7 if percentage > 15 else 0.8  # Для больших сегментов - ближе к центру
        x = radius_factor * wedge.r * np.cos(np.radians(angle))
        y = radius_factor * wedge.r * np.sin(np.radians(angle))
        
        # Размещаем текст внутри сегмента
        if percentage > 8:  # Только для достаточно больших сегментов
            # Нежирный текст с увеличенным размером и прозрачным фоном
            ax.text(x, y, f'{label}\n{value} баллов\n{percentage:.1f}%', 
                   ha='center', va='center', fontsize=18, fontweight='normal',  # Нежирный текст
                   color='black', wrap=True)  # Убрали bbox - теперь фон полностью прозрачный
    
    # Заголовок
    if title:
        ax.set_title(title, fontsize=14, fontweight='bold', 
                    color=PRINT_COLORS['primary'], pad=20)
    
    # Убираем оси
    ax.axis('equal')
    
    # Настройка фона
    fig.patch.set_facecolor(PRINT_COLORS['background'])
    ax.set_facecolor(PRINT_COLORS['background'])
    
    # Сохранение
    plt.tight_layout()
    fig.savefig(out_path, format='png', bbox_inches='tight', 
                pad_inches=0.25, facecolor=PRINT_COLORS['background'], 
                edgecolor='none', dpi=300)
    plt.close(fig)
    return out_path

def make_paei_combined_chart(labels, values, out_path: Path, title: str = "") -> Path:
    """
    Создает комбинированную диаграмму для PAEI - столбиковая слева, круговая справа
    
    Args:
        labels: Названия категорий PAEI
        values: Значения для каждой категории
        out_path: Путь для сохранения файла
        title: Заголовок диаграммы
    """
    # Сбалансированная цветовая схема PAEI
    colors = PSYCH_COLORS['PAEI']
    
    # Подготовка данных
    total = sum(values)
    percentages = [(value / total) * 100 for value in values]
    
    # Маппинг меток на русские названия
    label_mapping = {
        'P': 'Производитель',
        'A': 'Администратор', 
        'E': 'Предприниматель',
        'I': 'Интегратор'
    }
    
    russian_labels = [label_mapping.get(label, label) for label in labels]
    chart_colors = [colors.get(label, '#4F81BD') for label in labels]
    
    # Настройка matplotlib для качественной печати на полную ширину
    plt.rcParams.update({
        'font.size': 12,
        'font.family': 'sans-serif',
        'axes.linewidth': 1.2,
        'figure.dpi': 150,  # увеличенный DPI для лучшего качества
        'savefig.dpi': 150,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.3  # увеличенные отступы
    })
    
    # Создание фигуры с двумя подграфиками - увеличенный размер для полной ширины
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')
    
    # === ЛЕВЫЙ ГРАФИК - СТОЛБИКОВАЯ ДИАГРАММА ===
    bars = ax1.bar(labels, values, color=chart_colors, 
                   edgecolor='white', linewidth=1.5, alpha=0.9)
    
    # Настройка столбиковой диаграммы
    ax1.set_ylim(0, max(values) * 1.2)
    ax1.set_ylabel('Количество баллов', fontsize=13, color='#2C3E50', fontweight='bold')
    ax1.set_title('PAEI - Уровни по типам', fontsize=14, fontweight='bold', 
                  color='#2C3E50', pad=20)
    
    # Добавление значений на столбцы
    for bar, value in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width()/2, value + max(values)*0.02, 
                f'{value}', ha='center', va='bottom', 
                fontsize=12, fontweight='bold', color='#2C3E50')
    
    # Стилизация столбиковой диаграммы
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color('#BDC3C7')
    ax1.spines['bottom'].set_color('#BDC3C7')
    ax1.tick_params(colors='#34495E', labelsize=10)
    ax1.set_facecolor('white')
    ax1.grid(True, alpha=0.3, color='#BDC3C7', linewidth=0.5)
    ax1.set_axisbelow(True)
    
    # === ПРАВЫЙ ГРАФИК - КРУГОВАЯ ДИАГРАММА ===
    wedges, texts = ax2.pie(values, labels=None, colors=chart_colors,
                            startangle=90, wedgeprops={'linewidth': 2, 'edgecolor': 'white'})
    
    ax2.set_title('PAEI - Пропорции баллов', fontsize=14, fontweight='bold', 
                  color='#2C3E50', pad=20)
    
    # Добавление текста в сегменты
    for i, (wedge, label, value, percentage, rus_label) in enumerate(zip(wedges, labels, values, percentages, russian_labels)):
        # Вычисляем угол для размещения текста
        angle = (wedge.theta2 + wedge.theta1) / 2
        
        # Размещаем текст в зависимости от размера сегмента
        radius_factor = 0.7 if percentage > 15 else 0.8
        x = radius_factor * wedge.r * np.cos(np.radians(angle))
        y = radius_factor * wedge.r * np.sin(np.radians(angle))
        
        # Размещаем текст внутри сегмента
        if percentage > 8:  # Только для достаточно больших сегментов
            ax2.text(x, y, f'{rus_label}\n{label} - {value}\n{percentage:.1f}%', 
                   ha='center', va='center', fontsize=11, fontweight='bold',
                   color='black')
    
    # Общая настройка фигуры
    fig.suptitle(title, fontsize=16, fontweight='bold', color='#2C3E50', y=0.98)
    
    # Настройка размещения для максимального использования пространства
    plt.tight_layout()
    plt.subplots_adjust(top=0.88, wspace=0.3)  # увеличенное пространство между графиками
    
    # Сохранение с увеличенным DPI для четкости
    fig.savefig(out_path, format='png', bbox_inches='tight', 
                pad_inches=0.3, facecolor='white', 
                edgecolor='none', dpi=150)
    plt.close(fig)
    return out_path

def make_disc_combined_chart(labels, values, out_path: Path, title: str = "") -> Path:
    """
    Создает комбинированную диаграмму для DISC - столбиковая слева, круговая справа
    
    Args:
        labels: Названия категорий DISC
        values: Значения для каждой категории
        out_path: Путь для сохранения файла
        title: Заголовок диаграммы
    """
    # Сбалансированная цветовая схема DISC
    colors = PSYCH_COLORS['DISC']
    
    # Подготовка данных
    total = sum(values)
    percentages = [(value / total) * 100 for value in values]
    
    # Маппинг меток на русские названия
    label_mapping = {
        'D': 'Доминирование',
        'I': 'Влияние', 
        'S': 'Постоянство',
        'C': 'Соответствие'
    }
    
    russian_labels = [label_mapping.get(label, label) for label in labels]
    chart_colors = [colors.get(label, '#3498DB') for label in labels]
    
    # Настройка matplotlib для качественной печати на полную ширину
    plt.rcParams.update({
        'font.size': 12,
        'font.family': 'sans-serif',
        'axes.linewidth': 1.2,
        'figure.dpi': 150,  # увеличенный DPI для лучшего качества
        'savefig.dpi': 150,
        'savefig.bbox': 'tight',
        'savefig.pad_inches': 0.3  # увеличенные отступы
    })
    
    # Создание фигуры с двумя подграфиками - увеличенный размер для полной ширины
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 6), facecolor='white')
    
    # === ЛЕВЫЙ ГРАФИК - СТОЛБИКОВАЯ ДИАГРАММА ===
    bars = ax1.bar(labels, values, color=chart_colors, 
                   edgecolor='white', linewidth=1.5, alpha=0.9)
    
    # Настройка столбиковой диаграммы
    ax1.set_ylim(0, max(values) * 1.2)
    ax1.set_ylabel('Количество баллов', fontsize=13, color='#2C3E50', fontweight='bold')
    ax1.set_title('DISC - Уровни по типам', fontsize=14, fontweight='bold', 
                  color='#2C3E50', pad=20)
    
    # Добавление значений на столбцы
    for bar, value in zip(bars, values):
        ax1.text(bar.get_x() + bar.get_width()/2, value + max(values)*0.02, 
                f'{value}', ha='center', va='bottom', 
                fontsize=12, fontweight='bold', color='#2C3E50')
    
    # Стилизация столбиковой диаграммы
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_color('#BDC3C7')
    ax1.spines['bottom'].set_color('#BDC3C7')
    ax1.tick_params(colors='#34495E', labelsize=12)
    ax1.set_facecolor('white')
    ax1.grid(True, alpha=0.3, color='#BDC3C7', linewidth=0.5)
    ax1.set_axisbelow(True)
    
    # === ПРАВЫЙ ГРАФИК - КРУГОВАЯ ДИАГРАММА ===
    wedges, texts = ax2.pie(values, labels=None, colors=chart_colors,
                            startangle=90, wedgeprops={'linewidth': 2, 'edgecolor': 'white'})
    
    ax2.set_title('DISC - Пропорции баллов', fontsize=14, fontweight='bold', 
                  color='#2C3E50', pad=20)
    
    # Добавление текста в сегменты
    for i, (wedge, label, value, percentage, rus_label) in enumerate(zip(wedges, labels, values, percentages, russian_labels)):
        # Вычисляем угол для размещения текста
        angle = (wedge.theta2 + wedge.theta1) / 2
        
        # Размещаем текст в зависимости от размера сегмента
        radius_factor = 0.7 if percentage > 15 else 0.8
        x = radius_factor * wedge.r * np.cos(np.radians(angle))
        y = radius_factor * wedge.r * np.sin(np.radians(angle))
        
        # Размещаем текст внутри сегмента
        if percentage > 8:  # Только для достаточно больших сегментов
            ax2.text(x, y, f'{rus_label}\n{label} - {value}\n{percentage:.1f}%', 
                   ha='center', va='center', fontsize=11, fontweight='bold',
                   color='white' if label in ['D'] else 'black')  # белый текст для темных цветов
    
    # Общая настройка фигуры
    fig.suptitle(title, fontsize=16, fontweight='bold', color='#2C3E50', y=0.98)
    
    # Настройка размещения для максимального использования пространства
    plt.tight_layout()
    plt.subplots_adjust(top=0.88, wspace=0.3)  # увеличенное пространство между графиками
    
    # Сохранение с увеличенным DPI для четкости
    fig.savefig(out_path, format='png', bbox_inches='tight', 
                pad_inches=0.3, facecolor='white', 
                edgecolor='none', dpi=150)
    plt.close(fig)
    return out_path

def make_hexaco_radar(labels, values, out_path: Path, title: str = "", max_value: int = 100, 
                     normalize: bool = True, normalize_method: str = "adaptive"):
    """
    Создает радарную диаграмму HEXACO с расшифровками аббревиатур
    
    Args:
        labels: Аббревиатуры HEXACO (H, E, X, A, C, O)
        values: Значения для каждой оси
        out_path: Путь для сохранения файла
        title: Заголовок диаграммы
        max_value: Максимальное значение шкалы (игнорируется при normalize=True)
        normalize: Применять ли нормализацию для баланса
        normalize_method: Метод нормализации
    """
    # Маппинг аббревиатур на полные названия (как на скриншоте)
    hexaco_mapping = {
        'H': 'H - Честность',
        'E': 'E - Эмоциональность', 
        'X': 'X - Экстраверсия',
        'A': 'A - Доброжелательность',
        'C': 'C - Добросовестность',
        'O': 'O - Открытость'
    }
    
    # Создаем расширенные лейблы
    extended_labels = [hexaco_mapping.get(label, label) for label in labels]
    
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
    N = len(extended_labels)
    angles = [n / float(N) * 2 * pi for n in range(N)]
    angles += angles[:1]
    vals = list(display_values) + display_values[:1]
    # Создание фигуры с увеличенным размером для длинных лейблов
    fig = plt.figure(figsize=(7, 7), facecolor=PRINT_COLORS['background'])
    ax = plt.subplot(111, polar=True)
    # Настройка полярных осей
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
    # Установка меток осей с расширенными названиями
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(extended_labels, fontsize=9, color=PRINT_COLORS['primary'])
    # Улучшенная радиальная сетка
    if actual_max <= 5:
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
    # Рисование диаграммы с цветом HEXACO
    hexaco_color = PSYCH_COLORS['HEXACO'].get('H', PRINT_COLORS['accent'])  # Используем цвет H как основной
    line = ax.plot(angles, vals, color=hexaco_color, linewidth=2.5, 
                  marker='o', markersize=6, markerfacecolor=hexaco_color, 
                  markeredgecolor=PRINT_COLORS['background'], markeredgewidth=2)
    # Заливка области
    ax.fill(angles, vals, color=hexaco_color, alpha=0.15)
    # Заголовок
    if title:
        plt.title(title, pad=25, fontsize=11, fontweight='bold', 
                 color=PRINT_COLORS['primary'])
    # Сохранение
    fig.savefig(out_path, format='png', bbox_inches='tight', 
                pad_inches=0.2, facecolor=PRINT_COLORS['background'], 
                edgecolor='none')
    plt.close(fig)
    return out_path
