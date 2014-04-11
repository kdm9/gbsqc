#!/bin/bash

cd reads
for i in {1..4} 6; do mkdir -p $i; done

parallel --gnu \
	pushd {}\; \
	echo {} \; \
	time ../tools/sabre/sabre pe -f ../orig/plate{}_R1.fq.gz -r ../orig/plate{}_R2.fq.gz -b ../../bd.sabre -u {}_nobcd_R1.fq -w {}_nobcd_R2.fq -m 1\; \
	popd \
	::: {1..4} 6
