#!/usr/bin/python -tt
# Removes fasta file names and concatenates all of the sequences together
# Any inputs with - or -- are optional and will default to certain values.
# Written by: Christopher R. Main, University of Delaware
# Last Updated: 09/08/2012

# Versions:
#	0.1 - Open fasta file correctly


# Allow opening of FASTA file
from Bio import SeqIO

# Ready arguments from the commandline
import argparse

# Read and parse the arguments from the command line
parser =  argparse.ArgumentParser()
parser.add_argument("-v", "--version", action="version", version='Version 0.6')
parser.add_argument("filename", help="location of FASTA file")
parser.add_argument("out_file", help="filename for output of BLAST search results")
args = parser.parse_args()

print "Loading %s to memory..." % (args.filename)
handle = open(args.filename, "rU")
output_handle = open(args.out_file, "w")
# Pulls in record names
records = list(SeqIO.parse(handle, "fasta"))

# Write sequences to file
for i in range(len(records)):
	output_handle.write("%s" % records[i].seq)
	print "Writing %s to file" % (records[i].seq)

handle.close()
output_handle.close()
print "Writing of %s complete, closing file..." % (args.out_file)