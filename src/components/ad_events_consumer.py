from datetime import datetime
from threading import Event

from redis import Redis

from src.components.ad_events_repository import AdEventsRepository


class AdEventsConsumer:
    def __init__(self, uid: str, conn: Redis, repository: AdEventsRepository, event: Event):
        self.uid = uid
        self.conn = conn
        self.repository = repository
        self.event = event

    def close(self):
        self.event.set()

    def consume_impressions(self, logs: list) -> None:
        impressions = [
            (
                str(log.get(b'uid', b''), 'utf-8'),
                str(log.get(b'user_agent', b''), 'utf-8'),
                datetime.utcfromtimestamp(int(str(sid, 'utf-8').split('-')[0]))
            )
            for (sid, log) in logs
        ]
        self.repository.add_impressions(impressions)
        self.conn.xack('impressions', 'clients', [id for (id, log) in logs])

    def consume_clicks(self, logs: list):
        clicks = [
            (
                str(log.get(b'uid', b''), 'utf-8'),
                str(log.get(b'user_agent', b''), 'utf-8'),
                str(log.get(b'screen_x', b''), 'utf-8'),
                str(log.get(b'screen_y', b''), 'utf-8'),
                datetime.utcfromtimestamp(int(str(sid, 'utf-8').split('-')[0]))
            )
            for (sid, log) in logs
        ]
        self.repository.add_clicks(clicks)
        self.conn.xack('clicks', 'clients', [id for (id, log) in logs])

    def consume_forever(self):
        while not self.event.is_set():
            for stream, logs in self.conn.xreadgroup("clients", self.uid, {'impressions': '0', 'clicks': '0'}, 200, 0):
                # [[b'impressions', [(b'1-0', {b'x': b'y', b'a': b'b'})]]]
                if stream == b'impressions':
                    self.consume_impressions(logs)
                elif stream == b'clicks':
                    self.consume_clicks(logs)
