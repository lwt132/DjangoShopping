$(function () {
    //+加点击事件
    $(".addCartNum").click(function () {
        addCartEle = $(this)
        cartDataid = addCartEle.parents("li").attr("cartDataid")
        $.getJSON("/app/addOrSubCart/",{"cartDataid":cartDataid,"action":"add"},function (data) {
            if (data["code"]=="201"){
                addCartEle.prev().html(data["num"])
                //--------------------------------------------------------计算价格，数量
                priceNumChange()
                //--------------------------------------------------------
            }
        })
    })

//    -减点击事件
    $(".subCartNum").click(function () {
        subCartEle = $(this)
        cartDataid = subCartEle.parents("li").attr("cartDataid")
        $.getJSON("/app/addOrSubCart/",{"cartDataid":cartDataid,"action":"sub"},function (data) {
            if (data["code"]=="301"){
                subCartEle.next().html(data["num"])
            }
            if (data["code"] == "302"){  //删除了
                subCartEle.parents("li").remove()
             //--没有商品付款提示变化---------------------------------------------------------------
                noselectList = []
                $(".is_chooice").each(function () {
                    isselect = $(this).attr("isselect")
                    cartid = $(this).parents("li").attr("cartDataid")
                    if (isselect == "False"){
                        noselectList.push(cartid)
                    }
                })
                if (noselectList.length == 0){
                    $("#nogoodToCart").html("去购物")
                }
             //-----------------------------------------------------------------
            }
            //----------------------------------------------------计算价格，数量
            priceNumChange()
            //----------------------------------------------------
        })
    })

//   商品勾选..---监听全选
    $(".is_chooice").click(function () {
        goodSelectEle = $(this)
        cartDataid = goodSelectEle.parents("li").attr("cartDataid")
        $.getJSON("/app/cartGoodSelect/",{"cartDataid":cartDataid},function (data) {
            if (data["code"] == "200"){
                if (data["isselect"]){
                    goodSelectEle.find("span").html("√")
                    goodSelectEle.attr("isselect","True")
                }
                else{
                    goodSelectEle.find("span").html("")
                    goodSelectEle.attr("isselect","False")
                }
                // allSelect() //监听全选
                //商品价格，数量-----------------------------------------------------
                selectList = []
                noselectList = []
                totalPrice = 0
                totalNum = 0
                $(".is_chooice").each(function () {
                    isselect = $(this).attr("isselect")
                    // console.log(isselect)
                    cartid = $(this).parents("li").attr("cartDataid")
                    if (isselect == "True"){
                        selectList.push(cartid)
                        //计算总价和数量
                        goodOnePrice = $(this).parents("li").find("a span").text() //选中物品价格
                        goodNum = $(this).parents("li").find("section span").text()
                        totalPrice += (parseFloat(goodNum)*parseFloat(goodOnePrice))
                        totalNum += parseFloat(goodNum)
                    }
                    else if (isselect == "False"){
                        noselectList.push(cartid)
                    }
                })
                totalPrice = totalPrice.toFixed(2)
                console.log(totalPrice)
                console.log(totalNum)
                //总价，数量
                $("#totalPrice").html("总价："+totalPrice + "元")
                $("#totalNum").html("共计:" +totalNum)

                //判断全选
                if (noselectList.length > 0){
                    $("#allSelect").find("span").html("")
                    $("#allSelect").attr("allSelect","False")
                }
                else {
                    $("#allSelect").find("span").html("√")
                    $("#allSelect").attr("allSelect","True")
                }
            //    --------------------------------------------------------------
            }
        })
//在下面调用方法会出错，原因每次读取的都是点击之前的状态,应该写在上面--》allselect()
//            **** allSelect() ****
    })


//    点击全选
    $("#allSelect").click(function () {
        allSelectEle = $(this)
        isselectCartIdList = [] //选中物品 cartid
        noselectCartIdList  = [] //未选中物品 cartid
        $(".menuList").each(function () {
            goodLi = $(this)
            cartDataid = goodLi.attr("cartDataid")
            spanisselect = goodLi.find("div span").attr("isselect")
            // console.log(spanisselect)
            if (spanisselect == "True"){
                isselectCartIdList .push(cartDataid)
            }
            else{
                noselectCartIdList .push(cartDataid)
            }
        })
        //全选变成  ---》全不选
        if ((isselectCartIdList.length + noselectCartIdList.length) == isselectCartIdList.length){
            // console.log("---------------1")
            $.getJSON("/app/cartAllSelect/",{"cartids":isselectCartIdList.join("#"),"action":"allSelectChange"},function (data) {
                if(data["code"]=="201"){
                    $(".menuList").each(function () {
                        $(this).find("div span").attr("isselect","False")
                        $(this).find("div span span").html("")
                    })
                    allSelectEle.find("span").html("")
                    allSelectEle.attr("allSelect","False")
                }
                priceNumChange()
            })
        }
        //没有全选中变全选中
        if(noselectCartIdList.length>0){
            // console.log("2-------------")
            $.getJSON("/app/cartAllSelect/",{"cartids":noselectCartIdList.join("#"),"action":"noAllSelect"},function (data) {
                if (data["code"] == "202"){
                   $(".menuList").each(function (){
                       $(this).find("div span").attr("isselect","True")
                       $(this).find("div span span").html("√")
                   })
                    allSelectEle.find("span").html("√")
                    allSelectEle.attr("allSelect","True")
                }
                priceNumChange()
            })
        }
    })

})

//监听全选
// function allSelect() {
//         selectList = []
//         noselectList = []
//         $(".is_chooice").each(function () {
//             isselect = $(this).attr("isselect")
//             // console.log(isselect)
//             cartid = $(this).parents("li").attr("cartDataid")
//             if (isselect == "True"){
//                 selectList.push(cartid)
//             }
//             else if (isselect == "False"){
//                 noselectList.push(cartid)
//             }
//         })
//         // console.log(selectList)
//         // console.log(noselectList)
//
//         if (noselectList.length > 0){
//             $("#allSelect").find("span").html("")
//             $("#allSelect").attr("allSelect","False")
//         }
//         else {
//             $("#allSelect").find("span").html("√")
//             $("#allSelect").attr("allSelect","True")
//         }
//
// }

function priceNumChange() {
            totalPrice = 0
            totalNum = 0
            $(".is_chooice").each(function () {
                isselect = $(this).attr("isselect")
                if (isselect == "True"){
                    //计算总价和数量
                    goodOnePrice = $(this).parents("li").find("a span").text() //选中物品价格
                    goodNum = $(this).parents("li").find("section span").text()
                    totalPrice += (parseFloat(goodNum)*parseFloat(goodOnePrice))
                    totalNum += parseFloat(goodNum)
                }
            })
            totalPrice = totalPrice.toFixed(2)
            console.log(totalPrice)
            console.log(totalNum)
            //总价，数量
            $("#totalPrice").html("总价："+totalPrice + "元")
            $("#totalNum").html("共计:" +totalNum)

}