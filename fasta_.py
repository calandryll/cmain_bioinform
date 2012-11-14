#!/usr/bin/python -tt
# Pull out a sequence from a fasta file based by on name from another file list. 
# Any inputs with - or -- are optional and will default to certain values.
# Written by: Christopher R. Main, University of Delaware
# Last Updated: 10/18/12

# Versions:
#	0.1 - Open fasta file correctly
#	0.2 - Open and read a tab delimited file of sequence names
#	0.3 - Search read in tab file within fasta file
#	0.4 - Write to file
#	0.5 - Add Treatment name next to 
#	0.6 - 

# Allow opening of FASTA file
from Bio import SeqIO

# Ready arguments from the commandline
import argparse

# Read and parse the arguments from the command line
parser =  argparse.ArgumentParser()
parser.add_argument("-v", "--version", action="version", version='Version 0.6')
parser.add_argument("filename", help="location of FASTA file")
parser.add_argument("in_file", help="filename of sequence names")
parser.add_argument("out_file", help="filename for output of sequences")
args = parser.parse_args()

# Opens up filename
print "Loading %s to memory..." % (args.filename)
handle = open(args.filename, "rU")
input_handle = open(args.in_file, "rU")
output_handle = open(args.out_file, "w")

# Pull in sequences and treatment from tab delimited file
seq_nameList = []
treatList = []
blargList = []

for line in input_handle:
   seq_name, treat = line.split("\t")
   seq_nameList.append(seq_name)
   treatList.append(treat)

fasta_parse = SeqIO.parse(handle, "fasta")

# Search FASTA file with tab delimited file
print "Searching %s..." % (args.filename)	
records = (r for r in fasta_parse if r.id in seq_nameList)
count = SeqIO.write(records, output_handle, "fasta")
print "Saved %i records to %s" % (count, args.out_file)

handle.close()
output_handle.close()
input_handle.close()