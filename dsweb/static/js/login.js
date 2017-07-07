$(function () {
    name_ok = true;
    pwd_ok = true;
    $('#change').css({'cursor': 'pointer'}).click(function () {
        $('#yzm_img').prop('src', $('#yzm_img').prop('src') + 1);
    });


    $('.name_input').keyup(function () {

        if ($(this).val() == "") {
            $(this).next().html('用户名不能为空').show();

        }
        else {
            $(this).next().hide()

        }
    });

    $('.name_input').blur(function () {
        var user_name = $('.name_input').val();

        if (user_name.length < 5 || user_name.length > 20) {

            $(this).next().html('请输入5-15位英文或数字').show();
            name_ok = false;
        }
        else {
            name_ok = true;
            $(this).next().hide()
        }

    });
    $('.pass_input').blur(function () {

        var user_pwd = $('.pass_input').val();
        if (user_pwd.length < 6 || user_pwd.length > 15) {
            $(this).next().html('密码最少6位,最多15位').show();
            pwd_ok = false;
        }
        else {
            pwd_ok = true
            $(this).next().hide()

        }
    });
    $('#reg_form').submit(function () {
        $('.name_input').blur();
        $('.pass_input').blur();
        return name_ok && pwd_ok;
    });
    if ('{{yzm_error}}' == '1') {
        $('.user_error').html('验证码错误').show();


    }
    if ('{{name_error}}' == '1' || '{{pwd_error}}' == '1') {
        $('.user_error').html('用户名错误或密码').show();

    }

});