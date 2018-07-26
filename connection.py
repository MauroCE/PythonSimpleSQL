import pyodbc
from config import SQL_DRIVER, SQL_DB, SQL_SERVER

# Need a connection string to connect. Parenthesis are redundant and are used
# only so that the connection string looks much clearer. Could also just
# write this into pyobdc.connect() function. See:
# https://github.com/mkleehammer/pyodbc/wiki/Connecting-to-SQL-Server-from-Windows
# https://docs.microsoft.com/nl-be/sql/connect/python/pyodbc/step-3-proof-of-concept-connecting-to-sql-using-pyodbc?view=sql-server-2017
connection_string = (
    r"Driver={driver};"
    r"Server={server};"
    r"Database={db};"
    r"Trusted_Connection=yes"
    .format(driver=SQL_DRIVER, server=SQL_SERVER, db=SQL_DB)
)
# Pass the connection string to pyobdc.connect(). The keyword argument
# autocommit=False means that whenever we execute statements these are put
# into a transaction, which must be closed manually by the user using either
# cnxn.commit() or cursor.commit()
# For more information:
# https://github.com/mkleehammer/pyodbc/wiki/Database-Transaction-Management
cnxn = pyodbc.connect(connection_string, autocommit=False)
cursor = cnxn.cursor()
# In this package we will use large batches of statements. These are executed
# faster if we add fast_executemany=True
cursor.fast_executemany = True
