function getPieces(evt) {
	var composer_id = $("#composer-id").val();

	var data = {'composer_id': composer_id};

	var url = '/find-pieces-by-composer';

	$.get(url, data, showPieces);
}


function showPieces(results) {

	var pieces = results['pieces_arr'];
	var pieces_menu = '';
	
	for (var i = 0; i < pieces.length; i++) {
		
		var piece = pieces[i];

		if ('composer' in piece) {
			var composer = piece["composer"];
		}	
		else {
			var piece_id = piece["piece_id"];
			var title = piece["title"];

			pieces_menu += "<option value=" + piece_id + ">"
			 				+ title + "</option>";
		}
	}

	results = "Select a piece by " + composer + ".<br>"
				+ "<form action='/suggestion-results'>"
				+ "Pieces: <select name='piece-id'>"
				+ pieces_menu
				+ "</select><br><br>"
				+ "Find similar pieces by:<br>"
				+ "Title <input type='text' name='title' id='title'><br>"
				+ "Composer<input type='checkbox' name='composer' value='true'><br>"
				+ "Period<input type='checkbox' name='period' value='true'><br>"
				+ "Level<input type='checkbox' name='level' value='true'><br>"
				+ "Key<input type='checkbox' name='key' value='true'><br>"
				+ "Tonality<input type='checkbox' name='tonality' value='true'><br>"
				+ "<input type='submit'>"
				+ "</form>";

	$('#results').html(results); 
}


$('#composer-id').on('change', getPieces)

