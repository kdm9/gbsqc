#!/bin/bash
tooldir=$(dirname $(readlink -f $0))/tools
set -x
cd reads
for i in {1..4} 6
do
	pushd $i
	## Line-wise comments for the below:
	# get all demuxed read pairs, not the nobcd ones tho, and samplewise, do:
		# get bcd from sample name
		# interleave pairs for this sample
		# add bcd back. use the barcode as the qual string too, all NTs are > 33
		# Trim 3prime contaminants away. -M 0 is to keep all pairs
		# Sliding window trim. -q 26 = min window PHRED of 26, -c/m for interleaved files
		# Save a copy to disk as well as big catted file

	ls  --color=never [ACGT]*_1.fq |head -n 2 | parallel \
		bcd\=\$\(basename {}  _1.fq\) \; \
		${tooldir}/seqtkwithpatches/seqtk interleave \$\{bcd\}_[12].fq \| \
	       		${tooldir}/seqtkwithpatches/seqtk seq -b \$bcd -B \$bcd - \| \
			${tooldir}/scythe/scythe -p 0.05 -a ~/ws/refseqs/illumina_adapters.fa -M 0 - \| \
			${tooldir}/sickle/sickle pe -c - -t sanger -m - -q 26 -n \| \
			tee \$\{bcd\}_qcd.ilfq |gzip \>\> plate$i.ilfq.gz
	popd
done
