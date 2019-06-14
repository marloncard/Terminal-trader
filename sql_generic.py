#!/usr/bin/env python3


def create_insert(table_name, columns):

    columnlist = ", ".join(columns)
    qmarks = ", ".join("?" for val in columns)
    SQL = """ INSERT INTO {table_name} ({columnlist})
              VALUES ({qumarks})
          """
    return SQL.format(table_name=table_name,
                      columnlist=columnlist,
                      qmarks=qmarks)


if __name__ == '__main__':
    print(create_insert("employees",
                        ["first_name",
                        "last_name",
                        "employee_id",
                        "birth_date"]))