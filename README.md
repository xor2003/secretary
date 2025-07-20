# Secretary

## Overview
A modular application that summarizes unread messages from various messengers (Telegram, Viber) using Gemini AI, sends summaries via Telegram notifications, and can create Google Calendar reminders.

## Features
- Supports Telegram and Viber messengers
- Uses Gemini AI for message summarization
- Configurable summarization prompts per chat
- Scheduled summary generation
- Google Calendar reminder integration
- Modular architecture for easy extension

## Architecture
```mermaid
graph TD
    subgraph Main App
        A[App] -->|coordinates| B[Messengers]
        A -->|uses| C[Analyzer]
        A -->|uses| D[Notifier]
        A -->|uses| E[Reminder]
    end

    subgraph Messengers
        B --> F[TelegramConnector]
        B --> G[ViberConnector]
    end

    subgraph Analyzer
        C --> H[GeminiAnalyzer]
    end

    subgraph Notifier
        D --> I[TelegramNotifier]
    end

    subgraph Reminder
        E --> J[GoogleCalendarReminder]
    end
```

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/telegram_agent.git
cd telegram_agent
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration
The application uses two configuration files:

1. `config.json` - Contains non-sensitive configuration
2. `secrets.json` - Contains sensitive credentials (keep this file private)

### Setup Steps:
1. Copy the example files:
```bash
cp config.example.json config.json
cp secrets.example.json secrets.json
```

2. Update `config.json` with your non-sensitive settings.

3. Update `secrets.json` with your sensitive credentials.

> Note: The application merges secrets with configuration at runtime.

## Usage
Run the application:
```bash
python run.py
```

## Extending
To add new messengers:
1. Create a new connector in `connectors/` implementing the Messenger interface
2. Add configuration section in `config.json`
3. Update App class to initialize your connector
## Deployment to Render.com

1. Create a new Web Service on Render.com
2. Connect your GitHub repository
3. Use the following settings:
   - Runtime: Python 3
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python run.py`
4. Set environment variables from secrets.json in the Render dashboard
5. Deploy


## License
MIT