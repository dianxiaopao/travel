var uploader = $('#note_title_img');
uploader.fileupload(
    {
        url: '/mycenter/note/create/upload_title_img/',
        autoUpload: false,
        maxFileSize: 5 * 1024 * 1024,
        add: function (e, data) {
            data.submit().success(function (result, textStatus, jqXHR) {
                result = JSON.parse(result);
                result['csrfmiddlewaretoken'] = $("input[name='csrfmiddlewaretoken']").val()
                $.post('/mycenter/note/create/show_title_img/', result, function (res) {
                    res = JSON.parse(res);
                    res.path = res.path.toString().split('\\').join('/')
                    console.log("标题图片", res.path)
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
            if (result.error_msg) {
                alert(result.error_msg)
            } else {
                console.log(result)
            }
        })

    });
    $("body").on("click", ".show_edit_box_btn", function () {
        //点击加号显示选项
        if ($(".add_button").hasClass("add_button_show")) {
            $(".add_button").removeClass("add_button_show")
        } else {
            $(".add_button").addClass("add_button_show")
        }

    });

    $("body").on("click", ".edit_add_text", function () {
        //点击添加文字显示出来多行文本框
        $(".edit_content").css("display", "none")
        $(".add_text_con").css('display', 'block')
    });
    $("body").on("click", ".edit_add_image", function () {
        // 点击添加照片显示选择文件的页面
        $(".edit_content").css("display", "none")
        $(".add_img_con").css("display", "block")
    });
    $("body").on("click", ".edit_add_title", function () {
        // 添加段落标题
        $(".edit_content").css("display", "none")
        $(".add_title_con").css("display", "block")
    });
    console.log($("#articles_uuid").val())
    var upload_img_content = $("#note_img_content")
    upload_img_content.fileupload({
        url: '/mycenter/note/create/upload_img/?uuid=' + $("#articles_uuid").val()+'',
        autoUpload: false,
        maxFileSize: 5 * 1024 * 1024,
        add: function (e, data) {
            data.submit().success(function (result, textStatus, jqXHR) {
                result = JSON.parse(result);
                var path = result.path.toString().split('\\').join('/');
                console.log(path);
                var img_html = '<div class="g_img_content">' +
                    '<a href="#" role="button">' +
                    '<img style="width: 100%" src="/' + path + '" alt="图片">' +
                    '</a>' +
                    '</div>';
                $(".add_button_show").append(img_html);
                $('.add_img_con', '.add_button_show').css("display", "none")
            })
        }
    })


});

window.onbeforeunload = function (e) {
    // return false;
}
