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


## Filter Class
This class can be used to create any Where clause. There is 
a hierarchical structure inside the class. This is how I think
of a WHERE clause in SQL:
* Columns are paired with some sort of comparison *operator*.
  For instance, `column1 = 3` pairs the `column1` column
  with the `=` operator.
* Column-operator pairs are linked together via "joiners" to
  form a clause.  For instance, if we have `column1 = 3` and 
  we also have `column2 LIKE '% King'` then they can be
  joined together as such `column1 = 3 AND column2 LIKE 
  '% King'`. This would mean that we joined them together 
  with a `AND` joiner.
* Clauses can be joined together via other joiners as well. For instance
 `(column1 = 3 AND column2 LIKE '% King') OR (column1 = 1 AND column2 LIKE
  '% Queen')`. Here we use parenthesis for clarity.
 
The Filter class works in the same way. Here is how you instantiate it and 
how you build a where clause:

```python
from statements_classes import Filter
f = Filter()
f.clause(some=1, other=2).or_(op=">=", join="or", another=1, further=4)
f.and_(op='like', join='and', word=1, sentence=2)
```
printing `f.stmt` will result in `( some = ? AND other = ? ) OR 
( another >= ? OR further >= ? ) AND ( word LIKE ? AND sentence LIKE ? )`


## Selector Class
This class can be used to construct the part of the statement that says what
to select in a select statement. You can select the table's alias, the 
columns' aliases and also if they are distinct or not. Here is a quick example:

```python
from statements_classes import Selector
s = Selector(alias='table', use_alias=True)
s.column_list('col1', 'col2', 'col3', col4='c4', col5='c5', distinct=['col1', 'col5'])
```
printing `s.stmt` will result in ` DISTINCT table.col1, table.col2, table.col3,
 table.col4 AS c4, DISTINCT table.col5 AS c5`





