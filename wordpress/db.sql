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
RENAME table `wp_comments` TO `wp_pmlo_comments`;
RENAME table `wp_links` TO `wp_pmlo_links`;
RENAME table `wp_options` TO `wp_pmlo_options`;
RENAME table `wp_postmeta` TO `wp_pmlo_postmeta`;
RENAME table `wp_posts` TO `wp_pmlo_posts`;
RENAME table `wp_terms` TO `wp_pmlo_terms`;
RENAME table `wp_term_relationships` TO `wp_pmlo_term_relationships`;
RENAME table `wp_term_taxonomy` TO `wp_pmlo_term_taxonomy`;
RENAME table `wp_usermeta` TO `wp_pmlo_usermeta`;
RENAME table `wp_users` TO `wp_pmlo_users`;

RENAME table `wp_wpmlautoresponderemails` TO `wp_pmlo_wpmlautoresponderemails`;
RENAME table `wp_wpmlautoresponders` TO `wp_pmlo_wpmlautoresponders`;
RENAME table `wp_wpmlautoresponderslists` TO `wp_pmlo_wpmlautoresponderslists`;
RENAME table `wp_wpmlcountries` TO `wp_pmlo_wpmlcountries`;
RENAME table `wp_wpmlemails` TO `wp_pmlo_wpmlemails`;
RENAME table `wp_wpmlfields` TO `wp_pmlo_wpmlfields`;
RENAME table `wp_wpmlfieldslists` TO `wp_pmlo_wpmlfieldslists`;
RENAME table `wp_wpmlgroups` TO `wp_pmlo_wpmlgroups`;
RENAME table `wp_wpmlhistoriesattachments` TO `wp_pmlo_wpmlhistoriesattachments`;
RENAME table `wp_wpmlhistorieslists` TO `wp_pmlo_wpmlhistorieslists`;
RENAME table `wp_wpmlhistory` TO `wp_pmlo_wpmlhistory`;
RENAME table `wp_wpmllatestposts` TO `wp_pmlo_wpmllatestposts`;
RENAME table `wp_wpmlmailinglists` TO `wp_pmlo_wpmlmailinglists`;
RENAME table `wp_wpmlorders` TO `wp_pmlo_wpmlorders`; 
RENAME table `wp_wpmlposts` TO `wp_pmlo_wpmlposts`;
RENAME table `wp_wpmlqueue` TO `wp_pmlo_wpmlqueue`;
RENAME table `wp_wpmlsubscribers` TO `wp_pmlo_wpmlsubscribers`;
RENAME table `wp_wpmlsubscriberslists` TO `wp_pmlo_wpmlsubscriberslists`; 
RENAME table `wp_wpmltemplates` TO `wp_pmlo_wpmltemplates`;
RENAME table `wp_wpmlthemes` TO `wp_pmlo_wpmlthemes`;

SELECT * FROM `wp_pmlo_options` WHERE `option_name` LIKE '%wp_%';
UPDATE `wp_pmlo_options` SET `option_name` = replace(`option_name`, 'find', 'replace');

SELECT * FROM `wp_pmlo_usermeta` WHERE `meta_key` LIKE '%wp_%';
UPDATE `wp_pmlo_usermeta` SET `meta_key` = replace(`meta_key`, 'find', 'replace');