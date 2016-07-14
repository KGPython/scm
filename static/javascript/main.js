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
    cshSum=0.00;
    trs.each(function(){
        var rate = $(this).find('td').eq('1').find('input').val();
        var cmoney = $(this).find('td').eq('3').find('input').val();
        if(cmoney){
            cmoneySum += parseFloat(cmoney);
        }
        var csh = parseFloat(rate)/100.00 * parseFloat(cmoney);
        if(csh){
            cshSum += csh;
        }else{
            csh = 0.00;
        }

        $(this).find('td').eq('4').find('input').val(parseFloat(csh).toFixed(2));

        var jsum = parseFloat(csh)+parseFloat(cmoney);
        if(jsum){
             jshjSum += parseFloat(jsum);
        }

        $(this).find('td').eq('5').find('input').val(jsum.toFixed(2));
        $(this).find('td').eq('6').find('input').val(jsum.toFixed(2));
    });
    $("#cmoneySum").text(parseFloat(cmoneySum).toFixed(2));
    $("#cshSum").text(parseFloat(cshSum).toFixed(2));
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
            cshSum += parseFloat(csh);
        }

        var cmoney = $(this).find('td').eq('3').find('input').val();
        if(!cmoney){
            cmoney = 0.0;
        }
        var jsum =  parseFloat(csh)+parseFloat(cmoney);
        if(jsum){
             jshjSum += parseFloat(jsum);
        }

        $(this).find('td').eq('5').find('input').val(jsum.toFixed(2));
        $(this).find('td').eq('6').find('input').val(jsum.toFixed(2));
    });
    $("#cshSum").text(parseFloat(cshSum).toFixed(2));
    $("#jshjSum").text(parseFloat(jshjSum).toFixed(2));
});
//税额（jshj）求和
$(document).on('blur','input[name=ctaxrate]',function(){
    var trs = $("#invoiceTable").find("tr");
    cmoneySum=0.00;
    jshjSum=0.00;
    cshSum=0.00;
    trs.each(function(){
        var rate = $(this).find('td').eq('1').find('input').val();
        var cmoney = $(this).find('td').eq('3').find('input').val();
        if(cmoney){
            cmoneySum += parseFloat(cmoney);
        }
        var csh = parseFloat(rate)/100.00 * parseFloat(cmoney);
        if(csh){
            cshSum += csh;
        }else{
            csh = 0.00;
        }

        $(this).find('td').eq('4').find('input').val(parseFloat(csh).toFixed(2));

        var jsum = parseFloat(csh)+parseFloat(cmoney);
        if(jsum){
             jshjSum += parseFloat(jsum);
        }

        $(this).find('td').eq('5').find('input').val(jsum.toFixed(2));
        $(this).find('td').eq('6').find('input').val(jsum.toFixed(2));
    });
    $("#cmoneySum").text(parseFloat(cmoneySum).toFixed(2));
    $("#cshSum").text(parseFloat(cshSum).toFixed(2));
    $("#jshjSum").text(parseFloat(jshjSum).toFixed(2));
});

function getYestodayDate(date){
    var yesterday_milliseconds=date.getTime()-1000*60*60*24;
    var yesterday = new Date();
    yesterday.setTime(yesterday_milliseconds);
    return yesterday;
}
 //当前日期前一天
 function getYestoday(date){
    var yesterday = getYestodayDate(date);
    var strYear = yesterday.getFullYear();
    var strDay = yesterday.getDate();
    var strMonth = yesterday.getMonth()+1;
    if(strMonth<10){
        strMonth="0"+strMonth;
    }
    if(strDay<10){
        strDay="0"+strDay;
    }
    datastr = strYear+"-"+strMonth+"-"+strDay;
    return datastr;
}
//月时间进度
function getMonthTimeProgress(date){
    var yesterday = getYestodayDate(date);
    var strYear = yesterday.getFullYear();
    var strDay = yesterday.getDate();
    var strMonth = yesterday.getMonth()+1;
    var lastDay = getLastDay(strYear,strMonth);
    var rs = (strDay*100/lastDay).toFixed(2)+"%";
    return rs;
}
//当月最后一天
function getLastDay(year,month){
     var new_year = year;    //取当前的年份
     var new_month = month++;//取下一个月的第一天，方便计算（最后一天不固定）
     if(month>12)            //如果当前大于12月，则年份转到下一年
     {
          new_month -=12;        //月份减
          new_year++;            //年份增
     }
     var new_date = new Date(new_year,new_month,1);                //取当年当月中的第一天
     return (new Date(new_date.getTime()-1000*60*60*24)).getDate();//获取当月最后一天日期
}

//excel文件下载
function pub_export(url,ucode){
    //soft_key_validator.checkKey(export_bar,url,ucode);
    export_bar(url);
}
function export_bar(url){
      window.location.href=url;
}
