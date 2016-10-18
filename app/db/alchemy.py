def create_table_from_base(table, engine):
    '''
    Create a table from a defined declarative
    base SQL Class
    '''

    table.__table__.create(engine)


def drop_table_from_base(table, engine):
    '''
    Drop a table from a defined declarative
    base SQL Class
    '''

    table.__table__.drop(engine)