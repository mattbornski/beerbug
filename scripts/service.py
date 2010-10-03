#!/usr/bin/env python

import ConfigParser
import datetime
import gdata.docs
import gdata.docs.service
import gdata.spreadsheet.service
import getpass
import glob
import os.path
import serial
import sys
import traceback

def readSample(port):
    # Not the most efficient way to communicate over the port,
    # but I'm not exactly I/O limited here.
    try:
        temp = int(port.readline().split()[0])
        return temp
    except:
        pass

def serve(username, password):
    while True:
        port = None
        # Detect which USB device the Arduino lives on.
        for device in glob.glob('/dev/ttyUSB*'):
            try:
                port = serial.Serial(device)
            except:
                pass
        if port is not None:
# TODO This code was trying to determine if we need to create a spreadsheet
# to store beerbug samples in.  It requires a separate login apart from the
# spreadsheets API.  I haven't seriously attempted to create the document,
# I just made one manually.
#            docs_client = gdata.docs.service.DocsService(source='beerbug')
#            docs_client.ClientLogin(username, password)
#            q = gdata.docs.service.DocumentQuery(
#              categories = ['spreadsheet'],
#              params = {'title':'beerbug', 'title-exact':'false'}
#            )
#            feed = docs_client.Query(str(q))
#            if not feed.entry:
#                print >> sys.stderr, 'no such document'
#            else:
#                for entry in feed.entry:
#                    print 'Candidate Document:'
#                    print entry.title.text
            spreadsheet_client = gdata.spreadsheet.service.SpreadsheetsService()
            spreadsheet_client.email = username
            spreadsheet_client.password = password
            spreadsheet_client.source = 'beerbug'
            spreadsheet_client.ProgrammaticLogin()
            feed = spreadsheet_client.GetSpreadsheetsFeed()
            key = None
            id = None
            for spreadsheet in feed.entry:
                if 'beerbug' in spreadsheet.title.text.lower():
                    key = spreadsheet.id.text.rsplit('/', 1)[1]
                    for worksheet in spreadsheet_client.GetWorksheetsFeed(key).entry:
                        if id is None:
                            id = worksheet.id.text.rsplit('/', 1)[1]
                            break
                    if id is not None:
                        break
                    else:
                        key = None
            if key is not None and id is not None:
                try:
                    while True:
                        now = \
                          datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S')
                        sample = str(readSample(port))
                        if sample is not None:
                            print 'temperature is ' + sample + ' degrees F'
                            spreadsheet_client.InsertRow(
                              {'Time':now, 'Temperature':sample},
                              key, id)
                except:
                    print >> sys.stderr, 'Problem uploading sample'
                    traceback.print_exc(file=sys.stderr)
        else:
            print >> sys.stderr, 'Unable to locate Arduino on a USB port.'
            time.sleep(30)

def serve_forever():
    username = None
    password = None
    # Read the username and password from a config file.
    # If not present, prompt the user for their credentials.
    parser = ConfigParser.SafeConfigParser()
    path = os.path.expanduser('~/.beerbug/beerbug.ini')
    try:
        parser.read(path)
    except:
        traceback.print_exc(file=sys.stderr)
    if parser is not None:
        try:
            try:
                username = parser.get('beerbug', 'username')
            except ConfigParser.NoOptionError:
                pass
            try:
                password = parser.get('beerbug', 'password')
            except ConfigParser.NoOptionError:
                pass
        except ConfigParser.NoSectionError:
            pass
    if username is None:
        username = raw_input('Enter Google Docs username [' + getpass.getuser() + ']: ')
        if username.strip() == '':
            username = getpass.getuser()
    if password is None:
        password = getpass.getpass('Enter Google Docs password: ')
    serve(username, password)

if __name__ == '__main__':
    serve_forever()
