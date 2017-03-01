function getComposers(evt) {
	var composer1_id = $("#composer1-id").val();
	var composer2_id = $("#composer2-id").val();
	var tonality = $("input[name=tonality]:checked").val();

	var data = {'composer1_id': composer1_id,
				'composer2_id': composer2_id,
				'tonality': tonality};

	if (data['tonality'] === undefined) {
		data['tonality'] = 'major';
	}

	var url = '/radar-chart.json';

	$.get(url, data, showRadarChart);
}


$('.composer-radar').on('change', getComposers);
$('.tonality').on('change', getComposers);


function showRadarChart(results) {

	 var ctx_keys = $("#composerRadar").get(0).getContext("2d");
	 var myRadarChart = new Chart(ctx_keys,{
		  type: 'radar',
		  data: results,
		  options: options
		});
}



