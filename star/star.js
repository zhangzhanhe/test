$(function(){
    $.fn.starRate = function(options){
        options = $.extend({
            starRates: 5
        },options);
        if( options.starRates>5 ){
            options.starRates=5;
        }
        var starRates = options.starRates/5*80+"px";
        $(this).css("width",starRates);
    }
    $("input").change(function(){
        $("i").starRate({"starRates":$("input").val()});
    });
});