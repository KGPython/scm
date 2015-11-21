  //表单验证
  $("#save").click(function(e){
    var uName=$("#uName").val();
    if(uName==""){
      $(".uName-notice").show();
      if(e.preventDefault) {
        e.preventDefault();
      }else {
        window.event.returnValue = false;
      }
    }else{
      $(".uName-notice").hide();
    }
  })
  

  //门店列表
  $(".shopList-icon").click(function(){
    $(".shopList-cnt").show();
  });

  $(".shopList-cnt .all").click(function(){
    var check_status=$(this).prop('checked')
    // alert(check_status)
    if(check_status){
      $(this).parent().siblings().find("input").prop('checked',true);
    }else{
      $(this).parent().siblings().find("input").prop('checked',false);
    }
  });
  $(".shopList-cnt .close").click(function(){
    $(".shopList-cnt").hide();
  })


  