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
UPDATE wp_posts SET post_content = REPLACE (post_content, 'http://old.com','http://new.com');
UPDATE wp_posts SET guid = REPLACE (guid, 'http://old.com','http://new.com');
UPDATE wp_postmeta SET meta_value = REPLACE (meta_value, 'http://old.com', 'http://new.com');
UPDATE wp_options SET option_value = REPLACE (option_value, 'http://old.com', 'http://new.com') WHERE option_name = 'home' OR option_name = 'siteurl';

# Assign all articles by Author B to Author A
UPDATE wp_posts SET post_author = 'new-author-id' WHERE post_author = 'old-author-id';

# Delete all spam posts
DELETE FROM wp_comments WHERE comment_approved = 'spam';

# Rename tables
RENAME table `wp_commentmeta` TO `wp_pmlo_commentmeta`;

SELECT * FROM `wp_pmlo_options` WHERE `option_name` LIKE '%wp_%';
UPDATE `wp_pmlo_options` SET `option_name` = replace(`option_name`, 'find', 'replace');

SELECT * FROM `wp_pmlo_usermeta` WHERE `meta_key` LIKE '%wp_%';
UPDATE `wp_pmlo_usermeta` SET `meta_key` = replace(`meta_key`, 'find', 'replace');

# Search posts for bad stuff
SELECT * FROM wp_pmlo_posts WHERE post_content LIKE '%<iframe%'
UNION
SELECT * FROM wp_pmlo_posts WHERE post_content LIKE '%<noscript%'
UNION
SELECT * FROM wp_pmlo_posts WHERE post_content LIKE '%display:%';