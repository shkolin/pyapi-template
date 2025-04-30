from app.mapping import admin
from app.mapping import event_log
from app.mapping import user


def perform_mapping() -> None:
    admin.perform_mapping()
    user.perform_mapping()
    event_log.perform_mapping()
