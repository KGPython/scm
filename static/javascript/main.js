function myBrowser(){
    var userAgent = navigator.userAgent; //取得浏览器的userAgent字符串
    var isOpera = userAgent.indexOf("Opera") > -1; //判断是否Opera浏览器
    var isIE = userAgent.indexOf("compatible") > -1 && userAgent.indexOf("MSIE") > -1 && !isOpera; //判断是否IE浏览器
    var isFF = userAgent.indexOf("Firefox") > -1; //判断是否Firefox浏览器
    var isSafari = userAgent.indexOf("Safari") > -1; //判断是否Safari浏览器
    if (isIE) {
        var IE5 = IE55 = IE6 = IE7 = IE8 = false;
        var reIE = new RegExp("MSIE (\\d+\\.\\d+);");
        reIE.test(userAgent);
        var fIEVersion = parseFloat(RegExp["$1"]);
        IE55 = fIEVersion == 5.5;
        IE6 = fIEVersion == 6.0;
        IE7 = fIEVersion == 7.0;
        IE8 = fIEVersion == 8.0;

        if (IE7 || IE8) {
            return "IE7 AND IE8"
        }
    }//isIE end
    //if (isFF) {
    //    return "FF";
    //}
    //if (isOpera) {
    //    return "Opera";
    //}
}

 //导航
$(".nav-list .nav-list-item").hover(function(){
    $(this).css({"background":"#fff"});
    $(this).find(".nav-list2").stop(true,true).show();
    $(this).find(".nav-item-icon").text("∧");
},function(){
    $(this).css({"background":"#efefef"});
    $(this).find(".nav-list2").stop(true,true).hide();
    $(this).find(".nav-item-icon").text("∨");
});

//门店列表
$(".shopList-icon").click(function(){
    $(".shopList-cnt").show();
});
$(".shopSet").click(function(){
    $(".shopList-cnt").show();
});
$(".shopList-cnt .enter").click(function(){
    var checkVal='';
    var shopNm='';
    $(".shopList-cnt table input").each(function(){
        var check_status=$(this).prop('checked');
        if(check_status){
            checkVal += $(this).attr('value');
            checkVal += ',';
        }
    });
    $("#shopCode").attr("value",checkVal);
    $(".shopList-cnt").hide();
});

$(".shopList-cnt .close").click(function(){
    $(".shopList-cnt").hide();
});
$(".all").click(function(){
    var check_status=$(this).prop('checked')
    // alert(check_status)
    if(check_status){
        $(this).parent().siblings().find("input").prop('checked',true);
    }else{
        $(this).parent().siblings().find("input").prop('checked',false);
    }
});
  

//权限管理
$(".powerSet").click(function(){
    $(".powerSet-box").show()
});
$(".powerSet-box .close").click(function(){
    $(".powerSet-box").hide()
});

$(".roles").click(function(){
    $(".roles-box").show();
});
$(".roles-box .close").click(function(){
    $(".roles-box").hide();
});


//不含税金额（cmoney）求和
$(document).on('blur','input[name=cmoney]',function(){
    var trs = $("#invoiceTable").find("tr");
    cmoneySum=0.00;
    trs.each(function(){
        var cmoney = $(this).find('td').eq('3').find('input').val();
        if(cmoney){
            cmoneySum += parseFloat(cmoney,2)
        }
    });
    $("#cmoneySum").text(parseFloat(cmoneySum).toFixed(2))
});
//税额（csh）求和
$(document).on('blur','input[name=csh]',function(){
    var trs = $("#invoiceTable").find("tr");
    cshSum=0.00;
    trs.each(function(){
        var csh = $(this).find('td').eq('4').find('input').val();
        if(csh){
            cshSum += parseFloat(csh,2)
        }
    });
    $("#cshSum").text(parseFloat(cshSum).toFixed(2))
});
//税额（jshj）求和
$(document).on('blur','input[name=jshj]',function(){
    var trs = $("#invoiceTable").find("tr");
    jshjSum=0.00;
    trs.each(function(){
        var jshj = $(this).find('td').eq('5').find('input').val();
        if(jshj){
            jshjSum += parseFloat(jshj,2)
        }
    });
    $("#jshjSum").text(parseFloat(jshjSum).toFixed(2))
});


//发票信息提交
$("#enterAjax").click(function(){
    //发票详细验证（发票进项税率和发票号）

    //获取表头信息
    var PlanPayDate = $("#PlanPayDate").val();
    var shopId = $("#shopId").val();
    var payDate = $("#payDate").val();
    var refSheetId = $("#refSheetId").val();

    var data=[];
    var trs = $("#invoiceTable").find("tr");
    var inputError = 0;
    trs.each(function(){
        inputs = $(this).find('input');
        selects = $(this).find('select');
        if(inputs.length>0){
            if(inputs.eq(0).val()>=0 && inputs.eq(0).val()<=100 && inputs.eq(1).val() && inputs.eq(1).val().length<10 ){
                data.push({
                    "cclass":selects.eq(0).val(),
                    "paytype":selects.eq(1).val(),
                    "ctaxrate":inputs.eq(0).val(),
                    "cno":inputs.eq(1).val(),
                    "cmoney":inputs.eq(2).val(),
                    "csh":inputs.eq(3).val(),
                    "kmoney":inputs.eq(5).val(),
                    "cdate":inputs.eq(7).val(),
                    "cdno":inputs.eq(8).val(),
                    "cgood":inputs.eq(9).val()
                })
            }else{
                alert("发票进项税率必须在0-100之间，\n并且发票号不能为空(长度小于10位)，\n请核对！");
                inputError++;
                data=[];
                return false;
            }
        }
    });
    console.log(data);
    if(inputError==0){
        jsonStr= JSON.stringify(data);
        $.ajax({
            type:"post",
            url:"/scm/base/supp/invoice/save",
            data:{
                "jsonStr":jsonStr,
                "PlanPayDate":PlanPayDate,
                "shopId":shopId,
                "payDate":payDate,
                "refSheetId":refSheetId
            },
            cache:false,
            dataType:"json",
            success:function(data){
                if(data.succ){
                    alert('保存成功')
                    window.location.href="/scm/base/supp/home/"
                }else{
                    alert('保存失败')
                }
            }
        })
    }

});
  
