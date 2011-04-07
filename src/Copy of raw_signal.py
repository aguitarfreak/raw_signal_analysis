'''
Created on Mar 31, 2011

@author: ahwan
'''
import sys, csv
import matplotlib.pyplot as plt

try:
    filename = sys.argv[1]
    snpname = sys.argv[2]
    if(sys.argv[3]=='true'):
        tofile = True
    else: tofile = False
    if(sys.argv[4]=='true'):
        verbose = True
    else: verbose = False
    
except:
    print "USAGE : ", sys.argv[0], " 'signal_file' ", " 'snpname'"," (tofile)true/false", " (verbose)true/false"
    print "Eg..: ", sys.argv[0], " 'signal_file' ", " 'snpname'"," true", " false"
    sys.exit(1)

if(verbose):print "File : ", filename
if(verbose):print "Snp : " , snpname

#Try to get BD, NBS or 58C from filename
if('BD' in filename):
    dataset = 'BD'
    if(verbose):print 'BD data'
elif ('NBS' in filename):
    dataset = 'NBS'
    if(verbose):print 'NBS data'
elif ('58C' in filename):
    dataset = '58C'
    if(verbose):print '58C data'
else:
    dataset = filename

#create csv_reader
reader = csv.reader(open(filename, 'r'), delimiter = '\t')

#copy header
header = reader.next()

#check if the snp exists in the file
temp_snp = ''
temp_row = []
if(verbose):print 'Searching for ', snpname,
dots = 0 #just to print . in stdout while processing
while (temp_snp!=snpname):
    try:
        temp_row = reader.next()
        temp_snp = temp_row[1]
        dots+=1
        if(verbose):
            if(dots%500==0):
                print '.',
        if(verbose):
            if(temp_snp==snpname):
                print snpname, ' found!'
    except StopIteration :
        if(verbose):print snpname, ' not found!'
        sys.exit(1)
        
if(verbose):print 'Preprocessing data. 6 stages - ',
header_ids = header[:5]
if(verbose):print '1',
#strip last two characters, _A specifically, the 5::2 just keeps one copy of each subject
header_subjects = [x[:-2] for x in header[5::2]]
if(verbose):print '2',
#ids of the snp
ids = temp_row[:5]
if(verbose):print '3',
#change values to float
values = map(float, temp_row[5:])
if(verbose):print '4',
#create tuple of the values
values = zip(values[::2], values[1::2])
if(verbose):print '5',
##create dicionary from headers and values
ids_dictionary = dict(zip(header_ids,ids))
values_dictionary = dict(zip(header_subjects,values))
if(verbose):print '6! complete'

if(verbose):print 'plotting!',
plt.figure(1)
plt.xlabel("signal_A")
plt.ylabel("signal_B")
plt.title('Signal A vs Signal B in '+dataset+' subjects for '+ snpname)
dots=0; #just to print . in stdout while processing
for vals in values_dictionary.values():
    plt.plot(vals[0],vals[1],'ro')
    if(verbose):
        if(dots%500==0):
            print '.',
    dots+=1

if not tofile:
    plt.show()
    if(verbose):print 'done'
else:
    plt.savefig(snpname+'_'+dataset,format='png')
    if(verbose):print 'saved as file: ', (snpname+'_'+dataset+ '.png')


