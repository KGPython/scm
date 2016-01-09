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
      $("#shopCode").attr("value",checkVal)
      $(".shopList-cnt").hide();
  })

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
  })
  $(".powerSet-box .close").click(function(){
      $(".powerSet-box").hide()
  })

  $(".roles").click(function(){
      $(".roles-box").show();
  })
  $(".roles-box .close").click(function(){
      $(".roles-box").hide();
  })


  
