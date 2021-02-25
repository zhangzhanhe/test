//给页面注入jquery
$('.tool-item').click(function(){
	let cmd = $(this).attr('id');
	sendMessageToContentScript({
		cmd : cmd
	},(res)=>{
		console.log(res);
	})
})

//给后台发送消息接口
function sendMessageToContentScript(message, callback){
	chrome.tabs.query({active: true, currentWindow: true}, function(tabs){
		chrome.tabs.sendMessage(tabs[0].id, message, function(response){
			if(callback) callback(response);
		});
	});
}