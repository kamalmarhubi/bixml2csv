import xml.etree.cElementTree as etree
import cStringIO
import codecs
import csv
import sys
import os
import logging

logger = logging.getLogger(__name__)
rootLogger = logging.getLogger()
rootLogger.addHandler(logging.StreamHandler())
#rootLogger.setLevel(logging.DEBUG)


class UnicodeWriter:
    """
    A CSV writer which will write rows to CSV file "f",
    which is encoded in the given encoding.
    """

    def __init__(self, f, dialect=csv.excel, encoding="utf-8", **kwds):
        # Redirect output to a queue
        self.queue = cStringIO.StringIO()
        self.writer = csv.writer(self.queue, dialect=dialect, **kwds)
        self.stream = f
        self.encoder = codecs.getincrementalencoder(encoding)()

    def writerow(self, row):
        self.writer.writerow([s.encode("utf-8") for s in row])
        # Fetch UTF-8 output from the queue ...
        data = self.queue.getvalue()
        data = data.decode("utf-8")
        # ... and reencode it into the target encoding
        data = self.encoder.encode(data)
        # write to the target stream
        self.stream.write(data)
        # empty queue
        self.queue.truncate(0)

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

if __name__ == '__main__':
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
