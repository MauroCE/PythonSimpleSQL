from config import SQL_DBO
from sql_table import Table


def insert(table: str, schema: str=SQL_DBO) -> str:
    """
    This function creates an insert statement for table.

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
    Creates update statement.

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


if __name__ == "__main__":
    pass
