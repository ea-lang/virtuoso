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

	results = "<center>Select a piece by " + composer + ".<br>"
				+ "<form action='/suggestion-results'>"
				+ "Pieces: <select name='piece-id' id='piece-id'>"
				+ pieces_menu
				+ "</select><br><br>"
				+ "Find similar pieces by:<br>"
				+ "<input type='checkbox' name='composer' id='composer' class='filter'> &nbsp; Composer<br>"
				+ "<input type='checkbox' name='period' id='period' class='filter'> &nbsp; Period<br>"
				+ "<input type='checkbox' name='level' id='level' class='filter'> &nbsp; Level<br>"
				+ "<input type='checkbox' name='key' id='key' class='filter'> &nbsp; Key<br>"
				+ "<input type='checkbox' name='tonality' id='tonality' class='filter'> &nbsp; Tonality<br>"
				+ "</form></center>";

	$('#results').html(results); 
		
	$('#piece-id').on('change', getPieces2)	
	$('.filter').on('change', getPieces2)
}


$('#composer-id').on('change', getPieces)

function getPieces2(evt) {

	var data = {'piece_id': $("#piece-id").val(),
				'composer_id': $('#composer').is(':checked'),
				'period': $('#period').is(':checked'),
				'level': $('#level').is(':checked'),
				'key': $('#key').is(':checked'),
				'tonality': $('#tonality').is(':checked')
				}

	var url = '/suggestion-results';

	$.get(url, data, showPieces2);
}


function create_pieces_results(pieces) {

	var str = '';

	for (var i = 0; i < pieces.length; i++) {
			
			var piece = pieces[i];

			var piece_id = piece["piece_id"];
			var title = piece["title"];
			var composer = piece["composer"];
			var period = piece["period"];
			var level = piece["level"];

			if (piece["key"] === null) {
				var key = "None";
			}
			else {
				key = piece["key"];
			}

			if (piece["tonality"] === null) {
				var tonality = "None";
			}
			else {
				tonality = piece["tonality"];
			}


			str += '#' + piece_id + ' <strong>' + title + '</strong><br>'
					// + '<ul>' 
					+ 'Composer: ' + composer + '<br>'
					+ 'Period: ' + period + '<br>'
					+ 'Level: ' + level + '<br>'
					+ 'Key: ' + key + '<br>'
					+ 'Tonality: ' + tonality + '<br><br>'
					// + '</ul>';
	}
	
	return str;
}


function showPieces2(results) {
	var my_piece = results['my_piece']
	var pieces = results['pieces_query_arr']
	var filters = results['filters']
	var count = results['count']

	my_piece_str = create_pieces_results(my_piece)
	pieces_str = create_pieces_results(pieces)

	$('#my_piece').html("<center>Your piece:<br><br>" + my_piece_str + "</center>"); 
	$('#filters').html("<center>" + count.toString() + " similar pieces by filters:<br>" + filters + "<br><br></center>"); 
	$('#results2').html("<center>" + pieces_str + "</center>"); 

}

