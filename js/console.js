var CONSOLE = (function() {

    var CONFIG = {
        MODIS   :   {
            url_list            :   'http://127.0.0.1:5001/list/MODIS',
            ulr_start_manager   :   'http://127.0.0.1:5000/start/manager/MODIS',
            url_progress        :   'http://127.0.0.1:5000/progress'
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
            document.getElementById('product-label').innerHTML = 'Product <i class="fa fa-refresh fa-spin"></i>';
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
                        document.getElementById('product-label').innerHTML = 'Product';
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
            document.getElementById('from-year-label').innerHTML = 'From: Year <i class="fa fa-refresh fa-spin"></i>';
            document.getElementById('to-year-label').innerHTML = 'To: Year <i class="fa fa-refresh fa-spin"></i>';
            $.ajax({
                url         :   CONFIG[$('#source-list').val()].url_list + '/' + $('#product-list').val(),
                type        :   'GET',
                dataType    :   'json',
                success: function (response) {
                    $('#from-year-list').empty();
                    $('#to-year-list').empty();
                    var s = '';
                    s += '<option>Please Select...</option>';
                    for (var i = response.length - 1 ; i >= 0 ; i--)
                        s += '<option>' + response[i] + '</option>';
                    $('#from-year-list').append(s);
                    $('#to-year-list').append(s);
                    $('#from-year-list').trigger('chosen:updated');
                    $('#to-year-list').trigger('chosen:updated');
                    document.getElementById('from-year-label').innerHTML = 'From: Year';
                    document.getElementById('to-year-label').innerHTML = 'To: Year';
                },
                error: function (a, b, c) {
                    console.log(a);
                    console.log(b);
                    console.log(c);
                }
            });
        });
        $('#from-year-list').on('change', function() {
            document.getElementById('from-day-label').innerHTML = 'From: Day <i class="fa fa-refresh fa-spin"></i>';
            $.ajax({
                url         :   CONFIG[$('#source-list').val()].url_list + '/' + $('#product-list').val() + '/' + $('#from-year-list').val(),
                type        :   'GET',
                dataType    :   'json',
                success: function (response) {
                    $('#from-day-list').empty();
                    var s = '';
                    s += '<option>Please Select...</option>';
                    for (var i = 0; i < response.length ; i++)
                        s += '<option>' + response[i] + '</option>';
                    $('#from-day-list').append(s);
                    $('#from-day-list').trigger('chosen:updated');
                    document.getElementById('from-day-label').innerHTML = 'From: Day';
                },
                error: function (a, b, c) {
                    console.log(a);
                    console.log(b);
                    console.log(c);
                }
            });
        });
        $('#to-year-list').on('change', function() {
            document.getElementById('to-day-label').innerHTML = 'To: Day <i class="fa fa-refresh fa-spin"></i>';
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
                    document.getElementById('to-day-label').innerHTML = 'To: Day';
                },
                error: function (a, b, c) {
                    console.log(a);
                    console.log(b);
                    console.log(c);
                }
            });
        });
    };

    function updateProgress(id, key) {
        timers[key] = setTimeout(function() {
            $.ajax({
                url         :   'http://127.0.0.1:5000/progress/' + key,
                type        :   'GET',
                dataType    :   'json',
                success: function (response) {
                    var percent = (response.progress.progress <= 100 && response.progress.progress >= 0) ? response.progress.progress : 0;
                    var status = response.progress.status;
                    if (status == 'ERROR') {
                        window.clearTimeout(timers[key]);
                        $('#' + id).prop('aria-valuenow', 100);
                        $('#' + id).css('width', 100 + '%');
                        $('#' + id).attr('class', 'progress-bar progress-bar-danger');
                        document.getElementById(id).innerHTML = "<i class='fa fa-warning' style='margin-top: 2px;'></i>";
                    } else {
                        document.getElementById(id).innerHTML = percent + '%';
                        $('#' + id).prop('aria-valuenow', percent);
                        $('#' + id).css('width', percent + '%');
                        if (percent == 100) {
                            window.clearTimeout(timers[key]);
                            $('#' + id).attr('class', 'progress-bar progress-bar-success');
                            document.getElementById(id).innerHTML = "<i class='fa fa-check' style='margin-top: 2px;'></i>";
                        } else {
                            updateProgress(id, key);
                        }
                    }
                },
                error: function (a, b, c) {
                    console.log(a);
                    console.log(b);
                    console.log(c);
                }
            });
        }, parseInt(2500 + (7500 - 2500) * Math.random()));
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

        document.getElementById('threads-list').innerHTML = '<i class="fa fa-refresh fa-spin fa-5x"></i>';

        var url = CONFIG[$('#source-list').val()].ulr_start_manager + '/' +
                  $('#product-list').val() + '/' +
                  $('#from-year-list').val() + '/' +
                  $('#from-day-list').val() + '/' +
                  $('#from-h-list').val() + '/' +
                  $('#to-h-list').val() + '/' +
                  $('#from-v-list').val() + '/' +
                  $('#to-v-list').val();

        $.ajax({

            url: url,
            type: 'GET',
            dataType: 'json',

            success: function (r) {

                var layers = r.layers;

                var s = '';
                s += '<table border="1">';
                for (var i = 0 ; i < 18 ; i++) {
                    s += '<tr>';
                    for (var j = 0 ; j < 36 ; j++)
                        s += '<td style="background-color: #000000; border-color: #000000; width: 20px; height: 20px;" id="' + createMODISID(j, i) + '"></td>';
                    s += '</tr>';
                }
                s += '</table>';
                document.getElementById('threads-list').innerHTML = s;

                for (var i = 0 ; i < layers.length ; i++)
                    singleDownload(layers[i]);

                var min_h = 100;
                var min_v = 100;
                var max_h = 0;
                var max_v = 0;
                for (var i = 0 ; i < layers.length ; i++) {
                    var hv = extractMODISCoordinates(layers[i]);
                    if (hv.h > max_h)
                        max_h = hv.h;
                    if (hv.v > max_v)
                        max_v = hv.v;
                    if (hv.h < min_h)
                        min_h = hv.h
                    if (hv.v < min_v)
                        min_v = hv.v
                }

                for (var i = 0 ; i < layers.length ; i++) {
                    var hv = extractMODISCoordinates(layers[i]);
                    var id = createMODISID(parseInt(hv.h), parseInt(hv.v));
                    updateProgress(id + '-progress', layers[i]);
                }

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
        updateProgress  :   updateProgress,
        killThread      :   killThread,
        download        :   download
    };

})();