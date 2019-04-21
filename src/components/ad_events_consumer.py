from threading import Event

from redis import Redis

from src.components.ad_events_repository import AdEventsRepository


class AdEventsConsumer:
    def __init__(self, id: str, conn: Redis, repository: AdEventsRepository, event: Event):
        self.id = id
        self.conn = conn
        self.repository = repository
        self.event = event

    def close(self):
        self.event.set()

    def consume_forever(self):
        while not self.event.is_set():
            result = self.conn.xreadgroup("clients", self.id, {'impressions': '0', 'clicks': '0'}, 200, 0)
            print(result)
            # self.repository.add_clicks()
            # self.repository.add_impressions()
