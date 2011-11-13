# Delete duplicate posts
DELETE bad_rows.*
from wp_posts as bad_rows
inner join (
select post_title, MIN(id) as min_id
from wp_posts
group by post_title
having count(*) > 1
) as good_rows on good_rows.post_title = bad_rows.post_title
and good_rows.min_id <> bad_rows.id

# Find and replace URLS (for url migration)
UPDATE wp_posts SET post_content = REPLACE (post_content, 'http://www.old-domain.com','http://www.new-domain.com');
UPDATE wp_posts SET guid = replace(guid, 'http://www.old-domain.com','http://www.new-domain.com');
UPDATE wp_postmeta SET meta_value = replace(meta_value, 'http://www.old-domain.com', 'http://www.new-domain.com');
UPDATE wp_options SET option_value = replace(option_value, 'http://www.old-domain.com', 'http://www.new-domain.com');