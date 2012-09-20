#!/usr/bin/python -tt
# Automated BLAST search of a FASTA file. Search defaults to blastx (Protein) search,
# blast type, database, e-value threshold and number of hits can be changed with 
# commandline inputs.
# Any inputs with - or -- are optional and will default to certain values.
# Written by: Christopher R. Main, University of Delaware
# Last Updated: 09/08/2012

# Versions:
#	0.1 - Open Cluster file and begin searching internet blast
#	0.2 - Search and send output to screen of top result
#	0.3 - Output BLAST results with GI, Length, E-Value, Query Start, Subject Start, Score and Bits
#	0.4 - Setup of for loop to run multiple queries, and output to separate files
#	0.5 - Append data to the file with added sequence name to first column
#	0.6 - Change way of doing inputs
#	Future versions:
#	0.7 - Write for local database search, for use on BioHen

# Allow manipulating of FASTA file
from Bio import SeqIO
# Allows for internet blast search
from Bio.Blast import NCBIWWW
# Parsing of BLAST results
from Bio.Blast import NCBIXML

# Ready arguments from the commandline
import argparse

# Read and parse the arguments from the command line
parser =  argparse.ArgumentParser()
parser.add_argument("-v", "--version", action="version", version='Version 0.6')
parser.add_argument("filename", help="location of FASTA file")
parser.add_argument("out_file", help="filename for output of BLAST search results")
parser.add_argument("-b", "--blast", help="what type of blast to use (Defaults to blastx)", default='blastx')
parser.add_argument("-t", "--thres", help="e-value threshold, ignores any numbers above this number (Defaults to 0.005)", type=int, default=0.005)
parser.add_argument("-hl", "--hitlist", help="how many alignments do you want parsed into the file (Defaults to 10)", default=10)
parser.add_argument("-d", "--database", help="what database to search against (Defaults to nr)", default='nr')
parser.add_argument("-l", "--local", help="location of the local database to blast search against", default='')
args = parser.parse_args()


# Open file
handle = open(args.filename, "rU")

# BLAST first sequence of file
records = list(SeqIO.parse(handle, format="fasta"))

# Open file, this will append the file for each sequence, information is tab delimited and easily imported into Excel or other type software
wfile = open(args.out_file, "a")

# Write headers of columns: Sequence Name, GI #, Title, Length, E-Value, Query Start, Subject Start, Score, Bits
wfile.write("Sequence Name\tGI\tTitle\tLength\te-value\tQuery Start\tQuery End\tSubject Start\tSubject End\tGaps\tScore\tBits\n")


# Begin the loop to search each individual record. Each iteration of the loop will search a new sequence
for i in range(len(records)):
	print "Blasting %s..." % (records[i].id)
	# Blast type, database, name of sequence being run from fasta file, grab gi #s, limit number of hits to 10
	result_handle = NCBIWWW.qblast(args.blast, args.database, records[i].seq, ncbi_gi="TRUE", hitlist_size=args.hitlist)

	# Take Search and output to file
	blast_records = NCBIXML.parse(result_handle)
	#blast_records = NCBIXML.parse(open("blarg.xml"))

	# Begin the loop, run as many times as there are records in the blast search
	for blast_record in blast_records:
		print "Writing search results for %s..." % (records[i].id)
		# Run as many times as there are alignment sequences set by user input
		for alignment in blast_record.alignments:
			# Run as many times as there are information stored in the hsp (Has e-value, and other info)
			for hsp in alignment.hsps:
				# Ignore e-values above what was set by user
				if hsp.expect < float(args.thres):
					# Strip the ugliness out of the name file, so we can get what we want (ie GI # and Title
					giFields = alignment.title.strip().split("|")
					gi_num = giFields[1]
					gi_title = giFields[4]
					wfile.write("%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n" % (records[i].id, gi_num, gi_title, alignment.length, hsp.expect, hsp.query_start, hsp.query_end, hsp.sbjct_start, hsp.sbjct_end, hsp.gaps, hsp.score, hsp.bits))
wfile.close()
print "Writing of %s complete, closing file..." % (args.out_file)