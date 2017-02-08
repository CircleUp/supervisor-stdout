import json
import sys

import collections


def write_stdout(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def write_stderr(s):
    sys.stderr.write(s)
    sys.stderr.flush()

def main():
    while 1:
        write_stdout('READY\n') # transition from ACKNOWLEDGED to READY
        line = sys.stdin.readline()  # read header line from stdin
        headers = dict([ x.split(':') for x in line.split() ])
        data = sys.stdin.read(int(headers['len'])) # read the event payload
        write_stdout('RESULT %s\n%s'%(len(data), data)) # transition from READY to ACKNOWLEDGED

def event_handler(event, response):
    line, data = response.split('\n', 1)
    headers = dict([ x.split(':') for x in line.split() ])
    lines = data.split('\n')
    prefix = '%s %s | '%(headers['processname'], headers['channel'])
    print('\n'.join([ prefix + l for l in lines ]))

def json_handler(event, response):
    line, data = response.split('\n', 1)
    headers = dict([ x.split(':') for x in line.split() ])
    template = collections.OrderedDict()
    template['processname'] = headers['processname']
    template['channel'] = headers['channel']
    lines = filter(None, map(str.strip, data.split('\n')))
    for line in lines:
        output = template.copy()
        try:
            parsed_data = json.loads(line, object_pairs_hook=collections.OrderedDict)
            output.update(parsed_data)
        except ValueError:
            output['message'] = line
        print(json.dumps(output))

if __name__ == '__main__':
    main()
