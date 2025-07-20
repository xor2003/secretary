from ..interfaces import Reminder


class GoogleCalendarReminder(Reminder):
    def __init__(self, service_account_path, calendar_id):
        self.service_account_path = service_account_path
        self.calendar_id = calendar_id

    def create_reminder(self, summary, start_dt):
        print(f"Reminder created for '{summary}' at {start_dt}")
        # аутентификация по примеру на :contentReference[oaicite:17]{index=17}

        service.events().insert(
            calendarId="primary",
            body={
                "summary": "Тема: XYZ",
                "start": {"dateTime": start_dt, "timeZone": "Europe/Belgrade"},
                "end": {"dateTime": end_dt, "timeZone": "Europe/Belgrade"},
                "reminders": {
                    "useDefault": False,
                    "overrides": [{"method": "popup", "minutes": 30}],
                },
            },
        ).execute()
