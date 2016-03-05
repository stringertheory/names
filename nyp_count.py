import sys
import csv
import collections

from dateutil.parser import parse as date_parse

counter = collections.Counter()
filename = sys.argv[1]
with open(filename) as infile:
    reader = csv.reader(infile)
    reader.next()
    for url, date_string, headline in reader:
        date = date_parse(date_string).date()
        counter[date] += 1

for date, count in sorted(counter.iteritems()):
    print date.isoformat(), count
