#!/usr/bin/env python3
import sqlite3


class Sqlite3ORM:
    fields = []
    dbpath = ""
    dbtable = ""
    create = ""

    def __init__(self):
        raise NotImplementedError # Makes sure a child class has it's own init
    
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
                INSERT INTO {table_name} ({columnlist})
                VALUES({qmarks})
              """
        return SQL.format(table_name=cls.dbtable,
                          columnlist=columnlist,
                          qmarks=qmarks)
    
    def _insert(self):
        with sqlite3.connect(self.dbpath) as conn:
            curr = conn.cursor()
            SQL = self._create_insert()
            # getattr returns the value of the named attribute of an object.
            # if not found, it returns the default value provided to the func
            propvals = [getattr(self, propname) for propname in self.fields]

            curr.execute(SQL, propvals)
            #  .lastrowid returns row id of last modified row
            self.pk = curr.lastrowid

    @classmethod
    def _create_update(cls):
        update_column_list = ", ".join(field+"=?" for field in cls.fields)
        SQL = """
                UPDATE {table_name} 
                SET {update_column_list}
                WHERE pk = ?;
              """
        return SQL.format(table_name=cls.dbtable, update_column_list=update_column_list)


    def _update(self):
        with sqlite3.connect(self.dbpath) as conn:
            curr = conn.cursor()
            SQL = self._create_update()
            propvals = [getattr(self, propname) for propname in self.fields + ["pk"]]
            curr.execute(SQL, propvals)
    
    @classmethod
    def one_where(cls, whereclause="TRUE", values=tuple()):
        SQL = "SELECT * FROM {table_name} WHERE " + whereclause
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            cur.execute(SQL.format(table_name=cls.dbtable), values)
            row = cur.fetchone()
            if row is None:
                return None
            return cls(**row)

    @classmethod
    def many_where(cls, whereclause="TRUE", values=tuple()):
        """Equivalent of one_where but with fetchall, returns a list of 
        objects or an empty list."""
        SQL = "SELECT * FROM {table_name} WHERE " + whereclause
        with sqlite3.connect(cls.dbpath) as conn:
            conn.row_factory = sqlite3.Row
            cur = conn.cursor()

            cur.execute(SQL.format(table_name=cls.dbtable), values)
            rows = cur.fetchall()
            return [cls(**row) for row in rows]


    @classmethod
    def from_pk(cls, pk):
        return cls.one_where("pk=?", (pk,))

    @classmethod
    def all(cls):
        """ Return a list of every row in the table as instances of the class
        'SELECT * FROM user_info WHERE TRUE' """
        return cls.many_where()

    def delete(self):
        SQL = "DELETE FROM {table_name} WHERE pk=?"
        with sqlite3.connect(self.dbpath) as conn:
            cur = conn.cursor()
            cur.execute(SQL.format(table_name=self.dbtable),(self.pk,))
            self.pk = None

    def __repr__(self):
        reprstring = "<{cname} {fieldvals}>"
        fieldvals = " ".join("{key}:{value}".format(key=key, value=getattr(self, key))
                            for key in ["pk", *self.fields])# pk followed by all fields
        cname = type(self).__name__ # returns class name
        return reprstring.format(cname=cname, fieldvals=fieldvals)