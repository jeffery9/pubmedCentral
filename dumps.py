# !/usr/bin/python

import pickle
import codecs

pfile = open("datafile_2013-01-25 13:56:46.100935")
tfile = codecs.open('result.tsv', 'w', 'utf-8')

data_list = pickle.load(pfile)

for data in data_list:
    tfile.write("%s \t" % unicode(data['titile']))
    tfile.write("%s \t" % unicode(data['abstract']))
    tfile.write("%s \t" % unicode(data['posts']))
    tfile.write("%s \t" % unicode(data['keywords']))
    tfile.write("%s \t" % unicode(data['emails']))
    tfile.write("%s \t" % unicode(data['url']))
    tfile.write("%s \t" % unicode(data['publicaiton']['citation-abbreviation']))
    tfile.write('\n')

