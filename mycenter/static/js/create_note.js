/**
 * Created by frowlwood on 2016/11/24.
 */
var uploader = $('#note_title_img');
uploader.fileupload(
    {
        url: '/mycenter/note/create/upload_title_img/',
        autoUpload: false,
        maxFileSize: 5 * 1024 * 1024,
        processfail: function (e, data) {
            //单个文件上传失败
            //支持上传的最大文件、
            //单次允许上传的文件数
        },
        processdone: function (e, data) {
            if (self.datafile == undefined) {
                self.datafile = data;
            }
        },
        add: function (e, data) {
            data.submit().success(function (result, textStatus, jqXHR) {
                result = JSON.parse(result);
                result['csrfmiddlewaretoken'] = $("input[name='csrfmiddlewaretoken']").val()
                $.post('/mycenter/note/create/show_title_img/', result, function (res) {
                    res = JSON.parse(res);
                    res.path = res.path.toString().split('\\').join('/')
                    $('#t_img_con_back').css({
                        "background": "url(/" + res.path + ")",
                        "background-size": '100%',
                    });
                    $('#upload_title_img_laber').css({"visibility": "hidden"})
                    $('#again_title_img').css({"visibility": "inherit"}).off('click').on('click', function () {
                        $(this).css('visibility', 'hidden')
                        $('#upload_title_img_laber').css({"visibility": "inherit"})
                    })
                });
            })
        }
    });
$(document).ready(function () {
    $("body").on("click", "#test", function (data) {
        console.log($("input[name='csrfmiddlewaretoken']").val())
    })
    $("body").on("change", "#guide_title", function () {
        //上传文章标题
        var data = {
            "title": $(this).val().toString(),
            "uuid": $("#articles_uuid").val().toString()
        };
        data['csrfmiddlewaretoken'] = $("input[name='csrfmiddlewaretoken']").val()
        $.post('/mycenter/note/create/create_title/', data, function (result) {
            result = JSON.parse(result)
            if(result.error_msg){
                alert(result.error_msg)
            }else {
                console.log(result)
            }
        })

    });

    $("body").on("click",".edit_add_text",function () {
        //点击添加文字显示出来多行文本框
        $(".add_text_con").css('display','block')
    })
    $("body").on("click",".show_edit_box_btn",function () {
        //点击加号显示选项
        if($(".add_button").hasClass("add_button_show")){
            $(".add_button").removeClass("add_button_show")
        }else{
            $(".add_button").addClass("add_button_show")
        }

    })

});

window.onbeforeunload = function (e) {
    // return false;
}
