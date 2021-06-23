all: summary_A.txt summary_B.txt summary_B.pdf

summary_A.txt: FORCE
	quakeio -S -t yaml --human 58658_007_20210426_10.09.54.P.zip \
		| grep -v '\[\]' \
		| grep -v file \
		| grep -v "''" \
		| grep -v '\.units' 

summary_B.txt: FORCE
	python csmip.py

summary_B.pdf: FORCE
	python csmip.py | pandoc -o summary_B.pdf

FORCE:


