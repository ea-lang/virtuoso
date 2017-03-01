function getComposers(evt) {
	var composer1_id = $("#composer1-id").val();
	var composer2_id = $("#composer2-id").val();

	var data = {'composer1_id': composer1_id,
				'composer2_id': composer2_id};

	var url = '/major-radar-chart.json';

	$.get(url, data, showRadarChart);
}


$('.composer-radar').on('change', getComposers);

function showRadarChart(results) {

	 var ctx_majorkeys = $("#composerMajorRadar").get(0).getContext("2d");
	 var majorRadarChart = new Chart(ctx_majorkeys,{
		  type: 'radar',
			  data: results,
		  options: options
		});
}



