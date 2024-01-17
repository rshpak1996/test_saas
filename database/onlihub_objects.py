#!/usr/bin/python
# -*- coding: utf-8 -*-
import database.psql as psql


class onliub_object():

    def __repr__(self):
        return repr(self.__object__)

    def __init__(self, tableName='', id=None, filter=None):
        self.id = id
        # self.id = filter
        self.__object__ = {}
        self.tableName = tableName
        if id:
            self.getByFilter({"id": id})
        elif filter:
            self.getByFilter(filter)

    def __setattr__(self, key, value):
        if key == 'id':
            self.__dict__[key] = value
        elif key == 'tableName':
            self.__dict__[key] = value
        elif key == '__object__':
            self.__dict__[key] = value
        else:
            self.__object__[key] = value

    def __getattr__(self, key):
        if key == 'id':
            return self.__dict__[key]
        elif key == 'tableName':
            return self.__dict__[key]
        elif key == '__object__':
            return self.__dict__[key]
        else:
            return self.__dict__.get('__object__').get(key)

    def isEmpty(self):
        return self.id is None

    def save(self, childQueryList=None, prepareOnly=False, returned='id'):

        query = {}
        for attr in self.__dict__.get('__object__'):
            value = self.__dict__.get('__object__').get(attr)
            if type(value) == list:
                continue
            psql.addQueryField(query=query, name=attr, value=value)

        if prepareOnly:
            if not (childQueryList.get(self.tableName)):
                childQueryList[self.tableName] = []
            childQueryList[self.tableName].append(query)
            return

        if self.isEmpty():
            SQL, par = psql.generateInsertRequest(query=query, tableName=self.tableName)
            res = psql.cur_execute_fetchone(SQL + ' returning id', par)
            self.id = res.id
        else:
            psql.addQueryField(query=query, name='id', value=self.id, isFilter=True)
            SQL, par = psql.generateUpdateRequest(query=query, tableName=self.tableName)
            res = psql.cur_execute(SQL, par)
            pass

    def getByFilter(self, filter):
        data = psql.getSqlData(tableName=self.tableName, fields='*', filter=filter, dotAccess=False)
        if data is None:
            raise SystemError
        if len(data) == 1:
            self.id = data[0].get('id')
            self.__object__ = data[0]
            del self.__object__['id']
        elif len(data) > 1:
            raise SystemError
        return self
        pass

