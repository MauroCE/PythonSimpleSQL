# PythonSimpleSQL
A repository containing various code to deal with T-SQL, MS-SQL using pyobdc.
Notice that the config.py file is empty and should be populated as required.
In order to not track changes I followed:
https://stackoverflow.com/questions/9794931/keep-file-in-a-git-repo-but-dont-track-changes/17410119#17410119


## Table class
The Table class is a blueprint for an SQL table. It stores
information about the columns. It has a composition relationship
with Column class in that a Table has one or more Column objects.
To initialize a Table class just call it with its table name:

```python
from sql_table import Table
t = Table('MyTable')
```
Then printing `t` will result in `Table('MyTable')`


## Column class
This class is a blueprint for a column of an SQL table. It
stores information about a column such as:
* Whether it's a primary key
* Whether it's a auto-incrementing column
* Type of that column
* Whether it's nullable
* Which table it comes from
To instantiate a column is quite straight forward:

```python
from sql_table import Column
c = Column(name='Col1', is_nullable=False, 
           table_order=0, type_name='int', 
           is_key=True, table='MyTable')
```