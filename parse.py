import xml.etree.cElementTree as etree
import os
import os.path
import logging
from itertools import ifilter
import tarfile
from contextlib import closing

logger = logging.getLogger(__name__)
rootLogger = logging.getLogger()
rootLogger.addHandler(logging.StreamHandler())
rootLogger.setLevel(logging.INFO)
log_level_dict = { 0: logging.WARNING
                 , 1: logging.INFO
                 , 2: logging.DEBUG
                 }

def process_fileobj(fileobj, name='<nameless>'):
    logger.debug('processing file: ' + name)
    file_time = None
    try:
        for event, element in etree.iterparse(fileobj,
                                              events=('start', 'end')):
            if event == 'start':
                if element.tag == 'stations':
                    file_time = element.get('lastUpdate')
                else:
                    continue
            elif element.tag != 'station':
                continue
            else:
                row = [unicode(elt.text) or ''
                       for elt in element.getchildren()]
                row.insert(0, file_time)
                print(','.join(row).encode('utf-8'))
                element.clear()
    except etree.ParseError as e:
        logger.error('Error processing ' + name + ':')
        logger.exception(e)

def process_file(path):
    with open(path) as fileobj:
        process_fileobj(fileobj, path)

def process_tarfile(path):
    if isinstance(path, str):
        tf = tarfile.open(path)
    else:
        tf = tarfile.open(fileobj=path, mode='r|')
    with closing(tf) as tf:
        for tinf in ifilter(lambda tinf: tinf.isfile() and tinf.name.endswith('.xml'),
                            tf):
            with closing(tf.extractfile(tinf)) as fileobj:
                process_fileobj(fileobj, tinf.name)

def process_dir(path):
    for dirname, dirnames, filenames in os.walk(path):
        for filename in filenames:
            fullpath = os.path.join(dirname, filename)
            if not fullpath.endswith('.xml'):
                logger.debug('skipping file: ' + fullpath)
                continue
            process_file(fullpath)

def main():
    import sys
    import argparse
    argp = argparse.ArgumentParser()
    argp.add_argument('file', nargs='?', default='-',
                      help='directory or tar archive to process')
    argp.add_argument('-v', '--verbose', dest='verbosity', action='count', default=0,
                      help='be verbose (specify twice for more)')
    args = argp.parse_args()
    # set log level; higher repeats get DEBUG
    log_level = log_level_dict.get(args.verbosity, logging.DEBUG)
    logger.setLevel(log_level)

    if args.file == '-':
        logger.warn('using stdin as a tar archive...')
        process_tarfile(sys.stdin)
    else:
        if os.path.isdir(args.file):
            logger.info('walking directory: ' + args.file)
            process_dir(args.file)
        else:
            logger.info('processing tar archive: ' + args.file)
            process_tarfile(args.file)

if __name__ == '__main__':
    import sys
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(130) # 130: terminated by ^C
    except (IOError, OSError):
        sys.exit(141)
