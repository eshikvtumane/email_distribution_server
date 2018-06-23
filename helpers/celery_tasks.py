from enum import Enum


class CeleryTasks(Enum):
    EMAIL_SENDER = 'emails.tasks.send_emails_task'
