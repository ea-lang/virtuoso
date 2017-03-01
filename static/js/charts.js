var options = {
    responsive: true
  };

var ctx_period = $("#periodPie").get(0).getContext("2d");
$.get("/periods-counts.json", function (data) {
  var myPieChart = new Chart(ctx_period,{
	  type: 'doughnut',
		data: data,
	  options: options
});
});


var ctx_majorkey = $("#majorkeyPie").get(0).getContext("2d");
$.get("/majorkey-counts.json", function (data) {
  var myPieChart = new Chart(ctx_majorkey,{
	  type: 'doughnut',
		data: data,
	  options: options
});
});


var ctx_minorkey = $("#minorkeyPie").get(0).getContext("2d");
$.get("/minorkey-counts.json", function (data) {
  var myPieChart = new Chart(ctx_minorkey,{
	  type: 'doughnut',
		data: data,
	  options: options
});
});


var ctx_level = $("#levelPie").get(0).getContext("2d");
$.get("/level-counts.json", function (data) {
  var myPieChart = new Chart(ctx_level,{
	  type: 'doughnut',
		data: data,
	  options: options
});
});



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
