#!/usr/bin/python
# coding=utf-8
#
# File Name: database_handler.py
# File Author: 姚丰利(lidey) 
# File Created Date: 2015-12-28 12:54
import uuid
import tornado.web

from app.connect.connect_manager import DatabaseConnect
from app.core.base_exception import ConnectException
from app.core.base_handler import BaseHandler
from app.model.database_model import Database, Folder, Table, Column, Category, Model, ModelTable, ModelIndex


class DatabaseHandler(BaseHandler):
    def data_received(self, chunk):
        pass

    @tornado.web.authenticated
    def post(self, url_first='', url_second=''):
        if url_first == '':
            return
        if url_first == 'save':
            database = Database()
            database.uuid = self.args.get('uuid')
            database.title = self.args.get('title')
            database.description = self.args.get('description')
            database.hostname = self.args.get('hostname')
            database.port = self.args.get('port')
            database.type = self.args.get('type')
            database.name = self.args.get('name')
            database.username = self.args.get('username')
            database.password = self.args.get('password')
            return self.save_database(database)
        if url_first == 'folder' and url_second == 'save':
            folder = Folder()
            folder.uuid = self.args.get('uuid')
            folder.db_uuid = self.args.get('db_uuid')
            folder.title = self.args.get('title')
            folder.description = self.args.get('description')
            return self.save_folder(folder)
        if url_second == 'import_tables':
            return self.import_tables(url_first)
        if url_first == 'category' and url_second == 'save':
            category = Category()
            category.uuid = self.args.get('uuid')
            category.p_uuid = self.args.get('p_uuid')
            category.title = self.args.get('title')
            category.description = self.args.get('description')
            return self.save_category(category)
        if url_first == 'model' and url_second == 'save':
            model = Model()
            model.uuid = self.args.get('uuid')
            model.c_uuid = self.args.get('c_uuid')
            model.d_uuid = self.args.get('d_uuid')
            model.title = self.args.get('title')
            model.type = self.args.get('type')
            model.description = self.args.get('description')
            return self.save_model(model)
        if url_first == 'modelTable' and url_second == 'import':
            model_table = ModelTable()
            model_table.m_uuid = self.args.get('m_uuid')
            model_table.t_uuids = self.args.get('t_uuids')
            return self.import_model_table(model_table)
        if url_first == 'index' and url_second == 'save':
            model_index = ModelIndex()
            model_index.m_uuid = self.args.get('m_uuid')
            model_index.c_uuid = self.args.get('c_uuid')
            return self.save_index(model_index)

    @tornado.web.authenticated
    def get(self, url_first='', url_second=''):
        if url_first == '':
            return
        if url_first == 'tree':
            return self.tree()
        if url_first == 'database' and url_second == 'list':
            return self.database_list()
        if url_first == 'test':
            return self.test()
        if url_first == 'remove':
            return self.remove_database()
        if url_first == 'folder' and url_second == 'remove':
            return self.remove_folder()
        if url_second == 'folder_list':
            return self.folder_list(url_first)
        if url_second == 'table_names':
            return self.table_names(url_first)
        if url_second == 'table_list':
            return self.table_list(url_first)
        if url_first == 'table' and url_second == 'remove':
            return self.remove_table()
        if url_second == 'column_list':
            return self.column_list(url_first)
        if url_second == 'reload':
            return self.column_reload(url_first)
        if url_first == 'column' and url_second == 'remove':
            return self.remove_column()
        if url_first == 'model' and url_second == 'tree':
            return self.model_tree()
        if url_first == 'category' and url_second == 'remove':
            return self.remove_category()
        if url_second == 'model_list':
            return self.model_list(url_first)
        if url_first == 'model' and url_second == 'remove':
            return self.remove_model()
        if url_second == 'model':
            return self.model_info(url_first)
        if url_first == 'model' and url_second == 'table_tree':
            return self.table_tree()
        if url_second == 'index_list':
            return self.index_list(url_first)
        if url_first == 'index' and url_second == 'remove':
            return self.remove_index()

    def tree(self):
        """
        查询数据库链接及包含的目录结构
        :return: 树形数据集
        """
        tree = []
        for database in Database.select():
            tree.append(database.to_tree())
        self.write({'tree': tree})

    def database_list(self):
        """
        查询数据库链接列表
        :return: 数据库链接列表
        """
        databases = []
        for database in Database.select():
            databases.append(database.to_dict())
        self.write({'databases': databases})

    def folder_list(self, d_uuid):
        """
        查询数据库链接目录列表
        :param d_uuid: 数据库UUID
        :return: 目录列表
        """
        folders = []
        for folder in Folder.select().join(Database).where(Database.uuid, d_uuid):
            folders.append(folder.to_dict())
        self.write({'folders': folders})

    def table_names(self, uuid):
        """
        根据数据库链接UUID查询数据库包含的数据表
        :param uuid: 数据库链接UUID
        :return:数据表列表
        """
        self.write({'table_names': DatabaseConnect().get_tables(uuid, self.get_argument('name'))})

    def test(self):
        """
        测试数据库链接状态
        :return: 测试结果
        """
        try:
            DatabaseConnect().test(self.get_argument('uuid'))
            self.write({'success': True, 'content': '数据库测试成功'})
        except ConnectException, e:
            self.write({'success': False, 'content': '数据库测试失败,异常信息:<br/> {0}'.format(e.message)})

    def save_database(self, database):
        """
        保存数据库链接
        :param database:数据库链接配置信息
        :return: 处理结果
        """
        if database.uuid is None:
            database.uuid = str(uuid.uuid1())
            database.save(force_insert=True)
        else:
            database.save()
        self.write({'success': True, 'content': '数据库链接保存成功.'})

    def remove_database(self):
        """
        删除数据链接
        :return: 处理结果
        """
        Database.get(Database.uuid == self.get_argument('uuid')).delete_instance()
        self.write({'success': True, 'content': '数据库链接删除成功.'})

    def save_folder(self, folder):
        """
        保存数据分类目录
        :param folder:数据分类目录信息
        :return: 处理结果
        """
        if folder.uuid is None:
            folder.uuid = str(uuid.uuid1())
            folder.database = Database.get(Database.uuid == folder.db_uuid)
            folder.save(force_insert=True)
        else:
            folder.save()
        self.write({'success': True, 'content': '目录保存成功.'})

    def remove_folder(self):
        """
        删除数据分类目录
        :return: 处理结果
        """
        Folder.get(Folder.uuid == self.get_argument('uuid')).delete_instance()
        self.write({'success': True, 'content': '目录删除成功.'})

    def import_tables(self, db_uuid):
        """
        导入数据表,已导入的数据表将不再重新导入.
        :param db_uuid: 所属数据库UUID
        :return: 处理结果
        """
        names = self.args.get('names')
        folder_uuid = self.args.get('folder_uuid')
        for name in names:
            if folder_uuid is not None:
                folder = Folder.get(Folder.uuid == folder_uuid)
                table = Table.select().join(Database).switch(Table).join(Folder).where(Database.uuid == db_uuid,
                                                                                       Folder.uuid == folder_uuid,
                                                                                       Table.name == name)
            else:
                folder = None
                table = Table.select().join(Database).where(Database.uuid == db_uuid,
                                                            Table.folder.is_null(True),
                                                            Table.name == name)
            try:
                table.get()
            except Table.DoesNotExist:
                table = Table()
                table.uuid = str(uuid.uuid1())
                table.name = name
                table.database = Database.get(Database.uuid == db_uuid)
                table.folder = folder
                table.type = 'TABLE'
                table.save(force_insert=True)
                self.init_columns(table)
        self.write({'success': True, 'content': '数据表导入成功.'})

    def init_columns(self, table):
        """
        初始化数据表结构信息
        :param database: 数据库链接信息
        :param table: 数据表信息
        :return: 无
        """
        database = table.database
        Column.delete().where(Column.table == table).execute()
        for col in DatabaseConnect().get_columns(database.uuid, table.name):
            column = Column()
            column.uuid = str(uuid.uuid1())
            column.database = database
            column.table = table
            column.field = col['field']
            column.key = col['key']
            column.type = col['type']
            column.save(force_insert=True)

    def column_reload(self, t_uuid):
        """
        重新加载数据表结构
        :param t_uuid: 数据表UUID
        :return: 处理结果
        """
        self.init_columns(Table.get(Table.uuid == t_uuid))
        self.write({'success': True, 'content': '数据表结构更新成功.'})

    def table_list(self, db_uuid):
        """
        获取数据分类目录下的数据表
        :param db_uuid: 数据库UUID
        :return: 数据表列表
        """
        tables = []
        folder_uuid = self.get_argument('folder_uuid')
        if folder_uuid:
            query = Table.select().join(Database).switch(Table).join(Folder).where(Database.uuid == db_uuid,
                                                                                   Folder.uuid == folder_uuid)
        else:
            query = Table.select().join(Database).where(Database.uuid == db_uuid, Table.folder.is_null(True))
        for table in query:
            tables.append(table.to_dict())
        self.write({'tables': tables})

    def remove_table(self):
        """
        删除数据表
        :return: 处理结果
        """
        Table.get(Table.uuid == self.get_argument('uuid')).delete_instance()
        self.write({'success': True, 'content': '数据表删除成功.'})

    def column_list(self, t_uuid):
        """
        获取数据表结构信息
        :param t_uuid: 数据表UUID
        :return: 字段列表
        """
        columns = []
        for column in Column.select().join(Table).where(Table.uuid == t_uuid):
            columns.append(column.to_dict())
        self.write({'columns': columns})

    def remove_column(self):
        """
        删除字段
        :return: 处理结果
        """
        Column.get(Column.uuid == self.get_argument('uuid')).delete_instance()
        self.write({'success': True, 'content': '字段删除成功.'})

    def model_tree(self):
        """
        获取数据模型分类树
        :return: 模型分类树
        """
        tree = []
        for group in Category.select().where(Category.parent.is_null(True)):
            tree.append(group.to_tree())
        self.write({'tree': tree})

    def save_category(self, category):
        """
        保存模型分类信息
        :param category: 分类信息
        :return: 处理结果
        """
        if category.uuid is None:
            category.uuid = str(uuid.uuid1())
            if category.p_uuid:
                category.parent = Category.get(Category.uuid == category.p_uuid)
            category.save(force_insert=True)
        else:
            category.save()
        self.write({'success': True, 'content': '目录保存成功.'})

    def remove_category(self):
        """
        删除目录
        :return: 处理结果
        """
        Category.get(Category.uuid == self.get_argument('uuid')).delete_instance()
        self.write({'success': True, 'content': '目录删除成功.'})

    def model_list(self, c_uuid):
        """
        获取数据模型列表
        :param c_uuid: 类型UUID
        :return: 数据模型列表
        """
        models = []
        for model in Model.select().join(Category).where(Category.uuid == c_uuid):
            models.append(model.to_dict())
        self.write({'models': models})

    def save_model(self, model):
        """
        保存数据模型信息
        :param category: 分类信息
        :return: 处理结果
        """
        if model.uuid is None:
            model.uuid = str(uuid.uuid1())
            if model.c_uuid:
                model.category = Category.get(Category.uuid == model.c_uuid)
            if model.d_uuid:
                model.database = Database.get(Database.uuid == model.d_uuid)
            model.save(force_insert=True)
        else:
            model.save()
        self.write({'success': True, 'content': '数据模型信息保存成功.'})

    def remove_model(self):
        """
        删除模型
        :return: 处理结果
        """
        Model.get(Model.uuid == self.get_argument('uuid')).delete_instance()
        self.write({'success': True, 'content': '删除模型成功.'})

    def model_info(self, uuid):
        """
        获取数据模型信息
        :param uuid: 模型UUID
        :return: 数据模型信息JSON
        """
        self.write({'model': Model.get(Model.uuid == uuid).to_dict()})

    def import_model_table(self, model_table):
        """
        保存模型与表关联
        :param model_table: 模型与表关联
        :return: 处理结果
        """
        for t_uuid in model_table.t_uuids:
            try:
                ModelTable.select().join(Table).switch(ModelTable).join(Model).where(Model.uuid == model_table.m_uuid,
                                                                                     Table.uuid == t_uuid).get()
            except ModelTable.DoesNotExist:
                tmp = ModelTable()
                tmp.uuid = str(uuid.uuid1())
                if model_table.m_uuid:
                    tmp.model = Model.get(Model.uuid == model_table.m_uuid)
                if t_uuid:
                    tmp.table = Table.get(Table.uuid == t_uuid)
                tmp.save(force_insert=True)
        self.write({'success': True, 'content': '数据表导入成功.'})

    def table_tree(self):
        """
        查询数据库链接及包含的目录结构
        :return: 树形数据集
        """
        tree = []
        for modelTable in ModelTable.select().join(Model).where(Model.uuid == self.get_argument('m_uuid')):
            tree.append(modelTable.to_tree())
        self.write({'tree': tree})

    def save_index(self, model_index):
        """
        保存模型与字段关联
        :param model_index: 模型与字段关联
        :return: 处理结果
        """
        try:
            model_index = ModelIndex.select().join(Column).switch(ModelIndex).join(Model).where(
                    Column.uuid == model_index.c_uuid,
                    Model.uuid == model_index.m_uuid).get()
            self.write({'success': False, 'content': '指标已存在.'})
        except ModelIndex.DoesNotExist:
            model_index.uuid = str(uuid.uuid1())
            if model_index.m_uuid:
                model_index.model = Model.get(Model.uuid == model_index.m_uuid)
            if model_index.c_uuid:
                model_index.column = Column.get(Column.uuid == model_index.c_uuid)
            model_index.save(force_insert=True)
            self.write({'success': True, 'content': '指标保存成功.', 'index': model_index.to_dict()})

    def index_list(self, m_uuid):
        """
        获取数据模型指标列表
        :param m_uuid: 类型UUID
        :return: 指标列表
        """
        indexes = []
        for index in ModelIndex.select().join(Model).where(Model.uuid == m_uuid):
            indexes.append(index.to_dict())
        self.write({'indexes': indexes})

    def remove_index(self):
        """
        删除模型
        :return: 处理结果
        """
        ModelIndex.get(ModelIndex.uuid == self.get_argument('uuid')).delete_instance()
        self.write({'success': True, 'content': '删除指标成功.'})
