var options = {
    responsive: true
  };


var ctx_keys = $("#composerRadar").get(0).getContext("2d");

var myRadarChart = new Chart(ctx_keys,{
    type: 'radar',
    data: {
        "labels": ["C", "G", "D", "A", "E", "B", "Gb/F#", "Db", "Ab", "Eb", "Bb", "F"],
        "datasets": [
          {
              "label": "None",
              "backgroundColor": "rgba(88,146,227,0.2)",
              "borderColor": "rgba(88,146,227,1)",
              "pointBackgroundColor": "rgba(88,146,227,1)",
              "pointBorderColor": "#fff",
              "pointHoverBackgroundColor": "#fff",
              "pointHoverBorderColor": "rgba(88,146,227,1)",
              "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
          },
          {
              "label": "None",
              "backgroundColor": "rgba(255,99,132,0.2)",
              "borderColor": "rgba(255,99,132,1)",
              "pointBackgroundColor": "rgba(255,99,132,1)",
              "pointBorderColor": "#fff",
              "pointHoverBackgroundColor": "#fff",
              "pointHoverBorderColor": "rgba(255,99,132,1)",
              "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
          }
      ]
    },
    options: options
  });




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









var ctx_periods = $("#periodRadar").get(0).getContext("2d");

var myRadarChart2 = new Chart(ctx_periods,{
    type: 'radar',
    data: {
        "labels": ["C", "G", "D", "A", "E", "B", "Gb/F#", "Db", "Ab", "Eb", "Bb", "F"],
        "datasets": [
          {
              "label": "None",
              "backgroundColor": "rgba(88,146,227,0.2)",
              "borderColor": "rgba(88,146,227,1)",
              "pointBackgroundColor": "rgba(88,146,227,1)",
              "pointBorderColor": "#fff",
              "pointHoverBackgroundColor": "#fff",
              "pointHoverBorderColor": "rgba(88,146,227,1)",
              "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
          },
          {
              "label": "None",
              "backgroundColor": "rgba(255,99,132,0.2)",
              "borderColor": "rgba(255,99,132,1)",
              "pointBackgroundColor": "rgba(255,99,132,1)",
              "pointBorderColor": "#fff",
              "pointHoverBackgroundColor": "#fff",
              "pointHoverBorderColor": "rgba(255,99,132,1)",
              "data": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
          }
      ]
    },
    options: options
  });






$('.period-radar').on('change', getPeriods);
$('.tonality2').on('change', getPeriods);



function getPeriods(evt) {
  var period1 = $("#period1").val();
  var period2 = $("#period2").val();
  var tonality = $("input[name=tonality2]:checked").val();

  var data = {'period1': period1,
        'period2': period2,
        'tonality': tonality};

  if (data['tonality'] === undefined) {
    data['tonality'] = 'major';
  }

  var url = '/radar-chart.json';

  $.get(url, data, showRadarChart);
}



