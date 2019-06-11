#!/usr/bin/env python3
import sqlite3


class Sqlite3ORM:
    fields = []
    dbpath = ""
    dbtable = ""
    create = ""

    def __init__(self):
        # TODO What is this?
        raise NotImplementedError
    
    # if pk exists perform insert; else perform update
    def save(self):
        if self.pk is None:
            self._insert()
        else:
            self._update()

    @classmethod
    def _create_insert(cls):
        columnlist = ", ".join(cls.fields)
        qmarks = ", ".join("?" for val in cls.fields)
        SQL = """
                INSERT INTO {tablename} ({columnlist})
                VALUES({qmarks})
              """
        return SQL.format(tablename=cls.dbtable,
                          columnlist=columnlist,
                          qmarks=qmarks)
    
    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            curr = conn.cursor()
            SQL = self._create_insert()
            propvals = [getattr(self, propname) for propname in self.fields]

            curr.execute(SQL, propvals)
            #  .lastrowid returns row id of last modified row
            self.pk = curr.lastrowid

    @classmethod
    def _create_update(cls):
        columnlist = ", ".join(cls.fields)
        qmarks = ", ".join("?" for val in cls.fields)
        SQL = """
                UPDATE {tablename} 
                SET ({columnlist}={columnlist})
                WHERE pk = {qmarks}
            """
        return SQL.format(tablename=cls.dbtable,
                          columnlist=columnlist,
                          qmarks=qmarks)
        """
            TODO: IMPLEMENT THIS. Return a generic update SQL command
            like _create_insert did. You will want to be updating WHERE
            pk = ?
        """

    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            curr = conn.cursor()
        SQL = self.create_update()
        propvals = [getattr(self, propname) for propname in self.fields]
        curr.execute(SQL, propvals)
        """
            TODO: IMPLEMENT THIS. Execute the update statement. Remember 
            that you will also have to provide self.pk for that ? in addition
            to the field values.
        """