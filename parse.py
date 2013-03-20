import xml.etree.cElementTree as etree
import sys
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

if __name__ == '__main__':
    if len(sys.argv) == 1: # no argument, process std as a tar file
        logger.info('using stdin as a tar archive')
        process_tarfile(sys.stdin)
    else:
        path = sys.argv[1]
        if os.path.isdir(path):
            logger.info('walking directory: ' + path)
            process_dir(sys.argv[1])
        else:
            logger.info('processing tar archive: ' + path)
            process_tarfile(path)
