// Wrap code with module pattern.
(function() {
    var global = this;

    // widget constructor function
    global.Crowddata = function() {

        var o = {
            dropdown: {
                id_container: "dropdown",
                url: "http://localhost:8090/wds/rest/crowddata/crowddata/codingsystem/commodity/en"
            },

            slider: {
                id:  "daterangeslider",
                url: "http://localhost:8090/wds/rest/crowddata/crowddata/codes/data/daterange"
            },

            map: {
                 id: "map",
                 url:"http://localhost:8090/wds/rest/crowddata/crowddata/geo/data/'{codes}'/{startdate}/{enddate}/{geojson}/en",                 mapObject: '',
                 mapMarkers: ''
            },
            timeserie: {
                id: "timeserie",
                url:"http://localhost:8090/wds/rest/crowddata/crowddata/timeserie/data/'{codes}'/{startdate}/{enddate}/{geojson}/en",
                chartObject: ""
            },
            apply_id: 'apply'

        };

        // private instance methods
        var init = function(obj) {
            o = $.extend(true, {}, o, obj);
            createDropdown();
            createDateRangeSlider();
            createMap();
            $("#" + o.apply_id).click(function(){
                queryInterface();
            });
        };

        var createDateRangeSlider = function() {
            $.ajax({
                type : 'GET',
                url : o.slider.url,
                success : function(response) {
                    response = ( typeof response == 'string')? $.parseJSON( response): response;
                    var min = response[0];
                    var max = response[1];
                    $("#"+ o.slider.id).dateRangeSlider({
                        bounds:{ min: new Date(min), max: new Date(max)}},
                        {defaultValues: {min: new Date(min), max: new Date(max)}},
                        {step: 1}
                    );
                },
                error : function(err, b, c) {
                    console.log("error: " , err)
                }
            });
        }

        var createDropdown = function() {

            // get coding system
            $.ajax({
                type : 'GET',
                url : o.dropdown.url,
                success : function(response) {
                    var dropdowndID = randomID();
                    o.dropdown.id = dropdowndID;

                    // TODO: dynamic width
//                    var html = '<select multiple id="'+ dropdowndID+'" data-placeholder="Choose a Commodity...">';
                    var html = '<select id="'+ dropdowndID+'" data-placeholder="Choose a Commodity...">';
                    for(var i=0; i < response.length; i++)
                        html += '<option value="'+ response[i][0] + '">'+response[i][1] +'</option>';
                    html += '</select>';

                    $('#' + o.dropdown.id_container).empty();
                    $('#' + o.dropdown.id_container).append(html);

                    try {
                        $('#' + dropdowndID).chosen({disable_search_threshold:10, width: '100%'});
                    }  catch (e) {}

                    // enable on click
                    var _this = this;
                    $( "#" + dropdowndID ).change({},  function (event) {
                        queryInterface();
                    });
                },
                error : function(err, b, c) {
                    console.log("error")
                }
            });
        }

        var createMap = function() {
            o.map.mapObject = L.map(o.map.id).setView([0, 0], 1);
            L.tileLayer('https://{s}.tiles.mapbox.com/v3/{id}/{z}/{x}/{y}.png', {
                maxZoom: 18,
                attribution: '',
                id: 'examples.map-i86knfo3'
            }).addTo(o.map.mapObject);

        }

        var queryInterface = function() {
            var rangeValues = $("#"+ o.slider.id).dateRangeSlider("values");

            var code = $("#" + o.dropdown.id).val();

            queryMap(code, rangeValues.min, rangeValues.max)
            queryTimeserieChart(code, rangeValues.min, rangeValues.max)
        }

        var queryTimeserieChart = function(code, startdate, enddate) {
            var startmonth = startdate.getUTCMonth() +1;
            var startday = startdate.getUTCDate();
            var startyear = startdate.getUTCFullYear();
            var endmonth = enddate.getUTCMonth() +1;
            var endday = enddate.getUTCDate();
            var endyear = enddate.getUTCFullYear();
            startdate = startyear + "-" + startmonth  + "-" + startday
            enddate = endyear + "-" + endmonth  + "-" + endday

            var bounds = o.map.mapObject.getBounds();
            var sw = bounds.getSouthWest();
            var ne = bounds.getNorthEast();
            var BBOX = (sw.lat ) + ',' + (sw.lng) +',' + (ne.lat) + ',' + (ne.lng);

            var url = o.timeserie.url;
            url = url.replace("{startdate}", startdate)
            url = url.replace("{enddate}", enddate)
            url = url.replace("{codes}", code)
            url = url.replace("{geojson}", BBOX)

            $.ajax({
                type : 'GET',
                url: url,
                success : function(response) {
                    var response = (typeof data === 'string') ? $.parseJSON(response) : response;
                    var obj = {}
                    obj.id = o.timeserie.id;

                    //console.log(response);
                    var series = [];
                    var serieIndex = 0;

                    for (var i = 0; i < response.length; i++) {
                       // check serie name
                       var name = response[i][0] + " - " + response[i][3]
                       if ( series[serieIndex] == null )  {
                           series[serieIndex] = {};
                           series[serieIndex].name = name;
                           series[serieIndex].data = [];
                       }
                       else if ( series[serieIndex].name != name) {
                           serieIndex++;
                           series[serieIndex] = {};
                           series[serieIndex].name = name;
                           series[serieIndex].data = [];
                       }

                        // get data
                        var myDate=response[i][1];
                        myDate=myDate.split("-");
                        var newDate=myDate[0]+","+myDate[1]+","+myDate[2];

                        // add data serie
                        series[serieIndex].data.push([ new Date(newDate).getTime(), parseFloat(response[i][2]) ]);
                    }

                    // parse json
                    obj.seriesOptions = series;


                    //obj.seriesOptions = response;
                   /*obj.seriesOptions = [
                        {
                            "data": [[1400284800000,1371],[ 1400544000000,22]],
                            "name": "test"
                        },
                        {
                            "data": [[1400284800000,3],[ 1400544000000,12]],
                            "name": "test2"
                        }
                    ]; //name, data*/

                    o.timeserie.chartObject = CDChart();
                    o.timeserie.chartObject.init(obj);
                },
                error : function(err, b, c) {
                    console.log("error")
                }
            });
        }

        var queryMap = function(code, startdate, enddate) {
            var startmonth = startdate.getUTCMonth() +1;
            var startday = startdate.getUTCDate();
            var startyear = startdate.getUTCFullYear();
            var endmonth = enddate.getUTCMonth() +1;
            var endday = enddate.getUTCDate();
            var endyear = enddate.getUTCFullYear();
            startdate = startyear + "-" + startmonth  + "-" + startday
            enddate = endyear + "-" + endmonth  + "-" + endday

            var bounds = o.map.mapObject.getBounds();
            var sw = bounds.getSouthWest();
            var ne = bounds.getNorthEast();
            var BBOX = (sw.lat ) + ',' + (sw.lng) +',' + (ne.lat) + ',' + (ne.lng);

            var url = o.map.url;
            url = url.replace("{startdate}", startdate)
            url = url.replace("{enddate}", enddate)
            url = url.replace("{codes}", code)
            url = url.replace("{geojson}", BBOX)
            try {  o.map.mapObject.removeLayer(o.map.mapMarkers); }catch (e){}
            $.ajax({
                type : 'GET',
                url : url,
                //url: o.map.url + "/" + code + "/" + startdate + "/" + enddate + "/" +bbox,
                success : function(response) {
//                    o.map.mapObject.removeLayer(o.map.mapMarkers);
//                    o.map.mapMarkers = L.markerClusterGroup();
//                    var markers = L.markerClusterGroup();
//                    var obj = ( typeof response == 'object')? $.parseJSON( response[0]): response[0];
//                    var geoJsonLayer = L.geoJson(obj, {
//                        onEachFeature: function (feature, layer) {
//                            var fp = feature.properties;
//                            var content =
//                                '<div>' +
//                                '<h3>Commodity: ' + fp.commodityname + '</h3>' +
//                                '<h5>' + fp.varietyname + '</h5>' +
//                                '<h4>' + fp.price + ' <i>'+ fp.munitname+'/'+ fp.currencyname +'</i></h4>' +
//                                '</div>';
//                            layer.bindPopup(content);
//                        }
//                    });
//                    o.map.mapMarkers.addLayer(geoJsonLayer);
//                    o.map.mapObject.addLayer(o.map.mapMarkers)

                    try {
                        o.map.mapObject.removeLayer(o.map.mapMarkers);
                    }catch (e){}

                    o.map.mapMarkers = L.markerClusterGroup();

                    var response = ( typeof response === 'string')? $.parseJSON( response): response;
                    for (var i = 0; i < response.length; i++) {

                        var m = response[i];
                        var content =
                            '<div>' +
                            '<h3>Commodity: ' + m[0] + '</h3>' +
                            '<h4>' + m[1] + '</h4>' +
                            '<h5>' + m[4] + ' ' + m[2] + '/' + m[3]+ '</h5>' +
                            '</div>';
                        var marker = L.marker(new L.LatLng(m[5], m[6]));
                        marker.bindPopup(content);
                        o.map.mapMarkers.addLayer(marker);
                    }

                    o.map.mapObject.addLayer(o.map.mapMarkers);
                },
                error : function(err, b, c) {
                    console.log("error")
                }
            });
        }

        var randomID = function() {
            var randLetter = Math.random().toString(36).substring(7);
            return (randLetter + Date.now()).toLocaleLowerCase();
        };

        // public instance methods
        return {
            init: init
        };
    };
})();