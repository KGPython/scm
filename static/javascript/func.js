$(".all").click(function(){
    var check_status=$(this).prop('checked');
    // alert(check_status)
    if(check_status){
        $(this).parent().siblings().find("input").prop('checked',true);
    }else{
        $(this).parent().siblings().find("input").prop('checked',false);
    }
});