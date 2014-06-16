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

    function downloadLayer(layerName, id) {
        $.ajax({
            url         :   'http://127.0.0.1:5000/start/MODIS/' + layerName,
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
                        document.getElementById(id).innerHTML = 'Download Complete';
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
        url = 'http://127.0.0.1:5001/list/MODIS/MOD13Q1/2014/065';

        $.ajax({
            url: url,
            type: 'GET',
            dataType: 'json',
            success: function (r) {
                for (var i = 0 ; i < r.length ; i++)
                    singleDownload(r[i]);
            },
            error: function (a, b, c) {
                console.log(a);
                console.log(b);
                console.log(c);
            }
        });

    };

    function singleDownload(layerName) {
        $.get('templates.html', function (templates) {
            var view = {
                layerName: layerName
            };
            var template = $(templates).filter('#thread-template').html();
            $('#threads-list').append(Mustache.render(template, view));
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