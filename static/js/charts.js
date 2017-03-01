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

