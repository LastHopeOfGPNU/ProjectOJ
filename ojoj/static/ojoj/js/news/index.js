// layer弹出层的下标
var layerIndex = 0;

var $table = $('#table'),
    $searchPart = $("#search-part"),
    $search = $('#search'),
    $toggleSearch = $('#toggle-search');

var SEARCHING = false

$(function(){

    // 时间插件初始化
    $('.datepicker').datetimepicker({
        locale: 'zh-CN',
        format: "YYYY-MM-DD"
    })
    $('.datetimepicker').datetimepicker({
        locale: 'zh-CN',
        format: 'YYYY-MM-DD hh:mm:ss'
    });
    initTable();
});


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
