from os import environ
from signal import signal, SIGTERM, SIGINT
from threading import Thread

import psycopg2
from redis import Redis

from src.components.config import Config

if __name__ == '__main__':
    config = Config(environ)
    postgres_conn = psycopg2.connect(config.postgres_url)

    redis_conn = Redis(host=config.redis_host,
                       password=config.redis_password,
                       port=config.redis_port,
                       ssl=True,
                       ssl_ca_certs=config.redis_ssl_ca_certs,
                       ssl_certfile=config.redis_ssl_certfile,
                       ssl_keyfile=config.redis_ssl_keyfile)

    redis_conn.xgroup_create()
    ad_events_repository = AdEventsRepository(postgres_conn)
    consumer = AdEventsConsumer(redis_conn, ad_events_repository)

    server_thread = Thread(target=consumer.consume_forever)
    server_thread.start()
    signal(SIGTERM, consumer.die)
    signal(SIGINT, consumer.die)
    server_thread.join()
