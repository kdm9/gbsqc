#!/bin/bash

echo -n "preparing sabre barcode file: "
./sampleSheet2sabre.awk PstI_primers_sample_sheet.txt >bd.sabre
