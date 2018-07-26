import pyodbc
import pandas as pd
from config import SQL_DBO
from connection import cursor


class Table:

    def __init__(self, name: str):
        """
        Constructor for Table class. Instantiates the Table class.

        :param name: Name of the table.
        :type name: str
        """
        self.name = name
        # Table class HAS A Column (one at least)
        self.columns = self.get_cols()

    def __repr__(self) -> str:
        """
        Returns string that can be evaluated to evaluate to instantiate class.

        :return: String that can be used to create the instance.
        :rtype: str
        """
        return "Table('{}')".format(self.name)

    def get_cols(self):
        """
        This function implements a better way of getting information about the
        columns.
        To read more about these methods, go to:
        https://github.com/mkleehammer/pyodbc/wiki/Cursor
        https://stackoverflow.com/questions/37712307/pyodbc-read-primary-keys-from-ms-access-mdb-database
        :return:
        """
        # Get columns info
        cols = list(cursor.columns(table=self.name))
        # Get names of primary key columns
        keys = [key.column_name for key in list(cursor.primaryKeys(self.name))]
        # Get type, table position, nullable bool, primarykey bool
        info = {col.column_name: {
            'type': col.type_name,
            'index': col.ordinal_position - 1,
            'null': False if col.is_nullable == "NO" else True,
            'is_key': True if col.column_name in keys else False
        } for col in cols}
        # Use this information to instantiate Column objects
        columns = []
        for name in info.keys():
            c = Column(name=name, is_nullable=info[name]['null'],
                       table_order=info[name]['index'],
                       type_name=info[name]['type'], table=self.name)
            columns.append(c)
        return columns


class Column:

    def __init__(self, name: str, is_nullable: bool, table_order: int,
                 type_name: str, table: str):
        """
        Constructor for Column class.

        :param name: Name of the column
        :type name: str
        :param is_nullable: Whether the column can contain null values
        :type is_nullable: bool
        :param table_order: Ordinal position of the column in the table def
        :type table_order: int
        :param type_name: Name of the data type.
        :type type_name: str
        :param table: Name of the table this column is from
        :type table: str
        """
        # Initialize all attributes
        self.name = name
        self.is_nullable = is_nullable
        self.table_order = table_order
        self.type = type_name
        self.table = table

    def __repr__(self):
        """
        Return string that can be eval() to re-instantiate the obj.
        :return:
        """
        s = "Column('{name}', {null}, {ord}, '{type2}', '{t}')".format(
            name=self.name, null=self.is_nullable, ord=self.table_order,
            type2=self.type, t=self.table
        )
        return s


if __name__ == "__main__":
    t = Table('CustomTimeSeries')
    print(t)
    print(t.columns)
