var page = require('webpage').create();
page.open('http://s.weibo.com/top/summary', function (status) {
    if (status === "success") {
    	//此方法可以穿透打印出内部的console.log
    	page.onConsoleMessage = function(msg) {
		  	console.log(msg);
		};
        var resultHotList = page.evaluate(function() {
        	var hotList = []
		    var hotDom = document.querySelector('#realtimehot tbody').querySelectorAll('tr');
		    [].forEach.call(hotDom,function(item){
		    	itemDom = item.querySelector('.td_02 p a');
		    	hotList.push({
		    		'keyWord' : itemDom.innerText,
		    		'keyWordUrl' : ('http://s.weibo.com'+itemDom.getAttribute('href'))
		    	})
		    })
		    return hotList;
		});
		console.log(JSON.stringify(resultHotList))
    }else{
    	console.log('error')
    }
    phantom.exit();
});