from sqlalchemy.schema import (CreateTable, DropTable)


"""
ddl.py contains the Data Definition Language for Postgresql Server.
"""


def compile_create_table(qualified_name: str, column_statement: str,
                         primary_key_statement: str) -> str:
    """Postgresql Create Table statement formatter."""

    statement = """
                CREATE TABLE {table} ({columns} {primary_keys});
                """.format(table=qualified_name,
                           columns=column_statement,
                           primary_keys=primary_key_statement)
    return statement


def generate_create_statement_from_table(table):
    '''
    Generate a SQL create statement from a declarative
    table
    '''

    return str(CreateTable(table.__table__))


def generate_drop_statement_from_table(table):
    '''
    Generate a SQL create statement from a declarative
    table
    '''

    return str(DropTable(table.__table__))