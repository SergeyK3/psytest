#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест подключения к Telegram API
"""

import asyncio
from telegram import Bot

async def test_bot():
    """Тестирует подключение к боту"""
    try:
        bot = Bot('REDACTED_TOKEN')
        me = await bot.get_me()
        print(f"✅ Бот работает!")
        print(f"🤖 Имя: {me.first_name}")
        print(f"📛 Username: @{me.username}")
        print(f"🆔 ID: {me.id}")
        return True
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_bot())