<?php
/* --------------------------------------------
 * This is an example functions.php file
 * with a number of commonly used snippets
 * -------------------------------------------- */



/* --------------------------------------------
 * Hide Meta Boxes
 * -------------------------------------------- */
function remove_metaboxes() {
	remove_meta_box( 'postcustom', 'page', 'normal' );
	remove_meta_box( 'commentstatusdiv', 'page', 'normal' );
	remove_meta_box( 'commentsdiv', 'page', 'normal' );
	remove_meta_box( 'authordiv', 'page', 'normal' );
	remove_meta_box( 'trackbacksdiv', 'page', 'normal' );
	remove_meta_box( 'postexcerpt', 'page', 'normal' );
	remove_meta_box( 'postcustom', 'post', 'normal' );
	remove_meta_box( 'commentstatusdiv', 'post', 'normal' );
	remove_meta_box( 'commentsdiv', 'post', 'normal' );
	remove_meta_box( 'authordiv', 'post', 'normal' );
	remove_meta_box( 'trackbacksdiv', 'post', 'normal' );
	remove_meta_box( 'postexcerpt', 'post', 'normal' );
}
add_action( 'admin_menu' , 'remove_metaboxes' );


/* --------------------------------------------
 * Searchable Custom Post Types
 * -------------------------------------------- */
function searchAll( $query ) {
	if ( $query->is_search ) { $query->set( 'post_type', array( 'site','plugin', 'theme','person' )); }
	return $query;
}
add_filter( 'the_search_query', 'searchAll' );


/* --------------------------------------------
 * Enable GZIP
 * -------------------------------------------- */
if(extension_loaded("zlib") && (ini_get("output_handler") != "ob_gzhandler"))
   add_action('wp', create_function('', '@ob_end_clean();@ini_set("zlib.output_compression", 1);'));


/* --------------------------------------------
 * Register Nav Menus
 * -------------------------------------------- */
function my_register_menus() {
	add_theme_support('nav_menus');
	register_nav_menu('me', 'Connect Me menu');
	register_nav_menu('all', 'Connect All menu');
	register_nav_menu('footer', 'Footer menu');
}
add_action( 'init', 'my_register_menus' );

/* --------------------------------------------
 * Register Sidebar
 * -------------------------------------------- */
register_sidebar(array(
	'name' => 'Connect Sidebar',
	'id' => 'sidebar',
	'description' => 'Widgets in this area will be shown on the right-hand side of selected pages.',
	'before_widget' => '<div id="%1$s" class="widget %2$s">',
	'after_widget'  => '</div>',
));

/* --------------------------------------------
 * High Resolution Icons
 * -------------------------------------------- */
function my_hires_icons() {
	echo '<link rel="icon" href="' . get_bloginfo('stylesheet_directory') . '/images/icon-16.png" sizes="16x16">'."\n";
	echo '<link rel="icon" href="' . get_bloginfo('stylesheet_directory') . '/images/icon-32.png" sizes="32x32">'."\n";
	echo '<link rel="icon" href="' . get_bloginfo('stylesheet_directory') . '/images/icon-64.png" sizes="64x64">'."\n";
	echo '<link rel="icon" href="' . get_bloginfo('stylesheet_directory') . '/images/icon-128.png" sizes="128x128">'."\n";
}
add_action('wp_head', 'my_hires_icons');


/* --------------------------------------------
 * Hide Update Notice
 * -------------------------------------------- */
function hide_update_notice() {
	remove_action( 'admin_notices', 'update_nag', 3 );
}
add_action( 'admin_notices', 'hide_update_notice', 1 );


/* --------------------------------------------
 * Post Thumbnail & Sizes Setup
 * -------------------------------------------- */
function my_post_thumbnail_setup() {
	add_theme_support( 'post-thumbnails' );
	add_image_size( 'slide', 940, 640, true );
	add_image_size( 'testimonial', 80, 40, false );
	add_image_size( 'photos', 800, 500, false );
	add_image_size( 'product-thumb', 350, 200, true );
}
add_action( 'init', 'my_post_thumbnail_setup' );


/* --------------------------------------------
 * Prevent Duplicate Comment Pages
 * -------------------------------------------- */
function canonical_for_comments() {
	global $cpage, $post;
	if ( $cpage > 1 ) :
		echo "\n";
		echo "<link rel='canonical' href='";
		echo get_permalink( $post->ID );
		echo "' />\n";
	 endif;
}
add_action( 'wp_head', 'canonical_for_comments' );


/* --------------------------------------------
 * Load / Unload Scripts
 * -------------------------------------------- */
function my_load_scripts() {
	if (!is_admin()) {
		wp_deregister_script( 'jquery' );
		wp_register_script( 'jquery', 'http://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js');
		wp_enqueue_script( 'jquery' );
		wp_register_script('custom_script',
			get_bloginfo('stylesheet_directory') . '/js/site.js',
			array('jquery'),
			'1.0' );
		wp_enqueue_script('custom_script');
	}
}    
add_action('init', 'my_load_scripts');

/* --------------------------------------------
 * Clean Up Head
 * -------------------------------------------- */
remove_action('wp_head', 'rsd_link'); // Remove Really simple discovery link
remove_action('wp_head', 'wlwmanifest_link'); // Remove Windows Live Writer link
remove_action('wp_head', 'wp_generator'); // Remove the version number

/* --------------------------------------------
 * Remove Curly Quotes
 * -------------------------------------------- */
remove_filter('the_content', 'wptexturize');
remove_filter('comment_text', 'wptexturize');

/* --------------------------------------------
 * Allow HTML in User Profiles
 * -------------------------------------------- */
remove_filter('pre_user_description', 'wp_filter_kses');

/* --------------------------------------------
 * Delete Comment Link
 * -------------------------------------------- */
function delete_comment_link($id) {
  if (current_user_can(&#x27;edit_post&#x27;)) {
    global $post;
    echo &#x27;| &lt;a href=&quot;&#x27;.admin_url(&quot;comment.php?action=cdc&amp;c=$id&amp;redirect_to=/&quot;.$post-&gt;post_name.&quot;/&quot;).&#x27;&quot;&gt;del&lt;/a&gt; &#x27;;
    echo &#x27;| &lt;a href=&quot;&#x27;.admin_url(&quot;comment.php?action=cdc&amp;dt=spam&amp;c=$id&amp;redirect_to=/&quot;.$post-&gt;post_name.&quot;/&quot;).&#x27;&quot;&gt;spam&lt;/a&gt;&#x27;;
  }
}

/* --------------------------------------------
 * Relative Timestamp
 * http://codex.wordpress.org/Function_Reference/human_time_diff
 * human_time_diff( $from, $to )
 * -------------------------------------------- */


/* --------------------------------------------
 * Enable Threaded Comments
 * -------------------------------------------- */
function enable_threaded_comments(){
	if (!is_admin()) {
		if (is_singular() AND comments_open() AND (get_option('thread_comments') == 1))
			wp_enqueue_script('comment-reply');
	}
}
add_action('get_header', 'enable_threaded_comments');


/* --------------------------------------------
 * Custom Excerpts
 * -------------------------------------------- */
// custom excerpt ellipses
function custom_excerpt_more($more) {
	return '…';
}
add_filter('excerpt_more', 'custom_excerpt_more');

// Custom excerpt length
function new_excerpt_length($length) {
	return 100;
}
add_filter('excerpt_length', 'new_excerpt_length');


/* --------------------------------------------
 * Disable Comments on Posts > 1 Month
 * -------------------------------------------- */
function close_comments( $posts ) {

	if ( !is_single() ) { return $posts; }

	if ( time() - strtotime( $posts[0]->post_date_gmt ) > ( 30 * 24 * 60 * 60 ) ) {
	$posts[0]->comment_status = 'closed';
	$posts[0]->ping_status    = 'closed';
	}

return $posts;
}
add_filter( 'the_posts', 'close_comments' );


/* --------------------------------------------
 * Change User Contact Fields
 * -------------------------------------------- */
function change_user_profile( $contactmethods ) {
	// Add Twitter field
	$contactmethods['twitter'] = 'Twitter Name (no @)';
	// Remove AIM, Yahoo IM, Google Talk/Jabber
	unset($contactmethods['aim']);
	unset($contactmethods['yim']);
	unset($contactmethods['jabber']); 
	return $contactmethods;
}
add filter('user_contactmethods','change_user_profile',10,1);
