$(function () {

    flag1 = false;  // 用户名 是否输入合法，默认不合法
    flag2 = false;  // 密码 是否输入合法，默认不合法
    flag3 = false;  // 确认密码 是否输入合法，默认不合法
    flag4 = false;  // 邮箱 是否输入合法，默认不合法

    // 实时检测:change() blur() keyup()
    $('#username').change(function () {
        var uname = $(this).val()
          // 检测:6-18位的数字字母下划线，不能以数字开头
        if(/^[a-zA-Z_]\w{5,17}$/.test(uname)){
            flag1 = true
        }
        else {
            flag1 = false;
            alert("用户名不合法，请重新输入！")
        }
    });

    // 密码
    $('#password').change(function () {
        var passwd = $(this).val()
          // 检测:8位以上字符
        if(/^\w{8,}$/.test(passwd)){
            flag2 = true
        }
        else {
            flag2 = false;
            alert("密码错误，请重新输入！")
        }
    });
    // 确认密码
    $('#repassword').change(function () {
        var repasswd = $(this).val()
        var passwd = $('#password').val()

        if(repasswd==passwd){
            flag3 = true
        }
        else {
            flag3 = false;
            alert("密码输入不一致，请重新输入！")
        }
    });
        // 邮箱
       $('#email').change(function () {
        var em = $(this).val()
          // 检测:合法邮箱
        if(/^\w+@\w+\.\w+$/.test(em)){
            flag4 = true
        }
        else {
            flag4 = false;
            alert("邮箱输入不合法，请重新输入！")
        }
    });
       // $('form').submit(function () {
       $('button').click(function () {
           // console.log(1)

           // 点击注册按钮， 如果所有输入都合法
           if (flag1 && flag2 && flag3 && flag4){

               $('#password').val(md5($('#password').val()));

               return true
           }
           else{
               alert('信息有误，请重新输入');
               return false
           }
       });
   // 检测用户名是否存在
      $('#username').change(function () {

        $.get('/axf/checkusername/', {'username':$(this).val()}, function (data) {
            // console.log(data)

            // 可以使用
            if (data.status == 1){
                $('#username_errmsg').html(data.msg).css('color', 'green')
            }
            // 不可以使用
            else if (data.status == 0){
                $('#username_errmsg').html(data.msg).css('color', 'red')
            }
        })

    })
});

