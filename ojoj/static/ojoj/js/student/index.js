// layer弹出层的下标

var layerIndex = 0;

var $table = $('#table'),
    $addForm = $("#addForm"),
    $changeForm = $("#changeForm"),
    $searchPart = $("#search-part"),
    $search = $('#search'),
    $toggleSearch = $('#toggle-search');

var SEARCHING = false

$(function() {
    initPage();
});

function initPage() {
    $table.bootstrapTable({
        // height: getHeight(),
        toolbar: "#toolbar",
        // url: '/user/query',//异步请求的链接
        // method: 'post',
        // sortOrder: 'desc',//排序方式
        // responseHandler: responseHandler,//对回调数据进行处理
        // queryParams: queryParams,//异步请求的传参
        data:[
            {
                "uid": "767",
                "nick": "刘嘉威",
                "code": "2016025144120",
                "contact": null,
                "user_id": "2016025144120",
                "academy_id": "1",
                "classnum": "0",
                "academy": "计算机科学学院",
                "major": null,
                "login_time": "2017-11-22 12:04:11",
                "class_id": "20170347430",
                "class_name": "17软件工程"
            },
            {
                "uid": "766",
                "nick": "周云聪",
                "code": "2016094243016",
                "contact": null,
                "user_id": "2016094243016",
                "academy_id": "1",
                "classnum": "0",
                "academy": "计算机科学学院",
                "major": null,
                "login_time": "2018-05-01 18:02:48",
                "class_id": "20170347430",
                "class_name": "17软件工程"
            },
            {
                "uid": "765",
                "nick": "盘惠清",
                "code": "2016034843027",
                "contact": null,
                "user_id": "2016034843027",
                "academy_id": "1",
                "classnum": "0",
                "academy": "计算机科学学院",
                "major": null,
                "login_time": "2017-12-04 23:38:27",
                "class_id": "20170347430",
                "class_name": "17软件工程"
            },
            {
                "uid": "764",
                "nick": "张紫珊",
                "code": "2016034843019",
                "contact": null,
                "user_id": "2016034843019",
                "academy_id": "1",
                "classnum": "0",
                "academy": "计算机科学学院",
                "major": null,
                "login_time": "2017-12-05 18:44:24",
                "class_id": "20170347430",
                "class_name": "17软件工程"
            }

        ],//测试数据
        striped: true,//隔行变色
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
    // formValidator();
    $(document).on('change','#excelFile',function(e) {
        // 批量上传学生信息文件绑定
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
        batchStudent();
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

function batchStudent() {
    var targetInput=$("#fileInput");//获取文件输入框
    targetInput.val(file[0].name);
    var formData=new FormData();
    console.log(file[0]);
    formData.append('files',file);
    console.log(formData);
}

//回显修改信息模态框
function showStudentInfo() {
    var selection = $table.bootstrapTable('getSelections');
    if(selection.length == 0 || selection>1){
        layer.msg('请选择一项');
        return ;
    }
    $("#changeStudent").modal('show');
    console.log(selection[0]);
//    回填数据
    $("#changeCode").val(selection[0].code);
    $("#changeNick").val(selection[0].nick);
    $("#changeContact").val(selection[0].contact);
}

//删除学生
function delectStudent() {
    var selection = $table.bootstrapTable('getSelections');
    if(selection == 0){
        layer.msg('请选择至少一项');
        return;
    }else{
        layer.confirm("您确定要删除此记录",{
            btn:['确定','取消']
        },function () {
            layer.msg('删除中，请稍候', {icon: 1});
            $.ajax({
                url: '/systemMessage/batch_delete',
                contentType: 'application/json;charset=utf-8',
                type: 'post',
                dataType: 'json',
                success: function () {
                    layer.msg('删除成功！',  {icon: 1});
                    layer.closeAll();
                    refreshTable();//更新列表
                },
                error:function () {
                    layer.alert('删除失败！',  {icon: 2});
                }
            })
        },function () {
            layer.msg('已取消删除', {
                time: 3000 //20s后自动关闭
            });
        })
    }
}

//清空表单
function clearForm() {
    $('form').bootstrapValidator('resetForm', true);
}

//修改学生信息
function changeSduentInfo() {
    $changeForm.data('bootstrapValidator').validate();//进行表单验证
    var isValid = $changeForm.data('bootstrapValidator').isValid();//判断验证是否正确
    if(!isValid){
        return ;//没有按要求完整填写表单时
    }
    //验证成功后提交表单
    var array = $changeForm.serializeArray();//获取表单填入的信息
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
























function initTable() {
    $table.bootstrapTable({
        height: getHeight(),
        toolbar: "#toolbar",
        url: '/user/query',
        method: 'post',
        // sortOrder: 'desc',
        responseHandler: responseHandler,
        queryParams: queryParams,
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
        sidePagination: "server",
        clickToSelect:true
    });
    // sometimes footer render error.

    setTimeout(function () {
        $table.bootstrapTable('resetView');
    }, 200);

    $table.on('expand-row.bs.table', function (e, index, row, $detail) {
        var html = [];
        $.each(row, function (key, value) {
            html.push('<p><b>' + key + ':</b> ' + value + '</p>');
        });
        return $detail.html(html);
    });
    $(window).resize(function () {
        $table.bootstrapTable('resetView', {
            height: getHeight()
        });
    });
    $toggleSearch.on('click', function(e){
        e.stopPropagation();
        if($searchPart.css('display') === 'none') {
            $toggleSearch.html('<i class="icon-angle-up"></i> 收起搜索');
        } else {
            $toggleSearch.html('<i class="icon-angle-down"></i> 展开搜索');
        }
        $searchPart.slideToggle(function(){
            $table.bootstrapTable('resetView', {
                height: getHeight()
            });
        });
        $search.toggle();
    });
    // checkbox 选中
    $(".checkbox-input").click(function (e) {
        e.stopPropagation();
        if($(this).hasClass("selected")) {
            $(this).removeClass("selected");
            $(this).children('input[type="checkbox"]').first().prop('checked', false);
        }else {
            $(this).addClass("selected");
            $(this).children('input[type="checkbox"]').first().prop('checked', true);
        }
        searchInfo(true);
    });
    // 搜索
    $search.on('click', function(e) {
        e.stopPropagation();
        searchInfo(true);
    });
    // 搜索表单域中绑定的事件
    $("input.search-control").on('keydown',function(e){
        e.stopPropagation();
        if(e.keyCode == "13") {
            searchInfo(true);
        }
    });
    $("select.search-control").on("change", function (e) {
        e.stopPropagation();
        searchInfo(true);
    })
}

// 数据返回处理
function responseHandler(res) {
    var data=res.data.data_list;
    for(var i=0;i<data.length;i++){
        //处理专业领域
        var professionalFieldStr = data[i].professional_field;
        var professionalFieldObj = JSON.parse(professionalFieldStr);
        data[i].professional_field = professionalFieldObj.title;
    }
    return {
        "total": res.data.total,//总页数
        "rows": res.data.data_list   //数据
    };
}

// 搜索功能
function searchInfo(flag) {
    SEARCHING = !!flag
    if (SEARCHING) $('#table').bootstrapTable('refresh', {pageNumber:1}); // 重置页码
    else $table.bootstrapTable(('refresh'));
}

//表格数据获取的参数
function queryParams(params) {
    console.log(params);
    var pager = {};
    pager.current = params.offset/params.limit + 1;
    pager.size = params.limit;
    var postData = {
        pager: pager
        // order: params.order,
        // sort: params.sort
    };
    return postData;
}
// 获取bootstrap table高度
function getHeight() {
    var searchHeight = 0;
    if($("#search-part").css('display') !== 'none') {
        searchHeight = $('#search-part').height();
    }
    return $(window).height() - 20 - searchHeight;
}

// 返回关联选择后的值
function handleRelevance(data, selector) {
    var tempName = '';
    var tempId = '';
    for(var i = 0, len = data.length; i < len; i++) {
        if( i > 0 ) { // 如果不是第一个
            tempName += ',';
            tempId += ',';
        }
        tempName += data[i].name;
        tempId += data[i].id;
    }
    $('input[name=' + selector + ']').val(tempId).next().val(tempName);
    // 调用搜索功能
    searchInfo();
}

// 消息框位置控制
var stack_bottomright = {"dir1": "up", "dir2": "left", "firstpos1": 25, "firstpos2": 25};

/**
 * 获取选中项
 * @param  可以是：空值、字符串、字符串数组
 */
function getSelection(option) {
    if(typeof option === 'undefined') {
        return [];
    } else if(typeof option === 'string') {
        return $.map($table.bootstrapTable('getSelections'), function (row) {
            var obj = {};
            var tempName = row[option] + '';
            if(tempName.indexOf('<a') !== -1) {
                tempName = $(tempName).text();
            }
            obj[option] = tempName;
            return obj;
        });
    } else {
        return $.map($table.bootstrapTable('getSelections'), function (row) {
            var obj = {};
            for(var i = 0, len = option.length; i < len; i++) {
                var tempName = row[option[i]] + '';
                if(tempName.indexOf('<a') !== -1) {
                    tempName = $(tempName).text();
                }
                obj[option[i]] = tempName;
            }
            return obj;
        });
    }
}
//返回数据
function rebackInfo(){
    var data=$table.bootstrapTable("getAllSelections");
    if(data.length==0){
        layer.msg("未选择任何项！",function(){});
        return ;
    }
    if(data.length>1){
        layer.msg("只能选择一个发包人",function(){});
    }
    var postData={
        id:data[0].id,
        userName:data[0].userName
    }
    // console.log(postData);
    if(parent.window.handleRelevance){
        parent.window.handleRelevance(postData);
        layerIndex=parent.layer.getFrameIndex(window.name);
        parent.layer.close(layerIndex)
    }
}
