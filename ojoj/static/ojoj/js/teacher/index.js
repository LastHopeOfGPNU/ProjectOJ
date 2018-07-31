/*
 * Created by MUJUN on 2018/7/14
 */
//设置全局变量
var $table = $("#table");
var $addForm = $("#addForm");
var $changeForm = $("#changeForm");
var $toggleSearch = $("#toggle-search");
var $searchPart = $("#search-part");
var $search = $('#search');
var file;
var url = 'http://39.108.149.69';
var data={
    "username": "1073315663@qq.com",
    "password": "jl7798887"
}
$(function() {
    initPage();
    /*$.ajax({
        url: url,
        type: 'post',
        data:JSON.stringify(data),
        success: function(res){
            console.log(res);
        },
        error: function(e) {
            console.log(e);
        }
    })*/
});
//初始化页面
function initPage() {
    $table.bootstrapTable({
        // height: getHeight(),
        toolbar: "#toolbar",
        url: url+'/user/teachers',//异步请求的链接
        method: 'post',
        // sortOrder: 'desc',//排序方式
        responseHandler: responseHandler,//对回调数据进行处理
        queryParams: queryParams,//异步请求的传参
        /*data:[
            {"code":"20130347","nick":"李四","sex":"男","academic":"计算机科学学院","major":"应用数学系","contact":"13415554442","classnum":"8","email":"781244184@qq.com","QQ":"781244184"},
            {"code":"20130347","nick":"李四","sex":"男","academic":"计算机科学学院","major":"应用数学系","contact":"13415554442","classnum":"8","email":"781244184@qq.com","QQ":"781244184"},
            {"code":"20130347","nick":"李四","sex":"男","academic":"计算机科学学院","major":"应用数学系","contact":"13415554442","classnum":"8","email":"781244184@qq.com","QQ":"781244184"},
            {"code":"20130347","nick":"李四","sex":"男","academic":"计算机科学学院","major":"应用数学系","contact":"13415554442","classnum":"8","email":"781244184@qq.com","QQ":"781244184"},
            {"code":"20130347","nick":"李四","sex":"男","academic":"计算机科学学院","major":"应用数学系","contact":"13415554442","classnum":"8","email":"781244184@qq.com","QQ":"781244184"},

        ],//测试数据*/
        striped: true,  // 隔行换色
        showRefresh: true,
        showColumns: true,
        showToggle: true,
        detailView: true,
        minimumCountColumns: 2,
        pagination: true,
        pageList: "[15, 20, 25, 50, 100]",
        pageNumber: 1,
        pageSize: 15,
        showFooter: false,
        // sidePagination: "server",
        clickToSelect:true
    });
    setTimeout(function () {
        $table.bootstrapTable('resetView');
    }, 200);
    formValidator();
    $(document).on('change','#excelFile',function(e) {
        // 批量上传教师信息文件绑定
        e.stopPropagation();
        file = $(this).get(0).files;//获取文件
        if(file.length == 0)return ;//如果文件为空；
        var suffix = (file[0].name).split('.')[1];//判断文件类型
        if(suffix != "xls" && suffix != "xlsx"){
            // layer.msg("请上传Excel文件");//消息提示框
            layer.alert('请上传Excel文件');
            return ;
        }
        console.log(file);
        batchTeacher();
    });
    $toggleSearch.on('click',function(e) {
        e.stopPropagation();
        if($searchPart.css('display') === 'none') {
            $toggleSearch.html('<i class="icon-angle-up"></i> 收起搜索');
        }else {
            $toggleSearch.html('<i class="icon-angle-down"></i> 展开搜索');
        }
        $searchPart.slideToggle(function(){
            /*$table.bootstrapTable('resetView', {
                height: getHeight()
            });*/
        });
        $search.toggle();
    });

}
//新增教师
function addTeacher() {
    $addForm.data('bootstrapValidator').validate();//进行表单验证
    var isValid = $addForm.data('bootstrapValidator').isValid();//判断验证是否正确
    if(!isValid){
        return ;//没有按要求完整填写表单时
    }
    //验证成功后提交表单
    var array = $addForm.serializeArray();//获取表单填入的信息
//    当提交成功后 刷新表单
    $table.bootstrapTable('refresh');
}
//批量添加教师
function batchTeacher() {
    var targetInput=$("#fileInput");//获取文件输入框
    targetInput.val(file[0].name);
    var formData=new FormData();
    console.log(file[0]);
    formData.append('files',file);
    console.log(formData);
}
//删除教师
function delectTeacher() {
    var selection = $table.bootstrapTable('getSelections');//获取选中项
    if(selection.length==0){layer.msg('请选择至少一项');return;}
    layer.confirm('您确认要删除选中记录？', {
        btn: ['确认','取消'] //按钮
    }, function(){
        //确认删除执行的动作
        layer.msg('删除中，请稍候', {icon: 1});
        $.ajax({
            url: '/systemMessage/batch_delete',
            contentType: 'application/json;charset=utf-8',
            type: 'post',
            dataType: 'json',
            // data:JSON.stringify(ids),
            success: function (data) {
                layer.msg('删除成功！',  {icon: 1});
                layer.closeAll();
                refreshTable();//更新列表
            },
            error:function(){
                layer.alert('删除失败！',  {icon: 2});
            }
        });
    }, function(){
        layer.msg('重新考虑', {
            time: 20000 //20s后自动关闭
        });
    });

}
function formValidator() {
//    表单验证
    $addForm.bootstrapValidator({
        message: '这个值无效',
        feedbackIcons: {/*输入框不同状态，显示图片的样式*/
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        excluded: [':disabled', ':hidden', 'select'],
        fields: {//自定义验证
            addContact:{
                message:'请输入正确电话联系方式',
                validators:{
                    regexp:{
                        regexp:/^((00|\+)?(86(?:-| )))?((\d{11})|(\d{3}[- ]{1}\d{4}[- ]{1}\d{4})|((\d{2,4}[- ]){1}(\d{7,8}|(\d{3,4}[- ]{1}\d{4}))([- ]{1}\d{1,4})?))$/,
                        message:'请输入正确电话联系方式'
                    }
                }
            }
        }
    });
    $changeForm.bootstrapValidator({
        message: '这个值无效',
        feedbackIcons: {/*输入框不同状态，显示图片的样式*/
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        excluded: [':disabled', ':hidden', 'select'],
        fields: {//自定义验证
            addContact:{
                message:'请输入正确电话联系方式',
                validators:{
                    regexp:{
                        regexp:/^((00|\+)?(86(?:-| )))?((\d{11})|(\d{3}[- ]{1}\d{4}[- ]{1}\d{4})|((\d{2,4}[- ]){1}(\d{7,8}|(\d{3,4}[- ]{1}\d{4}))([- ]{1}\d{1,4})?))$/,
                        message:'请输入正确电话联系方式'
                    }
                }
            }
        }
    });
}
// 获取bootstrap table高度
function getHeight() {
    var searchHeight = 0;
    if($("#search-part").css('display') !== 'none') {
        searchHeight = $('#search-part').height();
    }
    return $(window).height() - 20 - searchHeight;
}
//更新列表
function refreshTable() {
    $table.bootstrapTable('refresh');
}
//回显修改信息模态框
function showTeacherInfo() {
    var selection = $table.bootstrapTable('getSelections');
    if(selection.length == 0 || selection>1){
        layer.msg('请选择一项');
        return ;
    }
    $("#changeTeacher").modal('show');
    console.log(selection[0]);
//    回填数据
    $("#changeCode").val(selection[0].code);
    $("#changeNick").val(selection[0].nick);
    $("#changeContact").val(selection[0].contact);
}
//清空表单
function clearForm() {
    $('form').bootstrapValidator('resetForm', true);
}
//修改教师信息
function changeTeacherInfo() {
    $changeForm.data('bootstrapValidator').validate();//进行表单验证
    var isValid = $changeForm.data('bootstrapValidator').isValid();//判断验证是否正确
    if(!isValid){
        return ;//没有按要求完整填写表单时
    }
    //验证成功后提交表单
    var array = $changeForm.serializeArray();//获取表单填入的信息
}