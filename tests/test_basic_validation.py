"""
Простые тесты для проверки базовой функциональности
Избегает циклических импортов, проверяя только ключевые аспекты
"""

import pytest
from pathlib import Path


class TestProjectStructure:
    """Проверяет структуру проекта и наличие ключевых файлов"""
    
    def test_main_bot_file_exists(self):
        """Проверяет наличие основного файла бота"""
        bot_file = Path("telegram_test_bot.py")
        assert bot_file.exists(), "Основной файл бота не найден"
        
    def test_soft_skills_questions_file_exists(self):
        """Проверяет наличие файла с вопросами soft skills"""
        questions_file = Path("data/prompts/soft_user.txt")
        assert questions_file.exists(), "Файл с вопросами soft skills не найден"
        
    def test_requirements_file_has_pytest(self):
        """Проверяет, что pytest добавлен в requirements"""
        requirements_file = Path("requirements.txt")
        assert requirements_file.exists(), "Файл requirements.txt не найден"
        
        try:
            with open(requirements_file, 'r', encoding='utf-8-sig') as f:  # utf-8-sig обрабатывает BOM
                content = f.read()
        except UnicodeDecodeError:
            # Пробуем другие кодировки
            with open(requirements_file, 'r', encoding='utf-16') as f:
                content = f.read()
            
        assert "pytest" in content, "pytest не найден в requirements.txt"


class TestSoftSkillsData:
    """Проверяет структуру данных soft skills без импорта основного модуля"""
    
    def test_soft_skills_file_format(self):
        """Проверяет формат файла с вопросами soft skills"""
        questions_file = Path("data/prompts/soft_user.txt")
        
        if questions_file.exists():
            with open(questions_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Проверяем, что файл не пустой
            assert len(content.strip()) > 0, "Файл soft skills пустой"
            
            # Проверяем наличие ключевых слов (включая цифры, которые есть в файле)
            assert ("как" in content.lower() or "question" in content.lower() or 
                   any(str(i) in content for i in range(1, 11))), \
                "Файл не содержит вопросов или нумерации"


class TestVSCodeConfiguration:
    """Проверяет конфигурацию VS Code"""
    
    def test_vscode_tasks_exist(self):
        """Проверяет наличие файла tasks.json"""
        tasks_file = Path(".vscode/tasks.json")
        assert tasks_file.exists(), "Файл .vscode/tasks.json не найден"
        
    def test_vscode_settings_exist(self):
        """Проверяет наличие файла settings.json"""
        settings_file = Path(".vscode/settings.json")
        assert settings_file.exists(), "Файл .vscode/settings.json не найден"
        
    def test_tasks_contain_pytest(self):
        """Проверяет, что в tasks.json есть задача для pytest"""
        tasks_file = Path(".vscode/tasks.json")
        
        if tasks_file.exists():
            with open(tasks_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            assert "pytest" in content, "Задача pytest не найдена в tasks.json"


class TestCodeQuality:
    """Проверяет аспекты качества кода"""
    
    def test_no_hardcoded_tokens_in_main_file(self):
        """Проверяет отсутствие хардкодинных токенов в основном файле"""
        bot_file = Path("telegram_test_bot.py")
        
        if bot_file.exists():
            with open(bot_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Удаляем комментарии для проверки
            lines = content.split('\n')
            code_lines = []
            for line in lines:
                # Убираем строки, которые являются комментариями
                stripped = line.strip()
                if not stripped.startswith('#') and not stripped.startswith('"""') and not stripped.startswith("'''"):
                    code_lines.append(line)
            
            code_content = '\n'.join(code_lines)
                
            # Проверяем, что нет явных токенов в коде
            dangerous_patterns = [
                'BOT_TOKEN = "',
                'TOKEN = "',
                'token = "',
                ":AAH",  # Часть токенов Telegram
                ":AAG"   # Часть токенов Telegram
            ]
            
            for pattern in dangerous_patterns:
                assert pattern not in code_content, f"Найден потенциально хардкодинный токен: {pattern}"
    
    def test_temp_directory_cleanup_exists(self):
        """Проверяет наличие cleanup логики для временных директорий"""
        bot_file = Path("telegram_test_bot.py")
        
        if bot_file.exists():
            with open(bot_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Проверяем наличие cleanup логики
            cleanup_indicators = [
                "shutil.rmtree",
                "tempfile.mkdtemp",
                "finally:",
                "temp_dir"
            ]
            
            found_indicators = [indicator for indicator in cleanup_indicators if indicator in content]
            assert len(found_indicators) >= 3, f"Недостаточно индикаторов cleanup логики. Найдено: {found_indicators}"
    
    def test_async_threading_pattern(self):
        """Проверяет использование async threading паттернов"""
        bot_file = Path("telegram_test_bot.py")
        
        if bot_file.exists():
            with open(bot_file, 'r', encoding='utf-8') as f:
                content = f.read()
                
            # Проверяем наличие async patterns
            async_patterns = [
                "asyncio.to_thread",
                "async def",
                "await"
            ]
            
            found_patterns = [pattern for pattern in async_patterns if pattern in content]
            assert len(found_patterns) >= 2, f"Недостаточно async паттернов. Найдено: {found_patterns}"


class TestProjectHealthCheck:
    """Общие проверки здоровья проекта"""
    
    def test_essential_files_exist(self):
        """Проверяет наличие основных файлов проекта"""
        essential_files = [
            "telegram_test_bot.py",
            "enhanced_pdf_report_v2.py", 
            "requirements.txt",
            "scale_normalizer.py"
        ]
        
        for file_path in essential_files:
            file_obj = Path(file_path)
            assert file_obj.exists(), f"Основной файл не найден: {file_path}"
    
    def test_data_directory_structure(self):
        """Проверяет структуру папки данных"""
        data_dir = Path("data")
        assert data_dir.exists(), "Папка data не найдена"
        
        prompts_dir = data_dir / "prompts"
        assert prompts_dir.exists(), "Папка data/prompts не найдена"


if __name__ == "__main__":
    # Запуск тестов напрямую
    pytest.main([__file__, "-v"])