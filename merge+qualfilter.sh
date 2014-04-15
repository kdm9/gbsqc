#!/bin/bash
tooldir=$(dirname $(readlink -f $0))/tools
set -x
cd reads
#for i in "test"
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
	# calls to Seqqs record the quality info to files for each stage.

	mkdir -p qc
	mkdir -p log
	ls  --color=never [ACGT]*_1.fq | parallel -j 14 --results log --joblog log/${i}_jlog_`date +%F_%T` \
		bcd\=\$\(basename {}  _1.fq\) \; \
		${tooldir}/seqtkwithpatches/seqtk interleave \$\{bcd\}_[12].fq \| \
			${tooldir}/seqqs/seqqs -i -e -p qc/\$\{bcd\}_initial - \| \
	       		${tooldir}/seqtkwithpatches/seqtk seq -b \$bcd -B \$bcd - \| \
			${tooldir}/scythe/scythe -p 0.05 -a ~/ws/refseqs/illumina_adapters.fa -M 0 - \| \
			${tooldir}/seqqs/seqqs -i -e -p qc/\$\{bcd\}_scythe - \| \
			${tooldir}/sickle/sickle pe -c /dev/stdin -t sanger -s \>\(gzip \>\$\{bcd\}_s.fq.gz\) -m /dev/stdout -q 26 -l 64 -n \| \
			${tooldir}/seqqs/seqqs -i -e -p qc/\$\{bcd\}_sickle - \| \
			gzip \>\> plate$i.ilfq.gz
	popd
done
