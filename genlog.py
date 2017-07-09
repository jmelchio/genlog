#!/usr/bin/env python
# encoding: utf-8
"""
genlog.py

Created by Joris Melchior on 2017-06-30
Copyright (c) 2017 Melchior I.T. Inc. All rights reserved
"""
import getopt
import sys
import time
import datetime
import json

help_message = """
Program to generate log files to experiment with ELK stack
Usage: python genlog.py [options] DESTINATION [SOURCE]

Where:
    DESTINATION file to log the lines to, only basename is needed, program will add timestamp and .log extension
    SOURCE      optional file to use as template and spit out line by line to DESTINATION
    
Options:
    -v or --verbose     also show lines on stdout
"""


class Usage(Exception):
    def __init__(self, msg):
        self.msg = msg


def generate_log_line():
    log_line = {'timestamp': datetime.datetime.now(datetime.timezone.utc).astimezone().isoformat(),
                'message': 'Some really fancy log line',
                'time_taken_ms': 200}
    return json.dumps(log_line)


def read_lines(source):
    with open(source, 'r') as source_file:
        while True:
            line = source_file.readline()
            if len(line) > 0:
                if not line.endswith('\n'):
                    line = line + '\n'
                yield line
            else:
                source_file.seek(0)


def produce_lines(destination, lines=None, verbose=False):
    with open(destination, 'w') as destination_file:
        if lines:
            for line in lines:
                time.sleep(0.2)
                if not line.endswith('\n'):
                    line = line + '\n'
                destination_file.write(line)
                if verbose:
                    print(line[:-1])
        else:
            while True:
                time.sleep(0.2)
                line = generate_log_line()
                destination_file.write(line + '\n')
                if verbose:
                    print(line)


def main(argv=None):
    if argv is None:
        argv = sys.argv

    try:
        try:
            opts, args = getopt.getopt(argv[1:], "hv", ["help", "verbose"])
        except getopt.error as goErr:
            raise Usage(goErr)

        verbose = False

        for option, value in opts:
            if option in ("-v", "--verbose"):
                verbose = True

        if len(args) < 1:
            raise Usage(help_message)

        destination = args[0]
        try:
            destination_log = destination + '_' + datetime.datetime.now().strftime('%Y-%m-%dT%H_%M_%S') + '.log'
            if len(args) > 1:
                source = args[1]
                lines = read_lines(source)
                print("logging with destination: '{}' and source: '{}', verbose is {}"
                      .format(destination_log, source, verbose))
                produce_lines(destination_log, lines=lines, verbose=verbose)
            else:
                print("logging with destination: '{}' only, verbose is {}".format(destination_log, verbose))
                produce_lines(destination_log, verbose=verbose)
        except OSError as osError:
            print('Error occurred in execution: {}'.format(osError))
            return 2
        except KeyboardInterrupt as keyInt:
            print('Program interrupted by user. {}'.format(keyInt))
            return 0

    except Usage as err:
        print(sys.argv[0].split("/")[-1] + ": " + str(err.msg), file=sys.stderr)
        print("for help use -h or --help", file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())

# That's All Folks !!
