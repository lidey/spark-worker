import time
from peewee import *
from app.core.base_model import BaseModel


class Script(BaseModel):
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    title = CharField(db_column='TITLE', max_length=100)
    script = CharField(db_column='SCRIPT', max_length=500)
    server_id = CharField(db_column='SERVER_ID', max_length=64)
    job_id = CharField(db_column='JOB_ID', max_length=64)
    createTime = DateTimeField(db_column='CREATE_TIME')

    def find_uuid(self, uuid):
        return self.get(Script.uuid == uuid)

    def delete_uuid(self):
        self.delete_instance()

    def to_dict(self):
        return {
            'title': self.title,
            'script': self.script,
            'date': time.mktime(self.createTime.timetuple())*1000,
            'id': self.uuid,
            'server_id': self.server_id,
            'job_id': self.job_id
        }
    class Meta:
        db_table = 'JOB_SCRIPT'

