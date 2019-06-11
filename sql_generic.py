#!/usr/bin/env python3


def create_insert(table, columns):

    columnlist = ", ".join(columns)
    qmarks = ", ".join("?" for val in columns)
    SQL = """ INSERT INTO {tablename} ({columnlist})
              VALUES ({qumarks})
          """
    return SQL.format(tablename=tablename,
                      columnlist=columnlist,
                      qmarks=qmarks)


if __name__ == '__main__':
    print(create_insert("employees",
                        ["first_name",
                        "last_name",
                        "employee_id",
                        "birth_date"]))