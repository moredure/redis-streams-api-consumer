class Config:
    def __init__(self, env: dict):
        self.redis_host = env.get('REDIS_HOST', 'localhost')
        self.redis_port = int(env.get('REDIS_PORT', 6379))
        self.port = int(env.get('PORT', '3000'))
        self.postgres_url = env.get('POSTRGRES_URL', 'postgres://postgres:postgres@localhost:5432?sslmode=disable')
        self.consumer_id = env.get('CONSUMER_ID', 'redis-streams-consumer-0')

    @property
    def address(self) -> tuple:
        return '', self.port
