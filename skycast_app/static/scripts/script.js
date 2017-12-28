$(document).ready(function(){

    //code goes here

    $('#header_banner').hover(function() {
        $('#sky_cast_heading').css("font-size", "72pt");
        }, function(){
        $('#sky_cast_heading').css("font-size", "66pt");
        });

    $("#header_banner").click(function(){
        document.location.href = "/";
    });

    $('.content_container').hide();
    $('.content_container').fadeIn('slow');

});