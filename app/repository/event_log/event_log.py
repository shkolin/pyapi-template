from app.domain.event_log import EventLog
from app.repository.base import BaseRepository
from app.repository.event_log.interface import EventLogRepositoryInterface


class EventLogRepository(BaseRepository[EventLog], EventLogRepositoryInterface):
    pass
