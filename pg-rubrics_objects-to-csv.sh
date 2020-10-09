#!/bin/bash

source config.sh

date

psql -U root -h $PGHOST -d rgdb -c \
"COPY 
(
    SELECT * FROM rubrics_objects
)
TO stdout 
DELIMITER ',' 
CSV HEADER
" > $CSVDIR/rubrics_objects.csv

date
