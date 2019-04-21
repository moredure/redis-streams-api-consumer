class Config:
    def __init__(self, env: dict):
        self.redis_host = env.get('REDIS_HOST', 'servers.microredis.com')
        self.redis_port = int(env.get('REDIS_PORT', 30026))
        self.redis_password = env.get('REDIS_PASSWORD', '137b7150-dfa4-4786-ac0f-d68c6f2d936e')
        self.redis_ssl_ca_certs = env.get('REDIS_SSL_CA_CERT', 'microredis_ca.pem')
        self.redis_ssl_certfile = env.get('REDIS_SSL_CERTTILE', 'microredis_user.crt')
        self.redis_ssl_keyfile = env.get('REDIS_SSL_KEYFILE', 'microredis_user_private.key')
        self.port = int(env.get('PORT', '3000'))
        self.postgres_url = env['POSTRGRES_URL']
        self.consumer_id = env.get('CONSUMER_ID', 'redis-streams-consumer-0')

    @property
    def address(self) -> tuple:
        return '', self.port
