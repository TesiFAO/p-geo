// Wrap code with module pattern.
(function() {
    var global = this;

    // widget constructor function
    global.CDChart = function() {

        var o = {
            id: 'timeserie',
            seriesOptions: [],//name, data
            colors : Highcharts.getOptions().colors
        };

        var init = function(obj) {
            o = $.extend(true, {}, o, obj);
            /*seriesOptions[i] = {
                name: name,
                data: data
            };*/
            /*o.seriesOptions[0] = {

                "data": [
                    [
                        1400284800000,
                        1371
                    ],
                    [
                        1400544000000,
                        22
                    ]
                ],
                "name": "test"

            }

            o.seriesOptions[1] = {

                data : [
                    [1147651200000,2.2],
                    [1147737600000,2.01],
                    [1147824000000,2.73],
                    [1147910400000,2.83],
                    [1149033600000,2.65]
                ],

                name : "test2"
            }   */

            createChart();
        }

       /* var seriesOptions = [],
            yAxisOptions = [],
            seriesCounter = 0,
            names = ['MSFT', 'AAPL', 'GOOG'],
            colors = Highcharts.getOptions().colors;

        $.each(names, function(i, name) {

            $.getJSON('http://www.highcharts.com/samples/data/jsonp.php?filename='+ name.toLowerCase() +'-c.json&callback=?',	function(data) {

                seriesOptions[i] = {
                    name: name,
                    data: data
                };

                // As we're loading the data asynchronously, we don't know what order it will arrive. So
                // we keep a counter and create the chart when all the data is loaded.
                seriesCounter++;

                if (seriesCounter == names.length) {
                    createChart();
                }
            });
        }); */

        // create the chart when all data is loaded
        var createChart = function() {

            $('#' + o.id).highcharts('StockChart', {

                rangeSelector: {
/*                    inputEnabled: $('#'+ o.id).width() > 480,
                    selected: 4*/
                },

                xAxis: {
                    type: 'datetime',
                    tickInterval: 24 * 3600 * 1000
                    /*plotLines: [{
                        value: 0,
                        width: 2,
                        color: 'silver'
                    }] */
                },

                plotOptions: {
                    series: {
//                        compare: 'percent'
                    }
                },

                tooltip: {
//                    pointFormat: '<span style="color:{series.color}">{series.name}</span>: <b>{point.y}</b> ({point.change}%)<br/>',
                    //valueDecimals: 2
                },

                series: o.seriesOptions
            });
        }



        // public instance methods
        return {
            init: init
        };
    };
})();