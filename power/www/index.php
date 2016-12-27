<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head> 
<meta http-equiv="Content-Type" content="text/html; charset=utf-8"/> 
<meta http-equiv="refresh" content="600"/>

<title>k34 power</title>

<script type="text/javascript" src="jquery-3.1.0.js" ></script>
<script type="text/javascript" src="Highcharts-4.2.6/js/highcharts.js" ></script>

<script type="text/javascript">
var chart;
$(document).ready(function() {
    var options = {
        chart: {
            renderTo: 'container',
            zoomType: 'x'
        },
        title: {
            text: 'Klyvarevägen 34'
        },
        subtitle: {
            text: document.ontouchstart === undefined ?
                'Click and drag in the plot area to zoom in' :
                'Pinch the chart to zoom in'
        },
        xAxis: {
            type: 'datetime',
        },
        yAxis: {
            title: {
                text: 'power (W)'
            },
            min: 0
        },
        plotOptions: {
            area: {
                fillColor: {
                    linearGradient: { x1: 0, y1: 0, x2: 0, y2: 1},
                    stops: [
                        [0, '#FF0000'],
                        [1, '#FFFACD']
                    ]
                },
                marker: {
                    radius: 2
                },
                lineWidth: 1,
                states: {
                    hover: {
                        lineWidth: 1
                    }
                },
                threshold: null
            }
        },
        legend: {
            layout: 'vertical',
            align: 'right',
            verticalAlign: 'top',
            x: -10,
            y: 100,
            borderWidth: 0
        },
        series: [{
            type: 'area',
            color: '#666666',
            name: 'Power consumption'}]
    }
    // Load data asynchronously using jQuery. On success, add the data
    // to the options and initiate the chart.
    // This data is obtained by exporting a GA custom report to TSV.
    // http://api.jquery.com/jQuery.get/
    jQuery.get('getdata.php', null, function(tsv) {
        var lines = [],
            readings = [],
            date;
        try {
            // split the data return into lines and parse them
            tsv = tsv.split(/\n/g);
            jQuery.each(tsv, function(i, line) {
                line = line.split(/\t/);
                console.log(line);
                date = Date.parse(line[0] + ' UTC');
                readings.push([
                    date,
                    parseInt(line[1].replace(',', ''))
                    ]);
            });
        } catch (e) {}
        options.series[0].data = readings;
        chart = new Highcharts.Chart(options);
    });
});
</script>
</head>
<body>

<div id="container" style="width: 100%; height: 500px; margin: 0 auto"></div>
                                        
</body>
</html>
