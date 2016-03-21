function myBrowser(){
    var userAgent = navigator.userAgent; //取得浏览器的userAgent字符串
    var isOpera = userAgent.indexOf("Opera") > -1; //判断是否Opera浏览器
    var isIE = userAgent.indexOf("compatible") > -1 && userAgent.indexOf("MSIE") > -1 && !isOpera; //判断是否IE浏览器
    var isFF = userAgent.indexOf("Firefox") > -1; //判断是否Firefox浏览器
    var isSafari = userAgent.indexOf("Safari") > -1; //判断是否Safari浏览器

    if (isIE) {
        var reIE = new RegExp("MSIE (\\d+\\.\\d+);");
        reIE.test(userAgent);
        var fIEVersion = parseFloat(RegExp["$1"]);
        var IE55 = fIEVersion == 5.5;
        var IE6 = fIEVersion == 6.0;
        var IE7 = fIEVersion == 7.0;
        var IE8 = fIEVersion == 8.0;

        if (IE7 || IE8) {
            return "IE7 AND IE8";
        }
    }
}

function myBrowser2(){
    var Sys = {};
    var ua = navigator.userAgent.toLowerCase();
    var s;
    (s = ua.match(/rv:([\d.]+)\) like gecko/)) ? Sys.ie = s[1] :
    (s = ua.match(/msie ([\d.]+)/)) ? Sys.ie = s[1] :
    (s = ua.match(/firefox\/([\d.]+)/)) ? Sys.firefox = s[1] :
    (s = ua.match(/chrome\/([\d.]+)/)) ? Sys.chrome = s[1] :
    (s = ua.match(/opera.([\d.]+)/)) ? Sys.opera = s[1] :
    (s = ua.match(/version\/([\d.]+).*safari/)) ? Sys.safari = s[1] : 0;

    if (Sys.ie <= 8.0) {
        return true;
    }else{
        return false;
    }
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
    $(".shopList-cnt").toggle();
});
$(".shopSet").click(function(){
    $(".shopList-cnt").hide();
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
    var check_status=$(this).prop('checked');
    // alert(check_status)
    if(check_status){
        $(this).parent().siblings().find("input").prop('checked',true);
    }else{
        $(this).parent().siblings().find("input").prop('checked',false);
    }
});
  

//权限管理
$(".powerSet").click(function(){
    $(".powerSet-box").toggle();
});
$(".powerSet-box .close").click(function(){
    $(".powerSet-box").hide();
});

$(".roles").click(function(){
    $(".roles-box").toggle();
});
$(".roles-box .close").click(function(){
    $(".roles-box").hide();
});


//不含税金额（cmoney）求和
$(document).on('blur','input[name=cmoney]',function(){
    var trs = $("#invoiceTable").find("tr");
    cmoneySum=0.00;
    jshjSum=0.00;
    trs.each(function(){
        var cmoney = $(this).find('td').eq('3').find('input').val();
        if(cmoney){
            cmoneySum += parseFloat(cmoney,2);
        }
        var csh = $(this).find('td').eq('4').find('input').val();
        if(!csh){
            csh = 0.0;
        }
        var jsum = parseFloat(csh)+parseFloat(cmoney);
        if(jsum){
             jshjSum += parseFloat(jsum,2);
        }

        $(this).find('td').eq('6').find('input').val(cmoney);
        $(this).find('td').eq('5').find('input').val(jsum);
    });
    $("#cmoneySum").text(parseFloat(cmoneySum).toFixed(2));
    $("#jshjSum").text(parseFloat(jshjSum).toFixed(2));
});
//税额（csh）求和
$(document).on('blur','input[name=csh]',function(){
    var trs = $("#invoiceTable").find("tr");
    cshSum=0.00;
    jshjSum=0.00;
    trs.each(function(){
        var csh = $(this).find('td').eq('4').find('input').val();
        if(csh){
            cshSum += parseFloat(csh,2);
        }

        var cmoney = $(this).find('td').eq('3').find('input').val();
        if(!cmoney){
            cmoney = 0.0;
        }
        var jsum =  parseFloat(csh)+parseFloat(cmoney);
        if(jsum){
             jshjSum += parseFloat(jsum,2);
        }

        $(this).find('td').eq('5').find('input').val(jsum);
    });
    $("#cshSum").text(parseFloat(cshSum).toFixed(2));
    $("#jshjSum").text(parseFloat(jshjSum).toFixed(2));
});
//税额（jshj）求和
$(document).on('blur','input[name=jshj]',function(){
    var trs = $("#invoiceTable").find("tr");
    jshjSum=0.00;
    trs.each(function(){
        var jshj = $(this).find('td').eq('5').find('input').val();
        if(jshj){
            jshjSum += parseFloat(jshj,2);
        }
    });
    $("#jshjSum").text(parseFloat(jshjSum).toFixed(2));
});



