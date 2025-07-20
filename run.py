#!/usr/bin/env python3
import asyncio

from telegram_agent.app import App

if __name__ == "__main__":
    app = App("config.json", "secrets.json")
    asyncio.run(app.run())
