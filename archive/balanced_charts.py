#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Улучшенная система создания сбалансированных диаграмм
Решает проблемы с высокими соотношениями и крайними значениями
"""
from math import pi, log, sqrt
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from typing import List, Tuple

# Улучшенная цветовая палитра для более сбалансированного вида
BALANCED_COLORS = {
    'primary': '#2C3E50',      # Глубокий синий-серый
    'secondary': '#34495E',     # Средний серый
    'light': '#BDC3C7',        # Светло-серый для сетки
    'accent': '#3498DB',        # Яркий синий для акцентов
    'fill': '#ECF0F1',          # Очень светлый для заливки
    'background': '#FFFFFF'     # Белый фон
}

class BalancedChartGenerator:
    """Генератор сбалансированных диаграмм"""
    
    @staticmethod
    def normalize_values(values: List[float], method: str = "sqrt") -> Tuple[List[float], float, str]:
        """
        Нормализует значения для лучшего баланса диаграммы
        
        Args:
            values: Исходные значения
            method: Метод нормализации ('sqrt', 'log', 'minmax', 'adaptive')
            
        Returns:
            Нормализованные значения, новый максимум, описание метода
        """
        max_val = max(values)
        min_val = min(values)
        ratio = max_val / min_val if min_val > 0 else float('inf')
        
        if ratio <= 2.0:
            # Хорошо сбалансированные данные - не нормализуем
            return values, max_val, "без_нормализации"
        
        elif method == "sqrt" and ratio > 3.0:
            # Квадратный корень для средних дисбалансов
            normalized = [sqrt(v) for v in values]
            return normalized, max(normalized), "квадратный_корень"
        
        elif method == "log" and ratio > 5.0:
            # Логарифм для сильных дисбалансов
            # Добавляем 1 чтобы избежать log(0)
            normalized = [log(v + 1, 2) for v in values]
            return normalized, max(normalized), "логарифм"
        
        elif method == "adaptive":
            # Адаптивная нормализация
            if ratio > 8.0:
                # Очень высокий дисбаланс - используем логарифм
                normalized = [log(v + 1, 2) for v in values]
                return normalized, max(normalized), "адаптивный_логарифм"
            elif ratio > 4.0:
                # Средний дисбаланс - квадратный корень
                normalized = [sqrt(v) for v in values]
                return normalized, max(normalized), "адаптивный_корень"
            else:
                # Небольшой дисбаланс - мягкая нормализация
                mean_val = sum(values) / len(values)
                normalized = [v * 0.7 + mean_val * 0.3 for v in values]
                return normalized, max(normalized), "адаптивная_мягкая"
        
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
        return values, max_val, "исходные"
    
    @staticmethod
    def create_balanced_radar(labels: List[str], values: List[float], 
                             out_path: Path, title: str = "",
                             normalize_method: str = "adaptive") -> Tuple[Path, str]:
        """Создает сбалансированную радарную диаграмму"""
        
        # Нормализуем значения
        norm_values, max_norm, method_used = BalancedChartGenerator.normalize_values(
            values, normalize_method
        )
        
        # Настройка matplotlib
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
        vals = list(norm_values) + norm_values[:1]
        
        # Создание фигуры
        fig = plt.figure(figsize=(5, 5), facecolor=BALANCED_COLORS['background'])
        ax = plt.subplot(111, polar=True)
        
        # Настройка полярных осей
        ax.set_theta_offset(pi / 2)
        ax.set_theta_direction(-1)
        
        # Установка меток осей
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(labels, fontsize=10, color=BALANCED_COLORS['primary'])
        
        # Улучшенная радиальная сетка
        # Используем круглое число делений на основе максимального значения
        if max_norm <= 4:
            tick_step = 1
        elif max_norm <= 8:
            tick_step = 2
        else:
            tick_step = max(1, int(max_norm / 4))
            
        ax.set_ylim(0, max_norm * 1.1)
        ticks = np.arange(0, max_norm * 1.1, tick_step)
        ax.set_yticks(ticks)
        ax.set_yticklabels([f'{t:.1f}' for t in ticks], 
                          fontsize=8, color=BALANCED_COLORS['secondary'])
        
        # Улучшенная стилизация сетки
        ax.grid(True, color=BALANCED_COLORS['light'], linewidth=0.6, alpha=0.8)
        ax.set_facecolor(BALANCED_COLORS['background'])
        
        # Рисование диаграммы с улучшенным стилем
        line = ax.plot(angles, vals, color=BALANCED_COLORS['accent'], linewidth=2.5, 
                      marker='o', markersize=6, markerfacecolor=BALANCED_COLORS['accent'], 
                      markeredgecolor=BALANCED_COLORS['background'], markeredgewidth=2)
        
        # Заливка области с градиентом (имитация)
        ax.fill(angles, vals, color=BALANCED_COLORS['accent'], alpha=0.15)
        
        # Заголовок с информацией о нормализации
        title_text = title
        if method_used != "без_нормализации" and method_used != "исходные":
            title_text += f" (норм: {method_used})"
            
        if title_text:
            plt.title(title_text, pad=25, fontsize=11, fontweight='bold', 
                     color=BALANCED_COLORS['primary'])
        
        # Сохранение
        fig.savefig(out_path, format='png', bbox_inches='tight', 
                    pad_inches=0.15, facecolor=BALANCED_COLORS['background'], 
                    edgecolor='none')
        plt.close(fig)
        
        return out_path, method_used
    
    @staticmethod
    def create_balanced_bar_chart(labels: List[str], values: List[float],
                                 out_path: Path, title: str = "",
                                 normalize_method: str = "adaptive",
                                 horizontal: bool = False) -> Tuple[Path, str]:
        """Создает сбалансированную столбчатую диаграмму"""
        
        # Нормализуем значения
        norm_values, max_norm, method_used = BalancedChartGenerator.normalize_values(
            values, normalize_method
        )
        
        # Настройка matplotlib
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
            fig, ax = plt.subplots(figsize=(7, 5), facecolor=BALANCED_COLORS['background'])
        else:
            fig, ax = plt.subplots(figsize=(8, 6), facecolor=BALANCED_COLORS['background'])
        
        if horizontal:
            bars = ax.barh(labels, norm_values, color=BALANCED_COLORS['accent'], 
                          edgecolor=BALANCED_COLORS['background'], linewidth=1.5)
            ax.set_xlim(0, max_norm * 1.15)
            ax.set_xlabel('Значение', fontsize=11, color=BALANCED_COLORS['primary'])
            
            # Добавление значений на столбцы
            for i, (bar, value, orig_value) in enumerate(zip(bars, norm_values, values)):
                text = f'{orig_value:.1f}'
                if method_used not in ["без_нормализации", "исходные"]:
                    text += f' ({value:.1f})'
                ax.text(value + max_norm*0.02, bar.get_y() + bar.get_height()/2, 
                       text, va='center', ha='left', 
                       fontsize=9, color=BALANCED_COLORS['primary'])
        else:
            bars = ax.bar(labels, norm_values, color=BALANCED_COLORS['accent'], 
                         edgecolor=BALANCED_COLORS['background'], linewidth=1.5)
            ax.set_ylim(0, max_norm * 1.2)
            ax.set_ylabel('Значение', fontsize=11, color=BALANCED_COLORS['primary'])
            
            # Поворот меток для лучшей читаемости
            ax.tick_params(axis='x', rotation=0, labelsize=10, pad=8)
            
            # Добавление значений на столбцы
            for bar, value, orig_value in zip(bars, norm_values, values):
                text = f'{orig_value:.1f}'
                if method_used not in ["без_нормализации", "исходные"]:
                    text += f'\n({value:.1f})'
                ax.text(bar.get_x() + bar.get_width()/2, value + max_norm*0.02, 
                       text, ha='center', va='bottom', 
                       fontsize=9, color=BALANCED_COLORS['primary'])
        
        # Улучшенная стилизация
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(BALANCED_COLORS['secondary'])
        ax.spines['bottom'].set_color(BALANCED_COLORS['secondary'])
        ax.tick_params(colors=BALANCED_COLORS['secondary'])
        ax.set_facecolor(BALANCED_COLORS['background'])
        
        # Улучшенная сетка
        ax.grid(True, alpha=0.4, color=BALANCED_COLORS['light'], linewidth=0.6)
        ax.set_axisbelow(True)
        
        # Заголовок с информацией о нормализации
        title_text = title
        if method_used not in ["без_нормализации", "исходные"]:
            title_text += f" (нормализация: {method_used})"
            
        if title_text:
            ax.set_title(title_text, fontsize=12, fontweight='bold', 
                        color=BALANCED_COLORS['primary'], pad=20)
        
        # Настройка размещения
        try:
            plt.tight_layout(pad=1.5)
        except:
            plt.subplots_adjust(bottom=0.15, left=0.12, right=0.95, top=0.9)
        
        # Сохранение
        fig.savefig(out_path, format='png', bbox_inches='tight', 
                    pad_inches=0.25, facecolor=BALANCED_COLORS['background'], 
                    edgecolor='none')
        plt.close(fig)
        
        return out_path, method_used

def test_balanced_charts():
    """Тестируем улучшенные сбалансированные диаграммы"""
    print("🎨 ТЕСТИРОВАНИЕ СБАЛАНСИРОВАННЫХ ДИАГРАММ")
    print("=" * 60)
    
    # Создаем тестовую папку
    test_dir = Path("test_balanced_charts")
    test_dir.mkdir(exist_ok=True)
    
    generator = BalancedChartGenerator()
    
    # Тестовые случаи
    test_cases = [
        {
            "name": "PAEI - Проблемный (A=10)",
            "labels": ["P", "A", "E", "I"],
            "values": [1.0, 10.0, 1.0, 1.0],
            "methods": ["adaptive", "sqrt", "log", "minmax"]
        },
        {
            "name": "DISC - Проблемный (D=7.8)", 
            "labels": ["D", "I", "S", "C"],
            "values": [7.8, 1.0, 3.2, 1.0],
            "methods": ["adaptive", "sqrt", "minmax"]
        },
        {
            "name": "Сбалансированный профиль",
            "labels": ["A", "B", "C", "D"],
            "values": [6.0, 7.0, 5.0, 6.0],
            "methods": ["adaptive"]
        }
    ]
    
    results = []
    
    for case in test_cases:
        print(f"\n📊 Тестирование: {case['name']}")
        print(f"Исходные значения: {case['values']}")
        
        for method in case['methods']:
            # Радарная диаграмма
            radar_path = test_dir / f"balanced_radar_{len(results)+1}_{method}.png"
            radar_path, radar_method = generator.create_balanced_radar(
                case['labels'], case['values'], radar_path,
                title=f"{case['name']} - Радар", normalize_method=method
            )
            
            # Столбчатая диаграмма
            bar_path = test_dir / f"balanced_bar_{len(results)+1}_{method}.png"
            bar_path, bar_method = generator.create_balanced_bar_chart(
                case['labels'], case['values'], bar_path,
                title=f"{case['name']} - Столбцы", normalize_method=method
            )
            
            print(f"  ✅ {method}: {radar_method} | Файлы: {radar_path.name}, {bar_path.name}")
            
            results.append({
                "case": case['name'],
                "method": method,
                "radar": radar_path,
                "bar": bar_path,
                "normalization": radar_method
            })
    
    print(f"\n🎉 Создано {len(results)} комплектов диаграмм в папке: {test_dir}")
    print("\nСравните с исходными диаграммами - должны быть более сбалансированными!")
    
    return results, test_dir

if __name__ == "__main__":
    print("🚀 СИСТЕМА СОЗДАНИЯ СБАЛАНСИРОВАННЫХ ДИАГРАММ")
    print("=" * 70)
    
    try:
        results, test_dir = test_balanced_charts()
        
        print(f"\n💡 РЕКОМЕНДАЦИИ:")
        print("1. Используйте 'adaptive' метод для автоматического выбора")
        print("2. Для сильных дисбалансов (>8:1) применяется логарифм")
        print("3. Для средних дисбалансов (4-8:1) применяется квадратный корень")
        print("4. Сбалансированные данные остаются без изменений")
        
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        import traceback
        traceback.print_exc()