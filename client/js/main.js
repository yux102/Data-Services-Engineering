//written by JingXuan Li
//javascript file for index page, using Vuejs framework


// url constant
const data_url = "http://127.0.0.1:5000/";

// Vuejs framework
var v = new Vue({
    el: '#index',
    // component: {
    //     'time-eater': 'time-eater'
    // },
    data: {
        rows: '',
        year: '2018',
        country: 'Russia',
        c : {},
        code: 'RU',

    },
    // computed: {
    //     img_code: function(){
    //         if(this.code == 'KR/JP'){
    //             var imgcode= "../client/svg/KR.svg";
    //             return imgcode;
    //         }
    //         var imgcode= "../client/svg/"+this.code+".svg";
    //         return imgcode;
    //     },
    //     korea_check: function(){
    //         if(this.country == "Korea/Japan"){
    //             this.country = "Korea&Japan";
    //             return this.country
    //         };
    //
    //         return this.country
    //     }
    // },
    mounted: function () {
        var self = this;

        $.ajax({
            url: data_url + 'getallevents/',
            method: 'GET',
            success: function (data) {
                self.rows = data;
            },
            error: function (error) {
                console.log(error);
            }
        });

        //get top10
        $.ajax({
            url: data_url + 'gettop/',
            method: 'GET',
            async: false,
            success: function (data) {
                console.log(data);
                country=[];
                dataset = [];
                for(var i = 0;i< data.length; i++){
                    country.push(data[i]['Country']);
                    dataset.push(data[i]['Count'])
                }

                //chart
                var ctx = document.getElementById("myChart").getContext('2d');
                var myChart = new Chart(ctx, {
                    type: 'bar',
                    data: {
                        labels:country,
                        datasets: [{
                            label: '# of qualification from 1930 to 2014',
                            data: dataset,
                            backgroundColor: 'rgba(54, 162, 235, 0.2)',
                            hoverBackgroundColor : 'rgba(54, 162, 235, 0.5)',
                            borderColor: 'rgba(54, 162, 235, 1)',
                            borderWidth: 1,
                            fill: 'red'
                        }],

                    },
                    options: {
                        scales: {
                            yAxes: [{
                                gridLines: {
                                    display : false    //不显示表格线
                                },
                                ticks: {
                                    beginAtZero:true
                                }
                            }]
                        },
                        onClick: function(c,i) {
                            e = i[0];
                            self.country = this.data.labels[e._index];
                            console.log(self.country);

                            //call funtion show country info and map
                            self.mapping();
                        }
                    }

                });
            },
            error : function (error) {
                console.log(error);
            }
        });

        this.info();
        // google.maps.event.addDomListener(window, 'load', this.google());


    },

    methods: {
        info : function(){
        	const available=['Russia', 'Brazil','South Africa', 'Germany', 'Korea/Japan', 'France', 'USA', 'Italy',
        					'Mexico', 'Spain', 'Argentina', 'England', 'Chile', 'Sweden', 'Switzerland', 'Uruguay']
        	this.country= this.capitalize(this.country)


        	var index= available.indexOf(this.country)
        	if (index<0){
        			alert("Sorry, country not in record!");
        			return 0
        	};

        	var self = this;
		        $.ajax({
		            url: data_url + 'querybycountry/'+this.korea_check,
		            method: 'GET',
		            success: function (data) {
		                    self.c=data[0];
		                    self.code=data[0]['CountryCode'];
		                    document.getElementById('jpflag').style.display="none";
		                    if(self.code == 'KR/JP'){
		                        document.getElementById('jpflag').style.display="block";
		                    }
		            },
		            error: function (error) {
		                    console.log(error);
		            }
		    });


        },
        capitalize: function(string){
            return string.charAt(0).toUpperCase() + string.slice(1);
        },

        mapping: function(){

            this.info();

            var self= this;
            $.ajax({
                url: google_url + 'country/'+this.country,
                method: 'GET',
                async: false,
                success: function (data) {

                    var country_coordinate=data[data.length-1]['Country Coordinate'].split(',');
                    self.map_center=[parseFloat(country_coordinate[0]), parseFloat(country_coordinate[1])];

                    self.stadium_coordinates=[];

                    self.stadium_names=[];
                    self.stadium_address=[];

                    for(var i = 0;i<data.length-1; i++){
                        if (data[i]["Coordinate"] == null){
                            continue;
                        };
                            var latlong=data[i]["Coordinate"].split(',');
                            var gloc = new google.maps.LatLng(parseFloat(latlong[0]), parseFloat(latlong[1]));
                            self.stadium_coordinates.push(gloc);
                            self.stadium_names.push(data[i]["Stadium"]);
                            self.stadium_address.push(data[i]["Address"]);

                    };


                },
                error : function (error) {
                    console.log(error);
                }

            });
            this.google();
        },
        table: function(new_c){
            this.country=new_c[0];
            this.year = new_c[1];
            this.mapping();
        },

        google: function () {
            console.log('googling');
            var myCenter=new google.maps.LatLng(this.map_center[0], this.map_center[1]);
            var mapProp = {
              center:myCenter,
              zoom:10,
              mapTypeId:google.maps.MapTypeId.ROADMAP
              };

            var map=new google.maps.Map(document.getElementById("googleMap"),mapProp);
            var infowindow = new google.maps.InfoWindow();
            console.log(this.stadium_coordinates);
            var markers = [];

            for(var i = 0;i< this.stadium_coordinates.length; i++){
                var gmarker = new google.maps.Marker({
                                            position : this.stadium_coordinates[i],
                                            map : map});
                markers.push(gmarker);

                var content= '<div><strong>' + this.stadium_names[i] + '</strong><br>' +
                            'Address: ' + this.stadium_address[i] + '<br></div>';

                var infowindow = new google.maps.InfoWindow();

                google.maps.event.addListener(gmarker,'click', (function(gmarker,content,infowindow){
                        return function() {
                            infowindow.setContent(content);
                            infowindow.open(map,gmarker);
                        };
                    })(gmarker,content,infowindow));
                google.maps.event.addListener(map,'click', (function(gmarker,content,infowindow){
                        return function() {
                            infowindow.close(map,gmarker);
                        };
                    })(gmarker,content,infowindow));


            };

            var bounds = new google.maps.LatLngBounds();
            for(var i = 0;i < markers.length;i++){
                bounds.extend(markers[i].getPosition());
            }
            map.fitBounds(bounds);
        },


    }
});