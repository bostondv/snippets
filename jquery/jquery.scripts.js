/* jquery.scripts.js
 * Global site jQuery scripts
 * ==================================================== */

(function($) {
	$(document).ready(function() {

		// Open rel=external in new window
		$('a[rel="external"]').click( function() {
			window.open( $(this).attr('href') );
			return false;
		});
		
	});
})(jQuery);