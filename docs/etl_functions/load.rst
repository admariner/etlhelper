
Load
^^^^

Functions
---------

ETL Helper provides two functions for loading of data.

- :func:`load() <etlhelper.load>`: Inserts data from an iterable of dictionaries
  or namedtuples into an existing target table.

.. literalinclude:: ../code_demos/load/demo_load_min.py
   :language: python

NOTE: the ``load`` function uses the first row of data to generate the
list of column for the insert query. If later items in the data contain
extra columns, those columns will not be inserted and no error will be
raised.

- :func:`executemany() <etlhelper.executemany>`: Applies SQL query with parameters
  supplied by iterable of data.  Customising the SQL query allows fine control.

.. literalinclude:: ../code_demos/load/demo_executemany_named.py
   :language: python
  
The INSERT query must container placeholders with an appropriate format for
the input data e.g. positional for tuples, named for dictionaries. 

.. literalinclude:: ../code_demos/load/demo_executemany_positional.py
   :language: python

:func:`executemany() <etlhelper.executemany>` can also be used with UPDATE commands.

Keyword arguments
-----------------

chunk_size
""""""""""

:func:`load() <etlhelper.load>` uses :func:`executemany() <etlhelper.executemany>`
behind the scenes.
Large datasets are broken into chunks and inserted in batches to reduce the number
of queries, and only one chunk of data is held in memory at any time.
Within a data processing pipeline, the next step can begin as soon as the first
chunk has been processed.
The database connection must remain open until all data have been processed.

The ``chunk_size`` default is 5,000 and it can be set with a keyword
argument.

commit_chunks
"""""""""""""

The ``commit_chunks`` flag defaults to ``True``. This ensures
that an error during a large data transfer doesn’t require all the
records to be sent again. Some work may be required to determine which
records remain to be sent. Setting ``commit_chunks`` to ``False`` will
roll back the entire transfer in case of an error.

transform
"""""""""

The ``transform`` parameter takes a callable (e.g. function) that
transforms the data before returning it.
See the :ref:`Transform <transform>` section for details.

on_error
""""""""

Accepts a Python function that will be applied to failed rows.
See :ref:`on_error <on_error>` section for details.


Return values
-------------

The number of rows that were processed and the number that failed is
returned as a tuple.
