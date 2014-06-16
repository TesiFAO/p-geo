var CONSOLE = (function() {

    var CONFIG = {
        MODIS   :   {
            url_products    :   'http://127.0.0.1:5001/list/MODIS'
        }
    };

    var timers = {};

    function init() {
        $('#source-list').chosen({disable_search_threshold: 10});
        $('#product-list').chosen({disable_search_threshold: 10});
        $('#from-list').chosen({disable_search_threshold: 10});
        $('#to-list').chosen({disable_search_threshold: 10});
        $('#source-list').on('change', function() {
            $.ajax({
                url         :   CONFIG[$('#source-list').val()].url_products,
                type        :   'GET',
                dataType    :   'json',
                success: function (response) {
                    $('#product-list').empty();
                    $('#product-list').append('<option>Please select...</option>');
                    var s = '';
                    for (var i = 0 ; i < response.length ; i++)
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

    return {
        CONFIG : CONFIG,
        init : init,
        downloadLayer   :   downloadLayer,
        updateProgress  :   updateProgress,
        killThread  :   killThread
    };

})();