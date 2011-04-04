'''
Created on Mar 31, 2011

@author: ahwan
'''
import sys, csv
import matplotlib.pyplot as plt

try:
    filename = sys.argv[1]
    snpname = sys.argv[2]
except:
    print "USAGE : ", sys.argv[0], " 'signal_file' ", " 'snpname'"
    sys.exit(1)

print "File : ", filename
print "Snp : " , snpname

#Try to get BD, NBS or 58C from filename
if('BD' in filename):
    dataset = 'BD'
    print 'BD data'
elif ('NBS' in filename):
    dataset = 'NBS'
    print 'NBS data'
elif ('58C' in filename):
    dataset = '58C'
    print '58C data'
else:
    dataset = filename

#create csv_reader
reader = csv.reader(open(filename, 'r'), delimiter = '\t')

#copy header
header = reader.next()

#check if the snp exists in the file
temp_snp = ''
temp_row = []
print 'Searching for ', snpname,
dots = 0 #just to print . in stdout while processing
while (temp_snp!=snpname):
    try:
        temp_row = reader.next()
        temp_snp = temp_row[1]
        dots+=1
        if(dots%50==0):
            print '.',
        if(temp_snp==snpname):
            print snpname, ' found!'
    except StopIteration :
        print snpname, ' not found!'
        sys.exit(1)
        
print 'Preprocessing data. 6 stages - ',
header_ids = header[:5]
print '1',
#strip last two characters, _A specifically, the 5::2 just keeps one copy of each subject
header_subjects = [x[:-2] for x in header[5::2]]
print '2',
#ids of the snp
ids = temp_row[:5]
print '3',
#change values to float
values = map(float, temp_row[5:])
print '4',
#create tuple of the values
values = zip(values[::2], values[1::2])
print '5',
##create dicionary from headers and values
ids_dictionary = dict(zip(header_ids,ids))
values_dictionary = dict(zip(header_subjects,values))
print '6! complete'

print 'plotting!',
plt.figure(1)
plt.xlabel("signal_A")
plt.ylabel("signal_B")
plt.title('Signal A vs Signal B in '+dataset+' subjects for '+ snpname)
dots=0; #just to print . in stdout while processing
for vals in values_dictionary.values():
    plt.plot(vals[0],vals[1],'ro')
    if(dots%50==0):
        print '.',

plt.show()
