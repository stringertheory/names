import sys
import urlparse
import os

outfile_list = []
n_files = 1
for i in range(n_files):
    outfilename = 'nyp-urls-%02i.txt' % i
    outfile = open(outfilename, 'w')
    outfile_list.append(outfile)

url_filename = sys.argv[1]
done_directory = sys.argv[2]

all_urls = {}
with open(url_filename) as infile:
    for line in infile:
        url = line.strip()
        stub = url.split('/')[-1]
        all_urls[stub] = url

for stub in os.listdir(done_directory):
    url = all_urls.pop(stub, None)

counter = 0
for stub, url in sorted(all_urls.iteritems()):
    index = counter % n_files
    outfile_list[index].write(url + '\n')
    counter += 1

print len(all_urls)
            
for outfile in outfile_list:
    outfile.close()
