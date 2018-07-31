var $submit = $('#submitMaintain')


$(function(){
    initPage()
    Datetime()
})


//初始化页面
function initPage() {
    $submit.on('click', function(e){
        e.stopPropagation();

        var startDate = $('#startdate').val()
        var endDate = $('#enddate').val()

        console.log(startDate);
        console.log(endDate);

        /*
        *   将数据提交给后台
        */


        e.preventDefault();
        layer.msg("已提交",function(){});
    });
}


//设置日期时间控件
function Datetime() {
    $('.date').datetimepicker({
        format: 'YYYY-MM-DD',//显示格式
        locale: moment.locale('zh-cn')
    });
}

