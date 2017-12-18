from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from redis import StrictRedis, RedisError
from rmon.common.rest import RestException


db = SQLAlchemy()


class Server(db.Model):
    __tablename__ = 'redis_server'
    __table_args__ = {'mysql_charset': 'utf8'}
    id = db.Column(db.Integer, primary_key=1)
    name = db.Column(db.String(64), unique=1)
    desc = db.Column(db.String(512))
    host = db.Column(db.String(15))
    port = db.Column(db.Integer, default=6379)
    password = db.Column(db.String(64))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Server(name={})>'.format(self.name)

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    @property
    def redis(self):
        return StrictRedis(host=self.host, port=self.port, password=self.password)

    def ping(self):
        try:
            return self.redis.ping()
        except RedisError:
            raise RestException(400, 'redis server {} can not connected'.format(self.host))

    def get_metrics(self):
        try:
            return self.redis.info()
        except RedisError:
            raise RestException(400, 'redis server {} can not connected'.format(self.host))



