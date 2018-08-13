$(function () {
    //密码验证
    $("#confirm_pwd").change(function () {
        pwd1 =  $("#pwd").val()
        pwd2 = $("#confirm_pwd").val()
       if(pwd1 == pwd2){
       //    提示 两次输入的密码一致
           $("#message").html("两次输入的密码一致")
           $("#message").css("color","green")
       }else{
       //    提示 两次输入的密码不一致
           $("#message").html("两次输入的密码不一致,请重新输入")
           $("#message").css("color","red")
       }
    })
    //验证用户名
    $("#username").change(function () {
        myusername = $(this).val()
        $.getJSON("/checkUser",{"username":myusername},function (data) {
            if (data["code"]=="200"){
                $("#user_register_iofo").html(data["msg"]).css("color","green")
            }
            if (data["code"] == 400){
                $("#user_register_iofo").html(data["msg"]).css("color","red")
            }
        })
    })

})

//检查是否能提交
function  checkInput() {
        //1.密码长度
        //2.用户名是否可用，字符合法
        //3.密码是否一致
        //4.邮箱是否被注册
        pwd$ =  $("#pwd")
        pwd1 =  pwd$.val()
        pwd2 =  $("#confirm_pwd").val()
        if (pwd1 != pwd2){
            return false
        }
        color = $("#user_register_iofo").attr("color")
        if (color == "red"){
            return false
        }
        // if (pwd1.length < 6){
        //     return false
        // }
         pwd = $("#pwd").val()
        res = md5(pwd)
        $("#pwd").val(res)
    }