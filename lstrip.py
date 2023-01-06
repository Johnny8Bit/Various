'''
Removes leading whitespace and empty lines from text file (in-place)

Usage: lstrip.py <filename.txt>
Overwrites existing file!
Useful for cleaning up output from messy log files

netpacket.net
'''
import sys

__author__ = 'Michal Kowalik'
__version__= '0.2'
__status__ = 'Prototype'

def end():
    print('\nUsage: lstrip.py <filename.txt>')
    sys.exit()

if __name__ == '__main__':
    if len(sys.argv) == 1: end()
    infile, outputlist = open(sys.argv[1]), []
    for line in infile: outputlist.append(line.lstrip())
    infile.close()
    outfile = open(sys.argv[1], 'w')
    for line in outputlist: outfile.write(line)
    outfile.close()
