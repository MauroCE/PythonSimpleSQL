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
        self.columns = self._columns_info()

    def __repr__(self) -> str:
        """
        Returns string that can be evaluated to evaluate to instantiate class.

        :return: String that can be used to create the instance.
        :rtype: str
        """
        return "Table('{}')".format(self.name)

    def _columns_info(self) -> list:
        """
        This function gets information about the columns.
        :return:
        """
        # Need to get column names. There are multiple ways but they depend
        # on MS-SQL version. For more information, see here:
        # https://stackoverflow.com/a/11459153/6435921
        stmt = "exec sp_columns '{}'".format(self.name) # Need ''
        cursor.execute(stmt)
        # Fetch all the results, construct a DataFrame from it
        data = pd.DataFrame.from_records(
            data=cursor.fetchall(),
            columns=[c[0] for c in cursor.description]
        )
        # Only keep col name, data type, type name, nullable, position
        cols = ['COLUMN_NAME', 'DATA_TYPE', 'TYPE_NAME',
                'IS_NULLABLE', 'ORDINAL_POSITION']
        # Order the rows to get column names in correct order
        data = data.loc[:, cols].sort_values(by=['ORDINAL_POSITION'])
        # Add columns to a list as Column instances
        columns = []
        for c in data.itertuples(index=False):
            col = Column(name=c.COLUMN_NAME, is_nullable=c.IS_NULLABLE,
                         table_order=c.ORDINAL_POSITION, data_type=c.DATA_TYPE,
                         type_name=c.TYPE_NAME)
            columns.append(col)
        return columns


class Column:

    def __init__(self, name: str, is_nullable: bool, table_order: int,
                 data_type: int, type_name: str):
        """
        Constructor for Column class.

        :param name: Name of the column
        :type name: str
        :param is_nullable: Whether the column can contain null values
        :type is_nullable: bool
        :param table_order: Ordinal position of the column in the table def
        :type table_order: int
        :param data_type: Integer representing the data type of the column
        :type data_type: int
        :param type_name: Name of the data type.
        :type type_name: str
        """
        # Initialize all attributes
        self.name = name
        self.is_nullable = is_nullable
        self.table_order = table_order
        self.type = type_name
        self.type_int = data_type

    def __repr__(self):
        """
        Return string that can be eval() to re-instantiate the obj.
        :return:
        """
        s = "Column('{name}', {null}, {ord}, {type}, '{type2}')".format(
            name=self.name, null=self.is_nullable, ord=self.table_order,
            type=self.type_int, type2=self.type
        )
        return s


if __name__ == "__main__":
    t = Table('CustomTimeSeries')
    print(t)
    print('hi')
