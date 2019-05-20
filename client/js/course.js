var $eleBtn1 = $("#btn1");
        var $eleBtn2 = $("#btn2");

        //已知一个下载文件的后端接口：https://codeload.github.com/douban/douban-client/legacy.zip/master
        //方法一：window.open()
        $eleBtn1.click(function(){
            window.open("https://codeload.github.com/douban/douban-client/legacy.zip/master");
        });
        //方法二：通过form
        $eleBtn2.click(function(){
            var $eleForm = $("<form method='get'></form>");

            $eleForm.attr("action","https://codeload.github.com/douban/douban-client/legacy.zip/master");

            $(document.body).append($eleForm);

            //提交表单，实现下载
            $eleForm.submit();
        });

const data_url = "http://127.0.0.1:5000/";


// Vuejs framework
var v = new Vue({
    el: '#course',

    data: {
        the_code: 'COMP9444'

    },


    mounted: function () {
        var self = this;

        $.ajax({
            url: data_url + 'resource/' + this.the_code,
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
            url: data_url + 'detail/' + this.the_code,
            method: 'GET',
            async: false,
            success: function (data) {
                console.log(data);
                self.campus = data['Campus'];
                self.career = data['Career'];
                self.description = data['Description'];
                self.requirement = data['Enrolment Requirements'];
                self.equivalent = data['Equivalent'];
                self.course_name = data['Name'];
                self.credit = data['Units of Credit'];

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
        },


        info : function(code){
        	// this.code1= code;
        	// console.log(code1);

        	var self = this;
		        $.ajax({
		            url: data_url + 'detail/'+this.code1,
		            method: 'GET',
		            success: function (data) {
		                console.log(data)
		                    // self.c=data[0];
		                    // self.code=data[0]['CountryCode'];
		                    // document.getElementById('jpflag').style.display="none";
		                    // if(self.code == 'KR/JP'){
		                    //     document.getElementById('jpflag').style.display="block";
		                    // }
		            },
		            error: function (error) {
		                    console.log(error);
		            }
		    });

		        var self = this;
		        $.ajax({
		            url: data_url + 'resource/'+this.code1,
		            method: 'GET',
		            success: function (data) {
		                console.log(data)
		                    // self.c=data[0];
		                    // self.code=data[0]['CountryCode'];
		                    // document.getElementById('jpflag').style.display="none";
		                    // if(self.code == 'KR/JP'){
		                    //     document.getElementById('jpflag').style.display="block";
		                    // }
		            },
		            error: function (error) {
		                    console.log(error);
		            }
		    });


        }

    }
});



