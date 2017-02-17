function getPieces(evt) {
	evt.preventDefault();
	var title = $("#title").val();
	var composer = $("#composer").val();
	var period = $("#period").val();
	var level = $("#level").val();
	var key = $("#key").val();

	var url = '/results?title=' + title
								+ '&composer=' + composer 
								+ '&period=' + period
								+ '&level=' + level
								+ '&key=' + key
	$.get(url, showPieces);
}


function showPieces(results) {
	var pieces = results['pieces_query_arr'];
	var str = '';
	
	for (var i = 0; i < pieces.length; i++) {
		
		var piece = pieces[i];

		var piece_id = piece[0];
		var title = piece[1];
		var composer = piece[2];
		var period = piece[3];
		var level = piece[4];

		if (piece[5] === null) {
			var key = 'None';
		}
		else {
			key = piece[5];
		}

		str += '#' + piece_id + ' <strong>' + title + '</strong>'
				+ '<ul>' 
				+ '<li> Composer: ' + composer + '</li>'
				+ '<li> Period: ' + period + '</li>'
				+ '<li> Level: ' + level + '</li>'
				+ '<li> Key: ' + key + '</li>'
				+ '</ul>';
	}

	$('#results').html(str); 
}

$('#title').keyup(getPieces)
$('#composer').on('change', getPieces)
$('#period').on('change', getPieces)
$('#level').on('change', getPieces)
$('#key').on('change', getPieces)
