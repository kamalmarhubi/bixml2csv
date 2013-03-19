import xml.etree.cElementTree as etree
import sys
import os
import logging

if __name__ == '__main__':
    logger = logging.getLogger(__name__)
    rootLogger = logging.getLogger()
    rootLogger.addHandler(logging.StreamHandler())
    rootLogger.setLevel(logging.INFO)

    for dirname, dirnames, filenames in os.walk(sys.argv[1]):
        for filename in filenames:
            fullpath = os.path.join(dirname, filename)
            if not fullpath.endswith('.xml'):
                #logger.debug('skipping file: ' + fullpath)
                continue
            logger.info('processing file: ' + fullpath)
            file_time = None
            try:
                for event, element in etree.iterparse(fullpath,
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
                logger.error('Error processing ' + fullpath)
                logger.exception(e)
