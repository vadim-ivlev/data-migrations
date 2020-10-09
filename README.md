Loading data from SQLite to Postgresql
=======================


load rubrics and ribrics_objects (3m)

    pgloader -v sqlite.load 

load articles (30 min)

    pgloader -v sqlite-articles.load 

You might change postgresql password

log in to db container

    dc exec db psql rgdb 

then

    \du
    \password

add columns to articles

```sql
ALTER TABLE articles
ADD COLUMN process_status TEXT NULL,
ADD COLUMN lemmas TEXT NULL,
ADD COLUMN entities TEXT NULL,
ADD COLUMN rubrics TEXT NULL,
ADD COLUMN ent_rub_text TEXT NULL
;

CREATE INDEX idx_articles_process_status ON articles (process_status);



```


## Export from Postgess to text

To avoid entering  passwords set PGPASSWORD environment variable  
either in ~/.bash_profile  or docker-compose.yml.

    export PGPASSWORD=passw


Dump some data

    dc exec db psql -U root -v -q -d postgres -f /dumps/online1.sql 

Copy to CVS and zip

1. with docker if docker is running
    
        dc exec db psql -U root  -d rgdb -c "COPY (select * from articles limit 100000) TO stdout DELIMITER ',' CSV HEADER" | pigz > articles100000.gz
2. No docker (faster). Database is on a remote computer.

        date; psql -U root -h 134.0.107.93  -d rgdb -c "COPY (SELECT * FROM rubrics) TO stdout DELIMITER ',' CSV HEADER" > /Volumes/ssd/dumps-2020-10-09/rubrics.csv; date

        date; psql -U root -h 134.0.107.93  -d rgdb -c "COPY (SELECT * FROM rubrics_objects) TO stdout DELIMITER ',' CSV HEADER" > /Volumes/ssd/dumps-2020-10-09/rubrics_objects.csv; date
        
        psql -U root -h 134.0.107.93  -d rgdb -c "SELECT count(1) FROM articles"
    
obj_id,announce,authors,date_modified,full-text,images,index_priority,is_active,is_announce,is_paid,link_title,links,obj_kind,projects,release_date,spiegel,title,uannounce,url,migration_status,process_status,lemmatized_text,entities_text,entities_grouped

regexp_replace('full-text', E'[\\n\\r]+', ' ', 'g' ) AS full_text,  <-before images

        date; psql -U root -h 134.0.107.93  -d rgdb -c "COPY (SELECT * FROM articles) TO stdout DELIMITER ',' CSV HEADER" > /Volumes/ssd/dumps-2020-10-09/articles.csv; date

        date; psql -U root -h 134.0.107.93  -d rgdb -c "COPY (SELECT obj_id,announce,authors,date_modified,regexp_replace('full-text', E'[\\n\\r]+', ' ', 'g' ) AS full_text,images,index_priority,is_active,is_announce,is_paid,link_title,links,obj_kind,projects,release_date,spiegel,title,regexp_replace(uannounce, E'[\\n\\r]+', ' ', 'g' ) AS uannounce,url,migration_status,process_status,lemmatized_text,entities_text,regexp_replace(entities_grouped, E'[\\n\\r]+', ' ', 'g' ) AS entities_grouped FROM articles LIMIT 10000000) TO stdout DELIMITER ',' CSV HEADER" > /Volumes/ssd/dumps-2020-10-09/articles.csv; date

        psql -U root -h 134.0.107.93  -d rgdb -c "SELECT count(1) FROM articles"