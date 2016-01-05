 //导航
$(".nav-list .nav-list-item").hover(function(){
    $(this).css({"background":"#fff"});
    $(this).find(".nav-list2").stop(true,true).show();
    $(this).find(".nav-item-icon").text("∧");
  },function(){
    $(this).css({"background":"#efefef"});
    $(this).find(".nav-list2").stop(true,true).hide();
    $(this).find(".nav-item-icon").text("∨");
  })

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


  
