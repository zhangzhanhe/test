var pList;
initPassword();
//绑定添加事件
$('.add-password').on('click',function(){
	$('.mask,.add-pop').show();
})
//添加行为
$('#saveBtn').on('click',function(){
	let name = $('#addItemName').val();
	let password = $('#addPasswrod').val();
	let key = $('#addKey').val();
	let aseCode = CryptoJS.AES.encrypt(password,key).toString();
	pList.push({
		name : name,
		code : aseCode
	})
	setStorage(JSON.stringify(pList),()=>{
		promptTips('保存成功');
		$('.mask,.add-pop').hide();
		initPassword();
	})
})
//绑定查看事件
$('.password-list').on('click','.look-item',function(){
	$('body').data('pw',$(this).parents('.pword-item').data('pw'));
	$('#lookPassword').text('');
	$('.mask,.look-pop').show();
});
//根据key来接出密码
$('#lookBtn').on('click',function(){
	let key = $('#lookKey').val();
	let code = $('body').data('pw');
	var bytes  = CryptoJS.AES.decrypt(code,key);
	var originalText = bytes.toString(CryptoJS.enc.Utf8);
	$('#lookPassword').text(originalText);
});
//确认要删除吗？
$('.password-list').on('click','.del-item',function(){
	$('body').data('name',$(this).parents('.pword-item').data('name'));
	$('.mask,.del-pop').show();
});
$('#delBtn').on('click',function(){
	let name = $('body').data('name');
	pList.some((item,index)=>{
		if(item.name == name){
			pList.splice(index,1);
			return true;
		}else{
			return false;
		}
	});
	setStorage(JSON.stringify(pList),()=>{
		promptTips('删除成功');
		$('.mask,.del-pop').hide();
		initPassword();
	})
});
//关闭蒙层
$('.mask').on('click',function(){
	$('.mask,.look-pop,.add-pop,.del-pop').hide();
});
//导出文件
function initExport(){
 	$('.export-data').attr('href',window.URL.createObjectURL(new Blob([JSON.stringify(pList)])));
}
//初始化页面
function initPassword(){
	//获取缓存中的数据
	getStorage().then((res)=>{
		pList = res.psWdKey ? JSON.parse(res.psWdKey) : [];
		//渲染dom元素
		let pStr = '';
		pList.forEach((item,index)=>{
			pStr = `${pStr}<div class="pword-item" data-pw="${item.code}" data-name="${item.name}"><div id="pword{index}">${item.name}</div><div><span class="look-item" id="look${index}">查看</span><span class="del-item" id="look${index}">删除</span></div></div>`;
		});
		$('.password-list').html(pStr);
		initExport();
	});	
}
//信息提示框
function promptTips(textMes,callback,timer){
    if(!!$('#codetip').length) return false;
    var timer = timer || 2500;
    var promptDom = $('<div id="codetip"></div>').css({
        'position':'fixed',
        'left':'10%',
        'right': '10%',
        'top':'120px',
        'width' : '80%',
        'text-align':'center',
        'font-size':'16px',
        'z-index':15
    })
    promptDom.append('<p></p>').find('p').css({
        'color': '#fff',
        'display':'inline-block',
        'line-height':'24px',
        'padding':'20px',
        'background':'#000',
        'border-radius':'5px',
        'opacity':'.8'
    }).html(textMes);
    promptDom.appendTo('body');
    setTimeout(function(){
        $('#codetip').remove();
        !!callback && callback();
    },timer);
}
//设置缓存
function setStorage(value,cb){
	chrome.storage.sync.set({'psWdKey':value},()=>{
      cb && cb();
    });
}
//读取缓存
function getStorage(cb){
	return new Promise(resolve=>{
		chrome.storage.sync.get('psWdKey',(result)=>{
			resolve(result);
	    });
	})
}
