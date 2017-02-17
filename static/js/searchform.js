function getPieces(evt) {
	var title = $("#title").val();
	var composer = $("#composer").val();
	var period = $("#period").val();
	var level = $("#level").val();
	var key = $("#key").val();
	var tonality = $("#tonality").val();

	var data = {'title': title, 
				'composer': composer,
				'period': period,
				'level': level,
				'key': key,
				'tonality': tonality};

	var url = '/results';

	$.get(url, data, showPieces);
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

		if (piece[6] === null) {
			var tonality = 'None';
		}
		else {
			tonality = piece[6];
		}

		str += '#' + piece_id + ' <strong>' + title + '</strong>'
				+ '<ul>' 
				+ '<li> Composer: ' + composer + '</li>'
				+ '<li> Period: ' + period + '</li>'
				+ '<li> Level: ' + level + '</li>'
				+ '<li> Key: ' + key + '</li>'
				+ '<li> Tonality: ' + tonality + '</li>'
				+ '</ul>';
	}

	$('#results').html(str); 
}

$('#title').keyup(getPieces)
$('.filter').on('change', getPieces)




