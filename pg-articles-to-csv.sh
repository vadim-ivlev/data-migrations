#!/bin/bash

source config.sh

date

psql -U root -h $PGHOST -d rgdb -c \
"COPY 
(
SELECT 
    obj_id,
    regexp_replace(announce, E'[\\n\\r]+', ' ', 'g' ) AS announce,
    authors,
    date_modified,
    regexp_replace(\"full-text\", E'[\\n\\r]+', ' ', 'g' ) AS full_text,
    images,
    index_priority,
    is_active,
    is_announce,
    is_paid,
    regexp_replace(link_title, E'[\\n\\r]+', ' ', 'g' ) AS link_title,
    links,
    obj_kind,
    projects,
    release_date,
    regexp_replace(spiegel, E'[\\n\\r]+', ' ', 'g' ) AS spiegel,
    regexp_replace(title, E'[\\n\\r]+', ' ', 'g' ) AS title,
    regexp_replace(uannounce, E'[\\n\\r]+', ' ', 'g' ) AS uannounce,
    url,
    migration_status,
    process_status,
    lemmatized_text,
    entities_text,
    regexp_replace(entities_grouped, E'[\\n\\r]+', ' ', 'g' ) AS entities_grouped 
FROM articles 
LIMIT 2000000
) 
TO stdout 
DELIMITER ',' 
CSV HEADER
" > $CSVDIR/articles.csv

date
