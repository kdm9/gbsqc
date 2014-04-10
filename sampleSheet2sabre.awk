#!/usr/bin/awk -f
BEGIN {
	FS="\t";
	RS="\n";
	samps=0;
}
NR > 1 && $2 !~ /\*/ { # skip header row
	printf("%s %s_1.fq %s_2.fq\n", $2, $2, $2);
	samps++;
}
END {
	printf("%d samples processed\n", samps) > "/dev/stderr";
}
