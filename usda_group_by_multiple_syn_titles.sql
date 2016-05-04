SELECT syn_title, count(syn_title) FROM usda_not_accepted
GROUP BY syn_title
ORDER BY count(syn_title) DESC