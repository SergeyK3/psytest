#!/usr/bin/env python3
"""
Загрузка вашего персонального отчета в Google Drive
"""

from oauth_google_drive import upload_to_google_drive_oauth
import os

# Путь к вашему отчету
report_path = "docs/2025-10-03_18-35-27_Ким_Сергей_tg_8364.pdf"

print("🔄 Загружаем ваш персональный отчет в Google Drive...")

if os.path.exists(report_path):
    result = upload_to_google_drive_oauth(report_path, 'PsychTest Reports')
    if result:
        print(f"🎉 УСПЕХ!")
        print(f"📊 Ваш персональный отчет доступен по ссылке:")
        print(f"🔗 {result}")
        print()
        print("📋 Отчет содержит:")
        print("   📈 DISC анализ (D=7, I=1, S=0, C=0)")
        print("   🧠 HEXACO профиль личности")
        print("   💼 Soft Skills оценка")
        print("   📊 Детальные графики и диаграммы")
        print("   🤖 AI интерпретацию результатов")
    else:
        print("❌ Ошибка загрузки в Google Drive")
else:
    print(f"❌ Файл не найден: {report_path}")
    print("📁 Проверьте папку docs/")