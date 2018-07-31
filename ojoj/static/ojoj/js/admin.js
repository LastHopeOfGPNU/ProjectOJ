/*
 * create by mujun at 2018/7/14
 */
var click = device.mobile() ? 'touchstart' : 'click';
// 获取表单
var $form = $("#modifyPasswordForm");
// 菜单栏解析
function analysisMenu(menus) {
    var menuDom = $('<ul class="menu-list sm-fontSize"></ul>');
    var TEMPS = menus;  // 存储树状中无其父节点的菜单项
    var count = 0; // 防止找不到父节点的菜单陷入死循环, 最大容错层数为20层
    while(TEMPS.length !== 0 && count < 20) {
        var tempMenus = [];
        for(var i = 0, len = TEMPS.length; i < len; i++ ){
            if(TEMPS[i].pid === 'undefined' || TEMPS[i].pid === null) { // 无父节点
                if(TEMPS[i].url === 'undefined' || TEMPS[i].url === '' || TEMPS[i].url === null) {
                    menuDom.append('<li class="sub-menu" data-id="'+TEMPS[i].id+'"><a class="icon-plus waves-effect" href="javascript:void(0)"><i class="' + TEMPS[i].icon + '"></i>'+TEMPS[i].title+'</a> <ul> </ul> </li>');
                } else {
                    var mark = TEMPS[i].url.indexOf('?') > - 1 ? '&' : '?';
                    var menuInfo = mark + 'menuId=' + TEMPS[i].id;
                    menuDom.append('<li data-id="'+TEMPS[i].id+'"><a class="waves-effect" href="javascript:Tab.addTab(\''+TEMPS[i].title+'\', \'tab_iframe_'+TEMPS[i].id+'\', \''+TEMPS[i].url + menuInfo +'\')">'+TEMPS[i].title+'</a></li>');
                }
            } else { // 有父节点  --- 层次遍历
                var queue = [], rear = -1, front = -1, temp;
                var found = false;
                queue[++rear] = menuDom;
                while(rear !== front) {
                    front = front + 1;
                    temp = queue[front];
                    var tempId = parseInt(temp.attr('data-id'));
                    if(tempId !== 'undefined' && parseInt(tempId) === parseInt(TEMPS[i].pid)) {
                        if(TEMPS[i].url === 'undefined' || TEMPS[i].url === null) {
                            temp.children('ul').first().append('<li class="sub-menu" data-id="'+TEMPS[i].id+'"><a class="waves-effect" href="javascript:void(0)"><i></i>'+TEMPS[i].title+'</a> <ul> </ul> </li>');
                        } else {
                            var mark = TEMPS[i].url.indexOf('?') > - 1 ? '&' : '?';
                            var menuInfo = mark + 'menuId=' + TEMPS[i].id;
                            temp.children('ul').first().append('<li data-id="'+TEMPS[i].id+'"><a class="waves-effect" href="javascript:Tab.addTab(\''+TEMPS[i].title+'\', \'tab_iframe_'+TEMPS[i].id+'\', \''+TEMPS[i].url + menuInfo + '\')">'+TEMPS[i].title+'</a></li>');
                        }
                        found =true;
                        break;
                    }
                    var tempLen = temp.children('li').length || temp.find('ul li').length ;
                    for(var k = 0; k < tempLen; k++) {
                        rear = rear + 1;
                        queue[rear] = temp.children('li').eq(k) || temp.find('ul li').eq(k);
                    }
                }
                if(!found) {
                    tempMenus.push(TEMPS[i]);
                }
            }
        }
        count++;
        TEMPS = tempMenus;
    }
    menuDom.prepend('<li><a class="waves-effect" href="javascript:Tab.addTab(\'首页\', \'home\', \'/\')"><i class="icon-home"></i> 首页</a></li>');
    menuDom.append('<li><div class="copyright">Copyright © 智汇+</div></li>');
    $(".main-menu").append(menuDom);
}

$(function() {
    /*var menuList = sortUp(roleMenus, 'sort');
    analysisMenu(menuList);*/
    // 侧边栏操作按钮
    $(document).on(click, '#guide', function() {
        $(this).toggleClass('toggled');
        $('#sidebar').toggleClass('toggled');
    });
    // 侧边栏二级菜单
    $(document).on(click, '.sub-menu>a', function() {
        $(this).next().slideToggle(200);
        $(this).parent().toggleClass('toggled');
        if($(this).hasClass('icon-plus')){
            $(this).removeClass('icon-plus');
            $(this).addClass('icon-minus');
        }else {
            $(this).removeClass('icon-minus');
            $(this).addClass('icon-plus');
        }
    }).on(click, '.s-profile>a', function(e){
        e.stopPropagation();
        if($(this).parent().hasClass('toggled')) {
            $(this).parent().removeClass('toggled');
            $(".s-profile-list").slideUp();
        }else {
            $(this).parent().addClass('toggled');
            $(".s-profile-list").slideDown();
        }
    });

    // 关闭tab页（为tab页上的关闭图标注册关闭事件）
    $(document).on('click', '.content_tab>ul>li>i', function(e) {
        e.stopPropagation();
        Tab.closeTab($(e.currentTarget).parent());
    });
    // Waves初始化
    Waves.displayEffect();
    // 滚动条初始化
    $("#sidebar .main-menu").slimScroll({
        width: '100%',
        height: '100%',
        size: '6px', //组件宽度
        color: '#333', //滚动条颜色
        position: 'right', //组件位置：left/right
        distance: '0', //组件与侧边之间的距离
        start: 'top', //默认滚动位置：top/bottom
        opacity: .4, //滚动条透明度
        alwaysVisible: false, //是否 始终显示组件
        disableFadeOut: true, //是否 鼠标经过可滚动区域时显示组件，离开时隐藏组件
        railVisible: true, //是否 显示轨道
        railColor: '#333', //轨道颜色
        railOpacity: .1, //轨道透明度
        railDraggable: true, //是否 滚动条可拖动
        railClass: 'slimScrollRail', //轨道div类名
        barClass: 'slimScrollBar', //滚动条div类名
        wrapperClass: 'slimScrollDiv', //外包div类名
        allowPageScroll: true, //是否 使用滚轮到达顶端/底端时，滚动窗口
        wheelStep: 20, //滚轮滚动量
        touchScrollStep: 200, //滚动量当用户使用手势
        borderRadius: '6px', //滚动条圆角
        railBorderRadius: '6px' //轨道圆角
    });
    formValidator();
});
// iframe高度自适应
function changeFrameHeight(ifm) {
    ifm.height = document.documentElement.clientHeight - 92;
}
function resizeFrameHeight() {
    $('.tab_iframe').css('height', document.documentElement.clientHeight - 92);
    $('md-tab-content').css('left', '0');
}
// 窗体尺寸改变时
window.onresize = function() {
    resizeFrameHeight();
    initScrollShow();
    initScrollState();
}

// 表单验证
function formValidator() {
    // 表单验证
    $("#modifyPasswordForm").bootstrapValidator({
        message: '这个值无效',
        feedbackIcons: {/*输入框不同状态，显示图片的样式*/
            valid: 'glyphicon glyphicon-ok',
            invalid: 'glyphicon glyphicon-remove',
            validating: 'glyphicon glyphicon-refresh'
        },
        excluded: [':disabled', ':hidden', 'select'],
        fields: {/*验证*/
            oldPassword: {/*键名username和input name值对应*/
                message: '旧密码无效',
                validators: {
                    notEmpty: {/*非空提示*/
                        message: '就密码不能为空'
                    }
                }
            },
            newPassword: {
                message:'新密码无效',
                validators: {
                    notEmpty: {
                        message: '新密码不能为空'
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: '密码长度必须在6到30之间'
                    }
                }
            },
            confirmPassword: {
                message:'确认新密码无效',
                validators: {
                    notEmpty: {
                        message: '确认新密码不能为空'
                    },
                    stringLength: {
                        min: 6,
                        max: 30,
                        message: '确认密码长度必须在6到30之间'
                    },
                    identical: {//相同
                        field: 'newPassword',
                        message: '两次密码不一致'
                    },
                }
            }
        }
    });
}

// 弹出修改密码的框
function passwordModal (e) {
    e.stopPropagation();
    $('#modify-password-modal').modal('show');
}
// 模态框关闭后调用
$('#modify-password-modal').on('hidden.bs.modal', function() {
    $form.data('bootstrapValidator').destroy();
    $form.data('bootstrapValidator', null);
    $form[0].reset();
    formValidator();
});
function modifyPassword() {
    $form.data('bootstrapValidator').validate();
    var isValid = $form.data('bootstrapValidator').isValid();
    if(!isValid) {
        return;
    }
    var postData = {
        oldPassword: encrypt($('#old-password').val()),
        newPassword: encrypt($('#new-password').val())
    };
    $.ajax({
        type: 'post',
        url: '/system/create_update_user/38/' + userObj.id,
        contentType: 'application/json;charset=utf-8',
        dataType: 'json',
        data: JSON.stringify(postData),
        success: function (data) {
            if (data.status === 580) {
                $('#old-password').val('');
                new PNotify({
                    title: '提示',
                    text: '旧密码错误，请重新输入',
                    type: 'error',
                    delay: 3000,
                    addclass: "stack-bottomright",
                    stack: stack_bottomright
                });
            } else {
                $("#modify-password-modal").modal('hide');
                new PNotify({
                    title: '提示',
                    text: '修改密码成功',
                    type: 'success',
                    delay: 3000,
                    addclass: "stack-bottomright",
                    stack: stack_bottomright
                });
            }
        }, error: function (XMLHttpRequest, textStatus, errorThrown) {
            $("#modify-password-modal").modal('hide');
            new PNotify({
                title: '提示',
                text: '登录失败，服务器内部错误',
                type: 'error',
                delay: 3000,
                addclass: "stack-bottomright",
                stack: stack_bottomright
            });
        }
    })
}

// ========== 选项卡操作 ==========
$(function() {
    // 选项卡点击
    $(document).on(click, '.content_tab li', function() {
        // 切换选项卡
        $('.content_tab li').removeClass('active');
        $(this).addClass('active');
        // 切换iframe
        $('.iframe').removeClass('active');
        $('#iframe_' + $(this).data('index')).addClass('active');
        var marginLeft = ($('#tabs').css('marginLeft').replace('px', ''));
        // 滚动到可视区域:在左侧
        if ($(this).position().left < marginLeft) {
            var left = $('.content_tab>ul').scrollLeft() + $(this).position().left - marginLeft;
            $('.content_tab>ul').animate({scrollLeft: left}, 200, function() {
                initScrollState();
            });
        }
        // 滚动到可视区域:在右侧
        if(($(this).position().left + $(this).width() - marginLeft) > document.getElementById('tabs').clientWidth) {
            var left = $('.content_tab>ul').scrollLeft() + (($(this).position().left + $(this).width() - marginLeft) - document.getElementById('tabs').clientWidth);
            $('.content_tab>ul').animate({scrollLeft: left}, 200, function() {
                initScrollState();
            });
        }
    });
    // 控制选项卡滚动位置
    $(document).on(click, '.tab_left>a', function() {
        $('.content_tab>ul').animate({scrollLeft: $('.content_tab>ul').scrollLeft() - 300}, 200, function() {
            initScrollState();
        });
    });
    // 向右箭头
    $(document).on(click, '.tab_right>a', function() {
        $('.content_tab>ul').animate({scrollLeft: $('.content_tab>ul').scrollLeft() + 300}, 200, function() {
            initScrollState();
        });
    });
    // 初始化箭头状态

    // 选项卡右键菜单
    var menu = new BootstrapMenu('.tabs li', {
        fetchElementData: function(item) {
            return item;
        },
        actionsGroups: [
            ['close', 'refresh'],
            ['closeOther', 'closeAll'],
            ['closeRight', 'closeLeft']
        ],
        actions: {
            close: {
                name: '关闭',
                iconClass: 'icon-remove',
                onClick: function(item) {
                    Tab.closeTab($(item));
                },
                isEnabled: function(item) {
                    if ($(item).data('index') === 'home') {
                        $(".dropdown-menu li[data-action='close']").addClass('disabled')
                    } else {
                        $(".dropdown-menu li[data-action='close']").removeClass('disabled')
                    }
                }
            },
            closeOther: {
                name: '关闭其他',
                iconClass: 'icon-remove-circle',
                onClick: function(item) {
                    var index = $(item).data('index');
                    $('.content_tab li').each(function() {
                        if ($(this).data('index') != index) {
                            Tab.closeTab($(this));
                        }
                    });
                },
                isEnabled: function(item) {
                    if ($('.content_tab li').length <= 1) {
                        $(".dropdown-menu li[data-action='closeOther']").addClass('disabled')
                    } else if ($('.content_tab li').length <= 2 && $(item).data('index') != 'home') {
                        $(".dropdown-menu li[data-action='closeOther']").addClass('disabled')
                    } else {
                        $(".dropdown-menu li[data-action='closeOther']").removeClass('disabled')
                    }
                }
            },
            closeAll: {
                name: '关闭全部',
                iconClass: 'icon-remove-sign',
                onClick: function() {
                    $('.content_tab li').each(function() {
                        Tab.closeTab($(this));
                    });
                },
                isEnabled: function(item) {
                    if ($('.content_tab li').length <= 1) {
                        $(".dropdown-menu li[data-action='closeAll']").addClass('disabled')
                    } else {
                        $(".dropdown-menu li[data-action='closeAll']").removeClass('disabled')
                    }
                }
            },
            closeRight: {
                name: '关闭右侧所有',
                iconClass: 'icon-arrow-right',
                onClick: function(item) {
                    var index = $(item).data('index');
                    $($('.content_tab li').toArray().reverse()).each(function() {
                        if ($(this).data('index') != index) {
                            Tab.closeTab($(this));
                        } else {
                            return false;
                        }
                    });
                },
                isEnabled: function(item) {
                    var index = $(item).data('index');
                    if ($($('.content_tab li').toArray().reverse()[0]).data("index") === index) {
                        $(".dropdown-menu li[data-action='closeRight']").addClass('disabled')
                    }else {
                        $(".dropdown-menu li[data-action='closeRight']").removeClass('disabled')
                    }
                }
            },
            closeLeft: {
                name: '关闭左侧所有',
                iconClass: 'icon-arrow-left',
                onClick: function(item) {
                    var index = $(item).data('index');
                    $('.content_tab li').each(function() {
                        if ($(this).data('index') != index) {
                            Tab.closeTab($(this));
                        } else {
                            return false;
                        }
                    });
                },
                isEnabled: function(item) {
                    var index = $(item).data('index');
                    if (index === 'home') {
                        $(".dropdown-menu li[data-action='closeLeft']").addClass('disabled')
                    } else if ($('.content_tab li')[1] && $($('.content_tab li')[1]).data('index') === index) {
                        $(".dropdown-menu li[data-action='closeLeft']").addClass('disabled')
                    } else {
                        $(".dropdown-menu li[data-action='closeLeft']").removeClass('disabled')
                    }
                }
            },
            refresh: {
                name: '刷新',
                iconClass: 'icon-refresh',
                onClick: function(item) {
                    var index = $(item).data('index');
                    var $iframe = $('#iframe_' + index).find('iframe');
                    $iframe.attr('src', $iframe.attr('src'));
                }
            }
        }
    });
});
// 选项卡对象
var Tab = {
    addTab: function(title, id, url) {
        // 如果存在选项卡，则激活，否则创建新选项卡
        if ($('#tab_' + id).length == 0) {
            // 添加选项卡
            $('.content_tab li').removeClass('active');
            var tab = '<li id="tab_' + id +'" data-index="' + id + '" class="sm-fontSize active"><a class="waves-effect waves-light">' + title + '</a><i class="glyphicon glyphicon-remove"></i></li>';
            $('.content_tab>ul').append(tab);
            // 添加iframe
            $('.iframe').removeClass('active');
            var iframe = '<div id="iframe_' + id + '" class="iframe active"><iframe class="tab_iframe" src="' + url + '" width="100%" frameborder="0" scrolling="auto" onload="changeFrameHeight(this)"></iframe></div>';
            $('.content_main').append(iframe);
            initScrollShow();
            $('.content_tab>ul').animate({scrollLeft: document.getElementById('tabs').scrollWidth - document.getElementById('tabs').clientWidth}, 200, function() {
                initScrollState();
            });
        } else {
            $('#tab_' + id).trigger('click');
        }
        // 关闭侧边栏
        $('#guide').trigger(click);
    },
    closeTab: function($item) {
        var closeable = $item.data('closeable');
        if (closeable != false) {
            // 如果当前时激活状态则关闭后激活左边选项卡
            if($item.hasClass('active')) {
                $item.prev().trigger('click');
            }
            // 关闭当前选项卡
            var index = $item.data('index');
            $('#iframe_' + index).remove();
            $item.remove();
        }
        initScrollShow();
    }
}

function initScrollShow() {
    if (document.getElementById('tabs').scrollWidth > document.getElementById('tabs').clientWidth) {
        $('.content_tab').addClass('scroll');
    } else {
        $('.content_tab').removeClass('scroll');
    }
}
function initScrollState() {
    if ($('.content_tab>ul').scrollLeft() == 0) {
        $('.tab_left>a').removeClass('active');
    } else {
        $('.tab_left>a').addClass('active');
    }
    if (($('.content_tab>ul').scrollLeft() + document.getElementById('tabs').clientWidth) >= document.getElementById('tabs').scrollWidth) {
        $('.tab_right>a').removeClass('active');
    } else {
        $('.tab_right>a').addClass('active');
    }
}
// 升序排序（从小到大，用于菜单）
function sortUp(array, property){
    return array.sort(function (a, b) {
        return a[property] - b[property];
    })
}