/*
 * Created by MUJUN on 2018/7/15
 */
var $table = $("table");
$(function(){
    initPage();
});


function initPage() {
    $table.bootstrapTable({
        // height: getHeight(),
        toolbar: "#toolbar",
        // url: '/user/query',
        // method: 'post',
        // sortOrder: 'desc',
        // responseHandler: responseHandler,
        // queryParams: queryParams,
        data: [
            {"nick":"申根","role":"注册用户","title":"造假数据","type":"7","content":"造假数据造假数据造假数据造假数据造假数据造假数据造假数据造假数据造假数据","is_mark":"是","is_solve":"是"},
            {"nick":"申根","role":"注册用户","title":"造假数据","type":"8","content":"造假数据造假数据造假数据造假数据造假数据造假数据造假数据造假数据造假数据","is_mark":"否","is_solve":"否"},
            {"nick":"申根","role":"注册用户","title":"造假数据","type":"9","content":"造假数据造假数据造假数据造假数据造假数据造假数据造假数据造假数据造假数据","is_mark":"否","is_solve":"是"},
            {"nick":"申根","role":"注册用户","title":"造假数据","type":"10","content":"造假数据造假数据造假数据造假数据造假数据造假数据造假数据造假数据造假数据","is_mark":"否","is_solve":"否"},
            {"nick":"申根","role":"注册用户","title":"造假数据","type":"11","content":"造假数据造假数据造假数据造假数据造假数据造假数据造假数据造假数据造假数据","is_mark":"是","is_solve":"是"},
            {"nick":"申根","role":"注册用户","title":"造假数据","type":"12","content":"造假数据造假数据造假数据造假数据造假数据造假数据造假数据造假数据造假数据","is_mark":"是","is_solve":"是"},

        ],
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
}
//打开反馈详情内容
function openFeedBack() {
    var selection = $table.bootstrapTable('getSelections');
    if (selection.length == 0 || selection.length > 1) {
       layer.msg('请选择一项');
       return ;
    }
    $("#lookInfo").modal('show');
    var title = selection[0].title;
    var content = selection[0].content;
    var nick = selection[0].nick;
    var type = selection[0].type;
    var detail = $("#infoDetail");
    detail.empty();
    switch (type) {
        case '7':type='其他';break;
        default : break;
    }
    var jumbotron = $('<div class="jumbotron"></div>');
    jumbotron.append('<h2>'+title+'<span class="label label-default">'+type+'</span>'+'</h2>');
    jumbotron.append('<p>'+nick+'</p>');
    jumbotron.append('<p style="text-indent:2em">'+content+'</p>');
    detail.append(jumbotron);
}
//标记反馈意见
function markFeedBack() {
    var selection = $table.bootstrapTable('getSelections');
    if (selection == 0) {
        layer.msg('请选择一项');
        return ;
    }
    layer.msg('进行标记，补充代码');
}
function solveFeedBack() {
    var selection = $table.bootstrapTable('getSelections');
    if (selection == 0) {
        layer.msg('请选择一项');
        return ;
    }
    layer.msg('进行修改，补充代码');
}
function delectFeedBack() {
    var selection = $table.bootstrapTable('getSelections');
    if (selection == 0) {
        layer.msg('请选择一项');
        return ;
    }
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
        layer.msg('重新考虑');
    });
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

