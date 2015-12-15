from peewee import *
import time
from app.core.base_model import BaseModel


class Job(BaseModel):
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    title = CharField(db_column='TITLE', max_length=100)
    desc = CharField(db_column='DESC', max_length=500)
    createTime = DateTimeField(db_column='CREATE_TIME')
    def find_uuid(self, uuid):
        return self.get(Job.uuid == uuid)

    def delete_uuid(self):
        self.delete_instance()

    def to_dict(self):
        return {
            'title':self.title,
            'content':self.desc,
            'date':time.mktime(self.createTime.timetuple())*1000,
            'id':self.uuid
        }
    class Meta:
        db_table = 'WORKER_JOB'

