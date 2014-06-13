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
            createChart();
        }
        // create the chart when all data is loaded
        var createChart = function() {

            $('#' + o.id).highcharts('StockChart', {

                rangeSelector: {
                    selected : 1,
                    inputEnabled: $('#container').width() > 480
/*                    inputEnabled: $('#'+ o.id).width() > 480,
                    selected: 4*/
                },

                xAxis: {
                    type: 'datetime',
                    tickInterval: 24 * 3600 * 1000
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