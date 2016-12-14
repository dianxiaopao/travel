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
                $.post('/mycenter/note/create/show_title_img/', result, function (res) {
                    res = JSON.parse(res);
                    res.path=res.path.toString().split('\\').join('/')
                    $('#t_img_con_back').css({
                        "background":"url(/"+res.path+")",
                        "background-size":'100%',
                    });
                    $('#upload_title_img_laber').css({"visibility":"hidden"})
                    $('#again_title_img').css({"visibility":"inherit"}).off('click').on('click',function () {
                        $(this).css('visibility','hidden')
                        $('#upload_title_img_laber').css({"visibility":"inherit"})
                    })
                });

            })
        }
    });
window.onbeforeunload=function (e) {
    return false;
}