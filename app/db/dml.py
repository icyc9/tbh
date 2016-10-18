"""
dml.py contains the Data Manipulation Language for Postgresql Server.
"""


def create_insert_statement(qualified_name, column_names, table_alias=''):
    column_string = ', '.join(column_names)
    value_string = ', '.join(['%s']*len(column_names))

    if table_alias:
        table_alias = ' as %s' % table_alias

    return 'INSERT INTO {0}{1} ({2}) VALUES ({3})'.format(qualified_name,
                                                          table_alias,
                                                          column_string,
                                                          value_string)