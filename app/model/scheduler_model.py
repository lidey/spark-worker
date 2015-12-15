from peewee import CharField, TextField, DateTimeField
import time
from app.core.base_model import BaseModel


class Scheduler(BaseModel):
    uuid = CharField(db_column='UUID', max_length='64', primary_key='true')
    name = CharField(db_column='NAME', max_length='128')
    cron = CharField(db_column='CRON', max_length='128')
    msg = TextField(db_column='MSG')
    created_time = DateTimeField(db_column='CREATED_TIME' ,null='false')

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'name': self.name,
            'cron': self.cron,
            'msg': self.msg,
            'created_time': time.mktime(self.created_time.timetuple()) * 1000,
        }

    def delete_uuid(self):
        self.delete_instance()

    class Meta:
        db_table = 'WORKER_SCHEDULER'
