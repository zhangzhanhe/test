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
        // $(this).css({"width":starRates,"height":"100%"});
    }

    $("input").change(function(){
        $("i").starRate({"starRates":$("input").val()});
    });
});