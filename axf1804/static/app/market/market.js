$(function () {
    $("#type_container").hide()
    $("#rank_container").hide()
    //分类
    $("#alltype").click(function () {
        $("#type_container").show()
        $("#alltype_g").removeClass().addClass("glyphicon glyphicon-arrow-up")
        $("#rank_container").hide()
        $("#allrank_g").removeClass().addClass("glyphicon glyphicon-arrow-down")
    })

    $("#type_container").click(function () {
        $("#type_container").hide()
        $("#alltype_g").removeClass().addClass("glyphicon glyphicon-arrow-down")
    })
    // #排序
    $("#allrank").click(function () {
        $("#rank_container").show()
        $("#allrank_g").removeClass().addClass("glyphicon glyphicon-arrow-up")
        $("#type_container").hide()
        $("#alltype_g").removeClass().addClass("glyphicon glyphicon-arrow-down")
    })
    $("#rank_container").click(function () {
        $("#rank_container").hide()
        $("#allrank_g").removeClass().addClass("glyphicon glyphicon-arrow-down")
    })
//    + 添加购物车
    $(".addShopping").click(function () {
        addelement = $(this)
        goodsid = addelement.attr("goodsid")
        $.getJSON("/app/addOrSubToCart",{"goodsid":goodsid,"action":"add"},function (data) {
            if (data["code"]=="201"){
                addelement.prev().html(data["num"])
            }
            if (data["code"]=="202"){
                addelement.prev().html("1")
            }
            if (data["code"]=="400"){
                // console.log(data["msg"])
                window.open("/app/loginUser/",target="_self")
            }
        })
    })
//    - 减 购物车
    $(".subShopping").click(function () {
        subelement = $(this)
        goodsid = subelement.attr("goodsid")
        $.getJSON('/app/addOrSubToCart/',{"goodsid":goodsid,"action":"sub"},function (data) {
            if (data["code"] == "301"){
                subelement.next().html("0")
            }
            if (data["code"] == "302"){
                subelement.next().html(data["num"])
            }
            if (data["code"]=="400") {
              window.open("/app/loginUser/",target="_self")
            }
        })

    })


})