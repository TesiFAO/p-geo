var CONSOLE = (function() {

    var CONFIG = {
        MODIS   :   {
            url_list    :   'http://127.0.0.1:5001/list/MODIS'
        }
    };

    var timers = {};

    function init() {
        $('#source-list').chosen({disable_search_threshold: 10, allow_single_deselect: true});
        $('#product-list').chosen({disable_search_threshold: 10});
        $('#from-year-list').chosen({disable_search_threshold: 10});
        $('#from-day-list').chosen({disable_search_threshold: 10});
        $('#to-year-list').chosen({disable_search_threshold: 10});
        $('#to-day-list').chosen({disable_search_threshold: 10});
        $('#from-h-list').chosen({disable_search_threshold: 10});
        $('#from-v-list').chosen({disable_search_threshold: 10});
        $('#to-h-list').chosen({disable_search_threshold: 10});
        $('#to-v-list').chosen({disable_search_threshold: 10});
        for (var i = 0 ; i < 36 ; i++) {
            $('.grid-h').append('<option>' + ((i < 10) ? '0' + i : i) + '</option>');
            $('.grid-h').trigger('chosen:updated');
        }
        for (var i = 0 ; i < 18 ; i++) {
            $('.grid-v').append('<option>' + ((i < 10) ? '0' + i : i) + '</option>');
            $('.grid-v').trigger('chosen:updated');
        }
        $('#source-list').on('change', function() {
            try {
                $.ajax({
                    url: CONFIG[$('#source-list').val()].url_list,
                    type: 'GET',
                    dataType: 'json',
                    success: function (response) {
                        $('#product-list').empty();
                        var s = '';
                        s += '<option>Please Select...</option>';
                        for (var i = 0; i < response.length; i++)
                            s += '<option>' + response[i] + '</option>';
                        $('#product-list').append(s);
                        $('#product-list').trigger('chosen:updated');
                    },
                    error: function (a, b, c) {
                        console.log(a);
                        console.log(b);
                        console.log(c);
                    }
                });
            } catch(e) {
                console.log(e);
            }
        });
        $('#product-list').on('change', function() {
            $.ajax({
                url         :   CONFIG[$('#source-list').val()].url_list + '/' + $('#product-list').val(),
                type        :   'GET',
                dataType    :   'json',
                success: function (response) {
                    $('#from-year-list').empty();
                    $('#to-year-list').empty();
                    var s = '';
                    s += '<option>Please Select...</option>';
                    for (var i = 0 ; i < response.length ; i++)
                        s += '<option>' + response[i] + '</option>';
                    $('#from-year-list').append(s);
                    $('#to-year-list').append(s);
                    $('#from-year-list').trigger('chosen:updated');
                    $('#to-year-list').trigger('chosen:updated');
                },
                error: function (a, b, c) {
                    console.log(a);
                    console.log(b);
                    console.log(c);
                }
            });
        });
        $('#from-year-list').on('change', function() {
            $.ajax({
                url         :   CONFIG[$('#source-list').val()].url_list + '/' + $('#product-list').val() + '/' + $('#from-year-list').val(),
                type        :   'GET',
                dataType    :   'json',
                success: function (response) {
                    $('#from-day-list').empty();
                    var s = '';
                    s += '<option>Please Select...</option>';
                    for (var i = 0 ; i < response.length ; i++)
                        s += '<option>' + response[i] + '</option>';
                    $('#from-day-list').append(s);
                    $('#from-day-list').trigger('chosen:updated');
                },
                error: function (a, b, c) {
                    console.log(a);
                    console.log(b);
                    console.log(c);
                }
            });
        });
        $('#to-year-list').on('change', function() {
            $.ajax({
                url         :   CONFIG[$('#source-list').val()].url_list + '/' + $('#product-list').val() + '/' + $('#to-year-list').val(),
                type        :   'GET',
                dataType    :   'json',
                success: function (response) {
                    $('#to-day-list').empty();
                    var s = '';
                    s += '<option>Please Select...</option>';
                    for (var i = 0 ; i < response.length ; i++)
                        s += '<option>' + response[i] + '</option>';
                    $('#to-day-list').append(s);
                    $('#to-day-list').trigger('chosen:updated');
                },
                error: function (a, b, c) {
                    console.log(a);
                    console.log(b);
                    console.log(c);
                }
            });
        });
    };

    function downloadLayer(product, year, day, layerName, id) {
        $.ajax({
            url         :   'http://127.0.0.1:5000/start/MODIS/' + product + '/' + year + '/' + day + '/' + layerName,
            type        :   'GET',
            dataType    :   'json',
            success: function (response) {
                updateProgress(id, response.key);
                $('#kill-' + id).click(function() {
                    killThread(response.key);
                });
            },
            error: function (a, b, c) {
                console.log(a);
                console.log(b);
                console.log(c);
            }
        });
    };

    function updateProgress(id, key) {
        timers[key] = setTimeout(function() {
            $.ajax({
                url         :   'http://127.0.0.1:5000/progress/' + key,
                type        :   'GET',
                dataType    :   'json',
                success: function (response) {
                    $('#' + id).prop('aria-valuenow', response.percent);
                    $('#' + id).css('width', response.percent + '%');
                    document.getElementById(id).innerHTML = response.percent + '%';
                    if (response.percent == 100) {
                        window.clearTimeout(timers[key]);
                        $('#' + id).attr('class', 'progress-bar progress-bar-success');
                        document.getElementById(id).innerHTML = "<i class='fa fa-check' style='margin-top: 2px;'></i>";
                    } else {
                        updateProgress(id, key);
                    }
                },
                error: function (a, b, c) {
                    console.log(a);
                    console.log(b);
                    console.log(c);
                }
            });
        }, 2000);
    };

    function killThread(key) {
        $.ajax({
            url         :   'http://127.0.0.1:5000/kill/' + key,
            type        :   'GET',
            dataType    :   'json',
            success: function (response) {
                window.clearTimeout(timers[key]);
            },
            error: function (a, b, c) {
                console.log(a);
                console.log(b);
                console.log(c);
            }
        });
    };

    function download() {

        var url = CONFIG[$('#source-list').val()].url_list + '/' + $('#product-list').val() + '/' + $('#from-year-list').val() + '/' + $('#from-day-list').val();

        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function (r) {

                var s = '';
                s += '<table border="1">';
                for (var i = 0 ; i < 15 ; i++) {
                    s += '<tr>';
                    for (var j = 0 ; j < 36 ; j++)
                        s += '<td style="background-color: #000000; border-color: #000000; width: 20px; height: 20px;" id="' + createMODISID(j, i) + '"></td>';
                    s += '</tr>';
                }
                s += '</table>';
                $('#threads-list').append(s);

                for (var i = 0 ; i < r.length ; i++)
                    singleDownload(r[i]);

                for (var i = parseInt($('#from-h-list').val()) ; i <= parseInt($('#to-h-list').val()) ; i++) {
                    for (var j = parseInt($('#from-v-list').val()) ; j <= parseInt($('#to-v-list').val()) ; j++) {
                        var id = createMODISID(i, j);
                        for (var z = 0 ; z < r.length ; z++) {
//                            console.log(id + ' VS ' + r[z] + '? ' + r[z].indexOf(id));
                            if (r[z].indexOf(id) > -1) {
                                var product = $('#product-list').val();
                                var year = $('#from-year-list').val();
                                var day = $('#from-day-list').val();
//                                console.log(product + ', ' + year + ', ' + day);
                                downloadLayer(product, year, day, r[z], id + '-progress');
                            }
                        }
                    }
                }

//                for (var i = 0 ; i < 13 ; i++) {
//                    var cs = extractMODISCoordinates(r[i]);
//                    var id = createMODISID(parseInt(cs.h), parseInt(cs.v));
//                    var product = $('#product-list').val();
//                    var year = $('#from-year-list').val();
//                    var day = $('#from-day-list').val();
//                    downloadLayer(product, year, day, r[i], id + '-progress');
//                }

            },
            error: function (a, b, c) {
                console.log(a);
                console.log(b);
                console.log(c);
            }
        });

    };

    function createMODISID(h, v) {
        var s = 'h';
        s += (h < 10) ? '0' : '';
        s += h;
        s += 'v';
        s += (v < 10) ? '0' : '';
        s += v;
        return s;
    }

    function extractMODISCoordinates(layerName) {
        var cs = {};
        cs.h = layerName.substring(1 + layerName.indexOf('h'), 3 + layerName.indexOf('h'));
        cs.v = layerName.substring(1 + layerName.indexOf('v'), 3 + layerName.indexOf('v'));
        return cs;
    }

    function singleDownload(layerName) {
        var cs = extractMODISCoordinates(layerName);
        var id = createMODISID(parseInt(cs.h), parseInt(cs.v));
        $.get('templates.html', function (templates) {
            var view = {
                id: id + '-progress',
                layerName: layerName
            };
            var template = $(templates).filter('#progress-cell').html();
            var render = Mustache.render(template, view);
            document.getElementById(id).innerHTML = render;
        });
    };

    return {
        CONFIG          :   CONFIG,
        init            :   init,
        downloadLayer   :   downloadLayer,
        updateProgress  :   updateProgress,
        killThread      :   killThread,
        download        :   download
    };

})();