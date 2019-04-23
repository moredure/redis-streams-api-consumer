from os import environ
from signal import signal, SIGTERM, SIGINT
from threading import Event
from threading import Thread

from psycopg2 import connect
from redis import Redis

from src.components.ad_events_consumer import AdEventsConsumer
from src.components.ad_events_repository import AdEventsRepository
from src.components.config import Config

if __name__ == '__main__':
    config = Config(environ)
    redis_conn = Redis(host=config.redis_host,
                       password=config.redis_password,
                       port=config.redis_port,
                       ssl=True,
                       ssl_ca_certs=config.redis_ssl_ca_certs,
                       ssl_certfile=config.redis_ssl_certfile,
                       ssl_keyfile=config.redis_ssl_keyfile)
    postgres_conn = connect(config.postgres_url)
    ad_events_repository = AdEventsRepository(postgres_conn)
    consumer = AdEventsConsumer(config.consumer_id, redis_conn, ad_events_repository, Event())
    server_thread = Thread(target=consumer.consume_forever)
    server_thread.start()
    signal(SIGTERM, consumer.close)
    signal(SIGINT, consumer.close)
    server_thread.join()
