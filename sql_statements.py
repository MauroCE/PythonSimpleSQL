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


def select(table: str, selector="*", schema: str=SQL_DBO) -> str:
    """
    Creates a select statement. Syntax taken from:
    https://docs.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql?view=sql-server-2017

    :param table: Name of table from which we are selecting data.
    :type table: str
    :param selector: What to select from the table
    :type selector: str
    :param schema: Name of schema for this table.
    :type schema: str
    :return: Select statement
    :rtype: str

    """
    stmt = "SELECT {select} FROM {table} WHERE {where}".format(
        select=selector,
        table=schema + "." + table + " t",
        where=""
    )
    return stmt


class Filter:

    def __init__(self):
        """
        This class can be used to construct a WHERE clause. Notice that all the
        methods below have been written copying:
        https://docs.microsoft.com/en-us/sql/t-sql/queries/where-transact-sql?view=sql-server-2017
        so they should be pretty comprehensive

        """
        self.valid_operators = ["=", ">", "<", ">=", "<=", "in",
                                "like", "between"]
        self.valid_joiners = ["and", "or"]
        self.stmt = ""

    def __repr__(self) -> str:
        """
        String that can be used to re-create the instance.

        :return: String to re-instantiate
        :rtype: str

        """
        return "Filter()"

    def __str__(self) -> str:
        """
        String printed to stdout for the instance.

        :return: Filter statement
        :rtype: str

        """
        return self.stmt

    def clause(self, join: str="AND", op: str="=", **kw) -> 'Filter':
        """
        Creates a clause joining different conditions using the same operator.

        :param join: One of 'and' or 'or' (can be upper case). They are joiners
                     in the sense that they join different conditions. For
                     instance "column1 = 'hello' AND column2='world'".
        :type join: str
        :param op: Operator used for the comparison. Can be one of the provided
                   list in self.valid_operators.
        :type op: str
        :param kw: Keyword arguments used to construct the query. The key
                   should be the name of the column, the value should be the
                   value for that column. Might think of moving this to *args
                   as not sure whether I should be handling in the values to
                   create the params.
        :return: The class instance itself.
        :rtype: Filter

        """
        # Need to use valid joiners and operators
        if join.lower() in self.valid_joiners:
            if op.lower() in self.valid_operators:
                self.stmt += "("
                self.stmt += join.upper().join(
                    " {col} {op} ? ".format(col=k, op=op.upper())
                    for k in kw.keys()
                )
                self.stmt += ")"
            else:
                raise NotImplemented(
                    "Provided operator not in {}".format(self.valid_operators)
                )
        else:
            raise NotImplemented(
                "Provided join not in {}".format(self.valid_joiners)
            )
        return self

    def or_(self, **kwargs) -> 'Filter':
        """
        Joins two clauses with an OR operator.

        :param kwargs: Same as in clause method.
        :return: Class instance itself
        :rtype: Filter.

        """
        self.stmt += " OR "
        self.clause(**kwargs)
        return self

    def and_(self, **kwargs) -> 'Filter':
        """
        Joins two clauses with an AND operator.

        :param kwargs: Same as in clause method.
        :return: Class instance itself
        :rtype: Filter.

        """
        self.stmt += " AND "
        self.clause(**kwargs)
        return self


if __name__ == "__main__":
    f = Filter()
    f.clause(some=1, other=2).or_(op=">=", join="or", another=1, further=4)
    f.and_(op='like', join='and', word=1, sentence=2)
    print(f)
