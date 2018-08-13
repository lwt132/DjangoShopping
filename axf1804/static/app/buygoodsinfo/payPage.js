$(function () {
    $("#pay").click(function () {
        goodsProductid =[]
        goodsnum=[]
        orderNum=$("#goodList").attr("orderNum")
        $(".buygoods").each(function () {
            buyEle=$(this)
            goodsProductid.push(buyEle.attr("goodsProductid"))
            goodsnum.push(buyEle.attr("num"))
        })
        $.getJSON("/app/payDeal/",{"goodsProductid":goodsProductid.join("#"),"goodsnum":goodsnum.join("#"),"orderNum":orderNum},function (data) {
            alert("支付成功,总价：" + data["totalPrice"] + "元")
            window.open("/app/mine/",target="_self")
        })
    })

    $("#nopay").click(function () {
        window.open("/app/mine/",target="_self")
    })
})