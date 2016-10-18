from app.tools.formatters import format_repr


class Database:
    __slots__ = 'name',

    def __init__(self, name):
        self.name = name

    def create_statement(self):
        return 'CREATE DATABASE %s;' % self.name

    def drop_statement(self):
        return 'DROP DATABASE IF EXISTS %s;' % self.name

    def __repr__(self):
        return format_repr(self, self.__slots__)