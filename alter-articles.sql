--adding NEW columns
ALTER TABLE articles
ADD COLUMN process_status TEXT NULL,
ADD COLUMN lemmas TEXT NULL,
ADD COLUMN entities TEXT NULL,
ADD COLUMN rubrics TEXT NULL,
ADD COLUMN ent_rub_text TEXT NULL
;

CREATE INDEX idx_articles_process_status ON articles (process_status);
