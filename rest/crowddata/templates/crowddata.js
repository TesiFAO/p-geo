// Wrap code with module pattern.
(function() {
    var global = this;

    // widget constructor function
    global.Crowddata = function() {

        var o = {
            dropdown: {
                id_container: "dropdown",
                url: "http://168.202.28.214:10900/crowddata/find/commodity"
            },

            slider: {
                id: "daterangeslider",
                url: "http://168.202.28.214:10900/crowddata/find/date"
            },

            map: {
                 id: "map",
                 url:"http://168.202.28.214:10900/crowddata/map/data",
                 mapObject: '',
                 mapMarkers: ''
            },
            timeserie: {
                id: "timeserie",
                url:"http://168.202.28.214:10900/crowddata/timeserie/data",
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
                    var min = response[0].min[0].date.$date
                    var max = response[1].max[0].date.$date
                    $("#"+ o.slider.id).dateRangeSlider({
                        bounds:{ min: new Date(min), max: new Date(max)}},
                        {defaultValues: {min: new Date(min), max: new Date(max)}},
                        {step: 1}
                    );


                    // This event will not ne fired
//                    $("#" + o.slider.id).bind("userValuesChanged", function(e, data){
//                        queryInterface();
//                    });
                },
                error : function(err, b, c) {
                    console.log("error")
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
                        html += '<option value="'+ response[i].code + '">'+response[i].name +'</option>';
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
            startdate = startyear + "," + startmonth  + "," + startday
            enddate = endyear + "," + endmonth  + "," + endday
            $.ajax({
                type : 'GET',
                //url : o.map.url + "/" + code + "/" + startdate + "/" + enddate + "/*",
                url: o.timeserie.url + "/" + code + "/" + startdate + "/" + enddate + "/*",
                success : function(response) {
                    response = (typeof data == 'string') ? $.parseJSON(response) : response;
                    var obj = {}
                    obj.id = o.timeserie.id;
                    obj.seriesOptions = response; //name, data
                    o.timeserie.chartObject = CDChart();
                    o.timeserie.chartObject.init(obj);
                },
                error : function(err, b, c) {
                    console.log("error")
                }
            });
        }

        var queryMap = function(code, startdate, enddate) {
            //@app.route('/crowddata/find/data/<commoditycode>/<startdate>/<enddate>/<bbox>
            var startmonth = startdate.getUTCMonth() +1;
            var startday = startdate.getUTCDate();
            var startyear = startdate.getUTCFullYear();
            var endmonth = enddate.getUTCMonth() +1;
            var endday = enddate.getUTCDate();
            var endyear = enddate.getUTCFullYear();
            startdate = startyear + "," + startmonth  + "," + startday
            enddate = endyear + "," + endmonth  + "," + endday
            var bbox = o.map.mapObject.getBounds();

            var a = { "type": "Polygon",
                "coordinates": [
                    [ [100.0, 0.0], [101.0, 0.0], [101.0, 1.0], [100.0, 1.0], [100.0, 0.0] ]
                ]
            }
            var bounds3 = new L.LatLngBounds(bbox.getSouthWest(), bbox.getNorthEast());
            console.log(bounds)


            $.ajax({
                type : 'GET',
                //url : o.map.url + "/" + code + "/" + startdate + "/" + enddate + "/*",
                url: o.map.url + "/" + code + "/" + startdate + "/" + enddate + "/" +bbox,
                success : function(response) {

                    try {
                        o.map.mapObject.removeLayer(o.map.mapMarkers);
                    }catch (e){}

                    o.map.mapMarkers = L.markerClusterGroup();

                    var markers = response.result;
                    for (var i = 0; i < markers.length; i++) {

                        var m = markers[i];
                        //<h3>Example heading <span class="label label-default">New</span></h3>

                        var content =
                            '<div>' +
                            '<h3>Vendor: ' + m._id.vendorname + '</h3>' +
                            '<h5>' + m._id.commodityname + '</h5>' +
                            '<h5>' + m._id.varietyname + '</h5>' +
                            '<h4>' + m.price + ' <i>'+ m._id.currencysymbol+'/'+ m._id.munitsymbol +'</i></h4>' +
                            '<h4>' + m.price + ' <i>'+ m._id.currencysymbol+'/'+ m._id.munitsymbol +'</i></h4>' +
                            '</div>';
                        var marker = L.marker(new L.LatLng(m._id.geo.coordinates[0], m._id.geo.coordinates[1]));
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