#!/usr/bin/env python

import BaseHTTPServer
import datetime
import traceback
import urlparse

import google

endpoint = {
  'bind_interface':     '',
  'bind_port':          8000,
  'target_document':    'Beerbug Testing',
  'target_page':        'Brewing Environment Data',
  'record_required':    {
    'temperature':None,
    'secret':'123987',
  },
  'record_additional':  {
    'time':lambda: datetime.datetime.now().strftime('%m/%d/%Y %H:%M:%S'),
  },
}

def application(environ, start_response):
    global endpoint
    status = 200
    output = ''
    try:
        # Extract the key-value pairs from the query string.
        record = dict(urlparse.parse_qsl(environ.get('QUERY_STRING', '')))
        # Determine if the submitted record is well-formed.
        for field in endpoint['record_required']:
            if not field in record:
                raise KeyError('Record field "' + str(field) + '" missing.')
            elif endpoint['record_required'][field] is not None:
                if endpoint['record_requierd'][field] != record[field]:
                    raise ValueError('Record field "' + str(field) + '" incorrect.')
        for field in endpoint['record_additional']:
            record[field] = endpoint['record_additional'][field]()
        # Upload the record.
        google.spreadsheet(endpoint['target_document'])[endpoint['target_page']].append(record)
    except:
        status = 500
        output = traceback.format_exc()
    response_headers = [
      ('Content-Type', 'text/plain'),
      ('Content-Length', str(len(output))),
    ]
    message = str(status) + ' ' \
      + BaseHTTPServer.BaseHTTPRequestHandler.responses[status][0]
    start_response(message, response_headers)
    if output is not None:
        return [output]
    else:
        return ['']

def serve():
    global endpoint
    import wsgiref
    import wsgiref.simple_server
    try:
        server = wsgiref.simple_server.make_server(
          endpoint['bind_interface'], endpoint['bind_port'], application)
        server.serve_forever()
    except KeyboardInterrupt:
        server.socket.close()

if __name__ == '__main__':
    serve()
