#!/bin/bash

source config.sh

date

psql -U root -h $PGHOST  -d rgdb -c \
"COPY 
(
    SELECT * FROM rubrics
)
TO stdout 
DELIMITER ',' 
CSV HEADER
" > $CSVDIR/rubrics.csv

date
