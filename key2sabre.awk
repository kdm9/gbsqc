#!/usr/bin/awk -f
BEGIN {
	FS="\t";
	RS="\n";
}
NR > 1 { # skip header row
	printf("%s %s_1.fq %s_2.fq\n", $3, $3, $3);
}
END {
	printf("%d barcodes processed\n", NR - 1) > "/dev/stderr";
}
