/*
 * Created by MUJUN on 2018/7/17
 */
var $table = $("#table");
var $toggleSearch = $("#toggle-search");
var $searchPart = $("#search-part");
var $search = $('#search');
$(function() {
    initPage();
});
//初始化页面
function initPage() {
    $table.bootstrapTable({
        height: getHeight(),
        toolbar: "#toolbar",
        // url: '/user/query',//异步请求的链接
        // method: 'post',
        // sortOrder: 'desc',//排序方式
        // responseHandler: responseHandler,//对回调数据进行处理
        // queryParams: queryParams,//异步请求的传参
        data:[
            {
                "class_id": "20170347430",
                "class_name": "17软件工程",
                "grade": "2017",
                "academy_id": "1",
                "student_count": "63",
                "courses_list": [
                    {
                        "courses_id": "81",
                        "courses_name": "C程序设计"
                    }
                ],
                "academy": "计算机科学学院"
            },
            {
                "class_id": "20160357430",
                "class_name": "16物联网",
                "grade": "2016",
                "academy_id": "1",
                "student_count": "46",
                "courses_list": [],
                "academy": "计算机科学学院"
            },
            {
                "class_id": "20160347431",
                "class_name": "16软件工程2班",
                "grade": "2016",
                "academy_id": "1",
                "student_count": "53",
                "courses_list": [
                    {
                        "courses_id": "70",
                        "courses_name": "C"
                    },
                    {
                        "courses_id": "75",
                        "courses_name": "?"
                    },
                    {
                        "courses_id": "76",
                        "courses_name": "C程序设计"
                    }
                ],
                "academy": "计算机科学学院"
            }
        ],//测试数据
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
//添加班级
function addClass() {
    $("#addClass").modal('show');
}
//删除班级
function deleteClass() {
    var selections = $table.bootstrapTable('getSelections');
    if (selections == 0){
        layer.msg('请选择一项');
        return ;
    }
    layer.confirm('您确认要删除选中记录？', {
        btn: ['确认','取消'] //按钮
    }, function(){
        //确认删除执行的动作
        layer.msg('删除中，请稍候', {icon: 1});
        /*$.ajax({
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
        });*/
    }, function(){
        layer.msg('重新考虑', {
            time: 20000 //20s后自动关闭
        });
    });
}
//查看班级信息
function openClassInfo() {
    var selection = $table.bootstrapTable("getSelections");
    if (selection > 1 || selection == 0){
        layer.msg("请选择一项");
        return ;
    }
    $("#classInfo").modal('show');
    $("#table2").bootstrapTable({
        height: getHeight(),
        // url: '/user/query',//异步请求的链接
        // method: 'post',
        // sortOrder: 'desc',//排序方式
        // responseHandler: responseHandler,//对回调数据进行处理
        // queryParams: queryParams,//异步请求的传参
        data:[
            {
                "class_id": "20170347430",
                "class_name": "17软件工程",
                "grade": "2017",
                "academy_id": "1",
                "student_count": "63",
                "courses_list": [
                    {
                        "courses_id": "81",
                        "courses_name": "C程序设计"
                    }
                ],
                "academy": "计算机科学学院"
            },
            {
                "class_id": "20160357430",
                "class_name": "16物联网",
                "grade": "2016",
                "academy_id": "1",
                "student_count": "46",
                "courses_list": [],
                "academy": "计算机科学学院"
            },
            {
                "class_id": "20160347431",
                "class_name": "16软件工程2班",
                "grade": "2016",
                "academy_id": "1",
                "student_count": "53",
                "courses_list": [
                    {
                        "courses_id": "70",
                        "courses_name": "C"
                    },
                    {
                        "courses_id": "75",
                        "courses_name": "?"
                    },
                    {
                        "courses_id": "76",
                        "courses_name": "C程序设计"
                    }
                ],
                "academy": "计算机科学学院"
            }
        ],//测试数据
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
        clickToSelect:true
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
//测试用 Ajax
/*function testAajx() {
    var postData = {
        action: "manager.class.list",
        page: 1,
        pagesize: 10
    };
    $.ajax({
        url: 'http://114.215.99.34/gdinoj/server/',
        contentType: 'text/html;charset=utf-8',
        dataType: "jsonp",
        jsonp: "callback",
        data: JSON.stringify(postData),
        success:function(res) {
            console.log(res);
        }
    })
}*/
