#!/bin/bash

cd tools
git submodule update --init --recursive
for i in sabre  scythe  seqtkwithpatches  sickle
do
       	pushd $i
	make -j8
       	popd
done
