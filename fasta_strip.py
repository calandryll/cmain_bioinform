#!/usr/bin/python -tt
# Pulls a range of sequences from large FASTA files. 
# Any inputs with - or -- are optional and will default to certain values.
# Written by: Christopher R. Main, University of Delaware
# Last Updated: 09/08/2012

# Versions:
#	0.1 - Open fasta file correctly
#	0.2 - Pull record names and parse them
#	0.3 - Print out cluster range that is wanted
#	0.4 - Write wanted sequences to file
#	0.5 - Comestic interactions
#	0.6 - Changes to argument handling

# Allow opening of FASTA file
from Bio import SeqIO

# Ready arguments from the commandline
import argparse

# Read and parse the arguments from the command line
parser =  argparse.ArgumentParser()
parser.add_argument("-v", "--version", action="version", version='Version 0.6')
parser.add_argument("filename", help="location of FASTA file")
parser.add_argument("out_file", help="filename for output of BLAST search results")
parser.add_argument("first", help="Starting sequence number to begin parsing of file", type=int)
parser.add_argument("last", help="Ending sequence number", type=int)
args = parser.parse_args()

print "Loading %s to memory..." % (args.filename)
handle = open(args.filename, "rU")
output_handle = open(args.out_file, "w")
# Pulls in record names
records = list(SeqIO.parse(handle, "fasta"))

# Write sequences to file
for i in range(int(args.first), int(args.last) + 1):
	SeqIO.write(records[i], output_handle, "fasta")
	print "Writing %s to file" % (records[i].id)

handle.close()
output_handle.close()
print "Writing of %s complete, closing file..." % (args.out_file)