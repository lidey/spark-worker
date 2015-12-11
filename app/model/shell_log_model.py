from peewee import *

from app.core.base_model import BaseModel


class ShellLog(BaseModel):
    uuid = CharField(db_column='UUID', max_length=64, primary_key=True)
    script_id = CharField(db_column='SCRIPT_ID', max_length=64)
    process_id = CharField(db_column='PROCESS_ID', max_length=64)
    log = TextField(db_column='LOG')
    status = IntegerField(db_column='STATUS')


    def find_uuid(self, uuid):
        return self.get(ShellLog.uuid == uuid)

    class Meta:
        db_table = 'SHELL_LOG'
