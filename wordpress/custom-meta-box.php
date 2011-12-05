<?php
/* --------------------------------------------
 * Add custom meta boxes
 * http://codex.wordpress.org/Function_Reference/add_meta_box
 * -------------------------------------------- */

add_action( 'add_meta_boxes', 'my_create_metaboxes' );
function my_create_metaboxes() {
	add_meta_box(
		'my_slides_meta', 
		__( 'Slide Details' ), 
		'my_slides_meta_cb', 
		'slides', 
		'normal', 
		'high'
	);
}

// Sets inner meta box content
function my_slides_meta_cb() {
	$values = get_post_custom( $post->ID );
	$text = isset( $values['my_slides_url'] ) ? esc_attr( $values['my_slides_url'][0] ) : '';
	wp_nonce_field( 'my_meta_box_nonce', 'meta_box_nonce' );

	// The actual fields for data entry
	echo '<label for="my_slides_url">';
	echo __( 'URL' ) . ':';
	echo '</label> ';
	echo '<input type="text" id="my_slides_url" name="my_slides_url" value="' . $text . '">';
}

// Saves post data
add_action( 'save_post', 'my_save_postdata' );
function my_save_postdata( $post_id ) {

	// Bail if we're doing an auto save
	if( defined( 'DOING_AUTOSAVE' ) && DOING_AUTOSAVE ) return;
	
	// if our nonce isn't there, or we can't verify it, bail
	if( !isset( $_POST['meta_box_nonce'] ) || !wp_verify_nonce( $_POST['meta_box_nonce'], 'my_meta_box_nonce' ) ) return;
	
	// if our current user can't edit this post, bail
	if( !current_user_can( 'edit_post' ) ) return;

	// OK, we're authenticated: we need to find and save the data

	// now we can actually save the data
	$allowed = array( 
		'a' => array( // on allow a tags
			'href' => array() // and those anchords can only have href attribute
		)
	);

	// Make sure your data is set before trying to save it
	if( isset( $_POST['my_slides_url'] ) )
		update_post_meta( $post_id, 'my_slides_url', wp_kses( $_POST['my_slides_url'], $allowed ) );

}