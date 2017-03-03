var options = {
    responsive: true
  };


var ctx_keys = $("#radarChart").get(0).getContext("2d");
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


function getData(evt) {

  var filter1 = ($("#filter1").val() !== undefined ? $("#filter1").val() : ""); 
	var filter2 = ($("#filter2").val() !== undefined ? $("#filter2").val() : ""); 
	var tonality = $("input[name=tonality]:checked").val();
  var category = $('#category').val();

	var data = {'filter1': filter1,
				'filter2': filter2,
				'tonality': tonality,
        'category': category};

	var url = '/radar-chart.json';

	$.get(url, data, showRadarChart);
}



$('.tonality').on('change', getData);


$('#category').on('change', renderMenus)



function renderMenus() {
  var data = {'category': $('#category').val()};

  var url = '/render-menus.json'

  $.get(url, data, showMenus)
}


function showMenus(results) {
  var options_dict = results;

    if (jQuery.isEmptyObject(options_dict)) {
      $('#select-menu').html(''); 
      data = {'all': $("input[name=tonality]:checked").val()};
      var url = "/radar-chart.json"
      $.get(url, data, showRadarChart)
    } 

    else {
      var menu = '';
      var label = options_dict['category'][0].toUpperCase() + options_dict['category'].substring(1);

      if (options_dict['category'] === 'composer') {

        var composers = options_dict['options']
        for (var i = 0; i < composers.length; i++) {
            var composer = composers[i];
            menu += "<option value=" + composer["composer_id"] + ">"
                  + composer["name"] + " (" + composer["piece_count"] + " pieces)</option>";
          }
      }

      if (options_dict['category'] === 'period' || options_dict['category'] === 'level') {

        var options = options_dict['options']
        for (var i = 0; i < options.length; i++) {
            var option = options[i];
            menu += "<option value=" + option["option"] + ">"
                  + option["option"] + " (" + option["piece_count"] + " pieces)</option>";
          }
      }

      var menus = "<center>" + label + " 1: <select id=\"filter1\" class=\"options\" name=" + options_dict["category"] + ">"
                  + "<option selected></option>" 
                  + menu
                  + "</select> &nbsp;" 
                  + label + " 2: <select id=\"filter2\" class=\"options\" name=" + options_dict["category"] + ">"
                  + "<option selected></option>" 
                  + menu
                  + "</select> </center>"

      $('#select-menu').html(menus); 
      $('.options').on('change', getData);
    }
}


function showRadarChart(results) {

	 var ctx_keys = $("#radarChart").get(0).getContext("2d");
	 var myRadarChart = new Chart(ctx_keys,{
		  type: 'radar',
		  data: results,
		  options: options
		});
}


