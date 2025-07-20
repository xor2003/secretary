from telegram_agent import App

if __name__ == "__main__":
    App("config.json", "secrets.json").run()