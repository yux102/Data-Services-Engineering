//written by JingXuan Li
//javascript file for index page, using Vuejs framework


// url constant
const data_url = "http://127.0.0.1:5000/";



// Vuejs framework
var v = new Vue({
    el: '#index',

    data: {
        first_slide: 'Hello Vue!',
        second_slide: 'Hello Vue!',
        thrid_slide: 'Hello Vue!',
        code1: 'COMP9021',
        code2: 'COMP9021',
        code3: 'COMP9021',
        code4: 'COMP9021',
        code5: 'COMP9021',
        code6: 'COMP9021',
    },
    // data: {
        //     rows: '',
        //     year: '2018',
        //     country: 'Russia',
        //     c : {},
        //     code: 'RU',
        //
        // },


    mounted: function () {
        var self = this;

        $.ajax({
            url: data_url + '1/',
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
            url: data_url + '2/',
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
            },
            error : function (error) {
                console.log(error);
            }
        });

        this.info();



    },

    methods: {
        sendParams:function () {
            this.$router.push({
                path: 'client/course.html',
                name: '',
                params: {
                    name: 'code',
                    // dataObj: this.code1
                }

            })
        }



    }
});


