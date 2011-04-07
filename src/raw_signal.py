'''
Created on Mar 31, 2011

@author: ahwan
'''
import sys, csv
import matplotlib.pyplot as plt
import optparse

#traverse list n at a time
def group(iterator, count):
    itr = iter(iterator)
    while True:
        yield tuple([itr.next() for i in range(count)])

# Create option parser
parser = optparse.OptionParser(usage="%prog [OPTIONS]", version="%prog 0.1")

# Add options to parser; use defaults if none specified
parser.add_option("-s", "--signal", dest="signal_filename", help="read data from SIGNAL FILE", default="")
parser.add_option("-g", "--gen", dest="gen_filename", help="read data from GENOTYPE FILE", default="")
parser.add_option("-r", "--rsNumber", dest="snpname", help="rs # of snp", default="")
parser.add_option("-o", "--output", action="store_true", dest="toFile", help="output figure to file", default=False)
parser.add_option("-v", "--verbose", action="store_true", dest="verbose", help="verbose mode", default=False)

(options, args) = parser.parse_args()

#snpname check
if options.snpname=="":
    print "Must specify snpname!"
    parser.print_help()
else:
    snpname = options.snpname

#signal file check
if(options.signal_filename!=""):
    try:
        signal_file = open(options.signal_filename, 'r')
    except IOError as err:
        if err.errno != 2:
            raise err
        print "Error: Signal file could not be opened."
        parser.print_help()
else:
    print "Must specify signal filename!"
    parser.print_help()

#genotype file check
if(options.gen_filename!=""):
    try:
        gen_file = open(options.gen_filename, 'r')
    except IOError as err:
        if err.errno != 2:
            raise err
        print "Error: Genotype file could not be opened."
        parser.print_help()

verbose = options.verbose
toFile = options.toFile

if(verbose):
    print "Signal File : ", options.signal_filename
    print "Snp : " , snpname
    if(options.gen_filename!=""):
        print "Gen File : " , options.gen_filename


#Try to get BD, NBS or 58C from filename
if('BD' in options.signal_filename):
    dataset = 'BD'
    if(verbose):print 'BD data'
elif ('NBS' in options.signal_filename):
    dataset = 'NBS'
    if(verbose):print 'NBS data'
elif ('58C' in options.signal_filename):
    dataset = '58C'
    if(verbose):print '58C data'
else:
    dataset = options.signal_filename

#create csv_reader
reader = csv.reader(signal_file, delimiter = '\t')

#copy header
header = reader.next()

#check if the snp exists in the file
temp_snp = ''
temp_row = []
if(verbose):print 'Searching for ', snpname, ' in signal file',
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
        
if(verbose):print 'Preprocessing data (signal file). 6 stages - ',
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
#create a placeholder for the genotype
values_with_genotype = []
for x in values:
    values_with_genotype.append([x]+[0])
values = values_with_genotype
if(verbose):print '5',
##create dicionary from headers and values
ids_dictionary = dict(zip(header_ids,ids))
values_dictionary = dict(zip(header_subjects,values))

if(verbose):print '6! complete'

#for gen file
if(options.gen_filename!=""):
    reader = csv.reader(gen_file, delimiter = ' ')
    temp_snp = ''
    temp_row = []
    if(verbose):print 'Searching for ', snpname, ' in gen file',
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
    
    if(verbose):print 'Preprocessing data (gen file). 4 stages - ',
    #change values to floats
    values = map(float, temp_row[5:])
    if(verbose):print '1',
    #create triple of the values
    values = list(group(values,3))
    if(verbose):print '2',
    #specify color depending on the triple
    subject_color = []
    color_values = ['ro','go','bo']
    for i in values:
        subject_color.append(color_values[i.index(max(i))])
    if(verbose):print '3',
    #update the previously created dictionary with the color values
    t = 0
    for subject in header_subjects:
        values_dictionary[subject][1] = subject_color[t]
        t = t+1
        
    if(verbose):print '4 complete!'

if(verbose):print 'plotting!',
plt.figure(1)
plt.xlabel("signal_A")
plt.ylabel("signal_B")
plt.title('Signal A vs Signal B in '+dataset+' subjects for '+ snpname)
dots=0; #just to print . in stdout while processing
for vals in values_dictionary.values():
    plt.plot(vals[0][0],vals[0][1],vals[1])
    if(verbose):
        if(dots%500==0):
            print '.',
    dots+=1

if not toFile:
    plt.show()
    if(verbose):print 'done'
else:
    plt.savefig(snpname+'_'+dataset,format='png')
    if(verbose):print 'saved as file: ', (snpname+'_'+dataset+ '.png')
