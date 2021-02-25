//接收消息popup的消息
chrome.runtime.onMessage.addListener(function(request, sender, sendResponse){
	if(request.cmd){
		toolList[request.cmd]();
		sendResponse('执行成功')
	}else{
		sendResponse('未找到对应方式')
	}
});
const toolList = {
	insertJq : function(){
		var script = document.createElement('script');
		script.type = 'text/javascript';
		script.src = 'https://libs.baidu.com/jquery/2.0.0/jquery.min.js';
	    document.getElementsByTagName('head')[0].appendChild(script);
	    alert('成功');
	},
	csdnMask : function() {
		document.querySelector('.login-mark').remove();
		document.querySelector('#passportbox').remove();
	}
}