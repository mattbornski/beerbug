#!/usr/bin/env python

import ConfigParser
import gdata.spreadsheet.text_db
import getpass
import os.path

class service(dict):
    username = None
    password = None
    client = None
    def __init__(self, username = None, password = None, implicit = False):
        # Read the username and password from a config file.
        # If not present, prompt the user for their credentials.
        paths = [
          os.path.expanduser('~/.beerbug/beerbug.ini'),
          os.path.join(os.path.dirname(__file__), 'beerbug.ini'),
          os.path.abspath('beerbug.ini'),
        ]
        for path in paths:
            parser = ConfigParser.SafeConfigParser()
            parser.read(path)
            if parser is not None:
                try:
                    try:
                        username = parser.get('google', 'username')
                    except ConfigParser.NoOptionError:
                        pass
                    try:
                        password = parser.get('google', 'password')
                    except ConfigParser.NoOptionError:
                        pass
                except ConfigParser.NoSectionError:
                    pass
        if not implicit:
            if username is None:
                username = raw_input('Enter Google Docs username [' \
                  + getpass.getuser() + ']: ')
                if username.strip() == '':
                    username = getpass.getuser()
            if password is None:
                password = getpass.getpass('Enter Google Docs password: ')
        if username is not None:
            self.username = username
        if password is not None:
            self.password = password
        # Connect
        self.client = self.connect()
        # Populate
        if not implicit:
            self._index()
    def connect(self):
        # Read username and password from config files if not set.
        
        # Connect to Google
        return gdata.spreadsheet.text_db.DatabaseClient(
          username = self.username, password = self.password)
    def _index(self):
        for db in self.client.GetDatabases(name = ''):
            self[db.entry.title.text] = spreadsheet(db_instance = db, service_instance = self)

class spreadsheet(dict):
    def __init__(self, name = None, db_instance = None, service_instance = None):
        if db_instance is not None and service_instance is not None:
            self._db = db_instance
            self._service = service_instance
        elif name is not None:
            self._service = service(implicit = True)
            self._db = self._service.client.GetDatabases(name = name)[0]
        tables = self._db.GetTables()
        for table in tables:
            self[table.name] = page(table)

class page(list):
    def __init__(self, table):
        self._table = table
        self._table.LookupFields()
        for record in self._table.GetRecords(1, int(table.entry.row_count.text)):
            list.append(self, record.content)
    def append(self, record):
        self._table.AddRecord(record)
        list.append(self, record)

def serve_forever():
    service()

if __name__ == '__main__':
    serve_forever()
