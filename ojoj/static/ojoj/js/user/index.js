/*
 * Created by MUJUN on 2018/7/16
 */
var $table = $("#table");
var searchOptions = {};
$(function(){
    initPage();
});

function initPage() {
    $table.bootstrapTable({
        height: getHeight(),
        toolbar: "#toolbar",
        // url: '/user/query',
        // method: 'post',
        // sortOrder: 'desc',
        // responseHandler: responseHandler,
        // queryParams: queryParams,
        data: userData,
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
    // sometimes footer render error.
    setTimeout(function () {
        $table.bootstrapTable('resetView');
    }, 200);
    $(window).resize(function () {
        $table.bootstrapTable('resetView', {
            height: getHeight()
        });
    });
}
//打开用户信息弹框
function openUserInfo() {
    var selection = $table.bootstrapTable('getSelections');
    if(selection.length == 0 || selection.length > 1){
        layer.msg('请选择一项记录');
        return;
    }
    getUserData();
    $("#UserInfo").modal('show');
}
//获取用户具体信息
function getUserData() {

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
    SEARCHING = !!flag;
    initSearchOptions();
    if (SEARCHING) $('#table').bootstrapTable('refresh', {pageNumber:1}); // 重置页码
    else $table.bootstrapTable(('refresh'));
}
function initSearchOptions() {
    searchOptions['nick'] = $("#searchNick").val();
    searchOptions['email'] = $("#searchEmail").val();
    searchOptions['sex'] = $("#searchSex").val();
    console.log(searchOptions);
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
var userData = [
        {
            "uid": "935",
            "email": "1595852135@qq.com",
            "sex": "1",
            "nick": "lyx",
            "reg_time": "2018-07-17 21:36:08",
            "login_time": null
        },
        {
            "uid": "934",
            "email": "28721054@qq.com",
            "sex": "1",
            "nick": "lyx",
            "reg_time": "2018-07-14 13:48:04",
            "login_time": "2018-07-14 13:48:10"
        },
        {
            "uid": "933",
            "email": "1111111@qq.com",
            "sex": "1",
            "nick": "111",
            "reg_time": "2018-04-14 12:51:59",
            "login_time": "2018-04-14 12:52:04"
        },
        {
            "uid": "932",
            "email": "111111111111111@qq.com",
            "sex": "1",
            "nick": "GPNU_team0077",
            "reg_time": "2018-04-14 12:35:06",
            "login_time": null
        },
        {
            "uid": "931",
            "email": "987654321@qq.com",
            "sex": "1",
            "nick": "忘记原来密码",
            "reg_time": "2018-04-13 20:59:46",
            "login_time": "2018-04-14 11:00:46"
        },
        {
            "uid": "930",
            "email": "543157495@qq.com",
            "sex": "1",
            "nick": "忘记原来密码了",
            "reg_time": "2018-04-13 20:58:39",
            "login_time": null
        }
]