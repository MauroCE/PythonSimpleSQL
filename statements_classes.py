

class Selector:

    def __init__(self, alias: str="t", use_alias: bool=True):
        """
        Constructor for Selector class. All syntax taken from:
        https://docs.microsoft.com/en-us/sql/t-sql/queries/select-transact-sql?view=sql-server-2017

        :param alias: Alias for the table.
        :type alias: str
        :param use_alias: Whether to use the alias or not
        :type use_alias: bool

        """
        # Keep the table alias and whether to use the alias or not
        self.t = alias + "." if use_alias else ""
        self.use_alias = use_alias
        # Placeholder for the statement
        self.stmt = ""

    def __repr__(self) -> str:
        """
        String used to re-create instance.
        :return: String used to re-create instance.
        :rtype: str
        """
        return "Selector({0}, {1})".format(self.t, self.use_alias)

    def __str__(self) -> str:
        """
        String displayed on screen with print() function.

        :return: String displayed on screen with print() function.
        :rtype: str
        """
        return self.stmt

    def column_list(self, *args: str, distinct: list=[], **kwargs: str):
        """
        Args represent columns without aliases, Kwargs represent columns with
        aliases.

        :param args: Name of columns that we want to select. These columns
                     do not need an alias.
        :type args: str
        :param distinct: List containing names of columns from which we want
                         distinct values.
        :type distinct: list
        :param kwargs: Keys are the names of the columns that we want to select
                       while the values are their aliases.
        :type kwargs: str
        :return: Nothing to return
        :rtype: None
        """
        no_alias = ", ".join(self.t + col
                             if col not in distinct
                             else " DISTINCT " + self.t + col
                             for col in args)
        alias = ", ".join(self.t + col + " AS " + kwargs[col]
                          if col not in distinct
                          else "DISTINCT " + self.t + col
                               + " AS " + kwargs[col]
                          for col in kwargs.keys())
        col_list = ", ".join([no_alias, alias])
        if len(self.stmt) == 0:
            self.stmt += col_list
        else:
            self.stmt = self.stmt + ", " + col_list

    def calc(self, field: str, op: str):
        """
        Selects a calculation.
        :param field: Name of the column that we want to select and for which
                      we want the calculation.
        :type field: str
        :param op: Operation that we want to perform on the table. For instance
                   is we want to calculate "col1 * 40" we would have
                   field = " col1" and op=" * 40"
        :return: Nothing to return
        :rtype: None
        """
        if len(self.stmt) == 0:
            self.stmt += field + op
        else:
            self.stmt += ", " + field + op


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
    # Filter
    f = Filter()
    f.clause(some=1, other=2).or_(op=">=", join="or", another=1, further=4)
    f.and_(op='like', join='and', word=1, sentence=2)
    print(f)
    # Selector
    s = Selector(alias='table', use_alias=True)
    s.column_list('col1', 'col2', 'col3', col4='c4', col5='c5', distinct=['col1', 'col5'])
    print(s.stmt)
