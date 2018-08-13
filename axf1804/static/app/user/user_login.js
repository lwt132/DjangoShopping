
function checkInput() {
    pwd = $("#pwd").val()
    res = md5(pwd)
    $("#pwd").val(res)

}