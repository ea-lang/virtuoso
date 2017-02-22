function getPieces(evt) {
	var title = $("#title").val();
	var composer_id = $("#composer-id").val();
	var period = $("#period").val();
	var level = $("#level").val();
	var key = $("#key").val();
	var tonality = $("#tonality").val();

	var data = {'title': title, 
				'composer_id': composer_id,
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

	console.log(pieces)
	
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




