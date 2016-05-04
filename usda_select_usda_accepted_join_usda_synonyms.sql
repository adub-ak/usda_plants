with synonyms AS (SELECT  usda_synonymy.syn_id, usda_synonymy.accept_id, usda_not_accepted.syn_code, usda_not_accepted.syn_title FROM usda_not_accepted
JOIN usda_synonymy
ON usda_not_accepted.syn_id = usda_synonymy.syn_id)
SELECT synonyms.syn_id, synonyms.accept_id, synonyms.syn_code, synonyms.syn_title, usda_accepted.code, usda_accepted.title FROM synonyms
JOIN usda_accepted
ON synonyms.accept_id = usda_accepted.accept_id
ORDER BY synonyms.accept_id, synonyms.syn_id
