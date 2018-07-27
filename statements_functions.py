"""
Notice that you can find more information about how a statement should be
prepared for pyodbc to execute it here:
https://stackoverflow.com/questions/43855514/pyodbc-execute-sql-code
https://github.com/mkleehammer/pyodbc/wiki/Cursor#Methods

Examples of pyodbc execution and stmt syntax here:
https://stackoverflow.com/questions/20199569/pyodbc-insert-into-sql
https://stackoverflow.com/questions/37008848/basic-pyodbc-bulk-insert
http://thepythonguru.com/inserting-rows/
"""
from config import SQL_DBO
from sql_table import Table
from statements_classes import Filter


def insert(table: str, schema: str=SQL_DBO) -> str:
    """
    This function creates an insert statement for table.
    Insert statement syntax taken from:
    https://docs.microsoft.com/en-us/sql/t-sql/statements/insert-transact-sql?view=sql-server-2017

    :param table: Name of the table that we want to insert data into.
    :type table: str
    :param schema: Name of the schema for this table.
    :type schema: str
    :return: Insert statement
    :rtype: str

    """
    # Use Table instance to use column names
    t = Table(table)
    columns = t.non_auto
    # Insert only to columns that do not auto-increment.
    stmt = "INSERT INTO {schema}.{table}".format(schema=schema, table=table)
    stmt += "(" + ", ".join(columns) + ")"
    stmt += " VALUES (" + ", ".join(["?"] * len(columns)) + ")"
    return stmt


def update(table: str, schema: str=SQL_DBO) -> str:
    """
    Creates update statement. Syntax for SQL update statement taken from
    https://docs.microsoft.com/en-us/sql/t-sql/queries/update-transact-sql?view=sql-server-2017

    :param table: Name of table we are updating.
    :type table: str
    :param schema: Name of schema for this table.
    :type schema: str
    :return: Update statement.
    :type: str

    """
    # Get the table
    t = Table(table)
    # Update non-keys, set an alias for a table, where clause on keys only
    stmt = "UPDATE table SET {fields} FROM {table} WHERE {where}".format(
        fields=", ".join("table.{}=?".format(c) for c in t.non_keys),
        table=schema + "." + table + " table",
        where=" AND ".join(["{}=?".format(c) for c in t.keys])
    )
    return stmt


def select(table: str, filter_by: 'Filter', schema: str=SQL_DBO) -> str:
    """
    Creates a select statement. Syntax taken from:
    https://docs.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql?view=sql-server-2017

    :param table: Name of table from which we are selecting data.
    :type table: str
    :param filter_by: Where clause
    :type filter_by: Filter
    :param schema: Name of schema for this table.
    :type schema: str
    :return: Select statement
    :rtype: str

    """
    stmt = "SELECT {select} FROM {table} WHERE {where}".format(
        select="",
        table=schema + "." + table + " t",
        where=filter_by.stmt
    )
    return stmt


if __name__ == "__main__":
    f = Filter()
    f.clause(some=1, other=2).or_(op=">=", join="or", another=1, further=4)
    f.and_(op='like', join='and', word=1, sentence=2)
    print(f)
