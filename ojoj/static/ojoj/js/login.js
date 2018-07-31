/*
 var $loginFrame = $('#login-frame');
 var $captcha = $('#captcha-img,#captcha-tip');
 */
var $loginBtn = $('#login-btn');
var $accountInput = $('#account-input');
var $passwordInput = $('#password-input');
/*
 var $captchaInput = $('#captcha-input');
 */

var host = "http://39.108.149.69/";
$(function () {
    $accountInput.bind('keydown', enterSubmit);
    $passwordInput.bind('keydown', enterSubmit);
    $loginBtn.bind('click', formSubmit);
});

function enterSubmit(ev) {
    if(ev.keyCode == 13){
        formSubmit(ev);
    }
}

function formSubmit(e) {
    e.stopPropagation();
    e.preventDefault();
    // var selfArguments = arguments;
    var account = $accountInput.val();
    var password = $passwordInput.val();
    /*
     var captcha = $captchaInput.val();
     */
    // 判空
    if(account === '') {
        showMessage('账号不能为空！', '#account-input', 1);
        return;
    } else if(password === '') {
        showMessage('密码不能为空！', '#password-input', 1);
        return;
    }/* else if(captcha === '') {
     showMessage('验证码不能为空！', '#captcha-input', 1);
     return;
     }
     */
    var postData = {
        username: account,
        password: password
        // password: passwordEncrypt(password),
        // captcha: captcha
    };
    $.ajax({
        type:'post',
        url:host + 'users/login',
        contentType:'application/json;charset=utf-8',
        dataType:'json',
        data: JSON.stringify(postData),
        success:function(data){
            console.log(data);
            switch(data.status){
                case 200:
                    new PNotify({
                        title: '登录',
                        text: '登录成功',
                        type: 'success',
                        delay: 3000,
                        addclass: "stack-bottomright",
                        stack: stack_bottomright
                    });
                    window.location.href = '/index';
                    break;
                /*
                 case 310:
                 new PNotify({
                 title: '登录失败',
                 text: '验证码错误或已过期',
                 type: 'error',
                 delay: 3000,
                 addclass: "stack-bottomright",
                 stack: stack_bottomright
                 });
                 $captchaInput.val("");
                 captchaClick();
                 break;
                 */
                case 405:
                    new PNotify({
                        title: '登录失败',
                        text: '密码错误或账号错误',
                        type: 'error',
                        delay: 3000,
                        addclass: "stack-bottomright",
                        stack: stack_bottomright
                    });
                    $captchaInput.val("");
                    captchaClick();
                    break;
                case 402:
                    new PNotify({
                        title: '登录失败',
                        text: '登录出错',
                        type: 'error',
                        delay: 3000,
                        addclass: "stack-bottomright",
                        stack: stack_bottomright
                    });
                    // $captchaInput.val("");
                    // captchaClick();
                    break;
                /*
                case 415:
                    $.getScript("/encrypt/javascript",function(){  //加载encrypt.js,成功后，并执行回调函数
                        selfArguments.callee();
                    });
                    break;
                */
            }
        },error:function(XMLHttpRequest, textStatus, errorThrown){
            new PNotify({
                title: '登录失败',
                text: '服务器内部出错，或网络出错！',
                type: 'error',
                delay: 3000,
                addclass: "stack-bottomright",
                stack: stack_bottomright
            });
        }
    });
}

/*
 // 密码加密
 function passwordEncrypt(password) {
 return hex_md5(encrypt(password));
 }
 */

// 不能为空的提示
function showMessage(msg, selector, type) {
    layer.tips(msg, selector, {
        tips: type
    });
}
