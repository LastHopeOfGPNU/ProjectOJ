// 消息框位置控制
var stack_bottomright = {"dir1": "up", "dir2": "left", "firstpos1": 25, "firstpos2": 25};
var $table = $("#table");
//查看信息详情
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