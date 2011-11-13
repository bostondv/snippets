<?php 
// Display post thumbnail as background image to slide if exists
if ( has_post_thumbnail() ) {
	$image = wp_get_attachment_image_src( get_post_thumbnail_id(), 'slide' );
	$style = sprintf( 'style="background-image:url(\'%s\')"', esc_attr($image[0]) );
} 

// Get post meta field
$slide_url = get_post_meta( $post->ID, 'my_slide_url', true ); 
