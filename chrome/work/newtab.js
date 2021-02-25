var siteList = [];
//首次进入获取数据
getStoreData();
//打开页面
$('.site-list').on('click','.site-name',function(){
	location.href = $(this).data('url');
});
//删除数据
$('.site-list').on('click','.del-site',function(){
	$('.del-pop,.mask').show();
	$('body').data('id',$(this).data('id'));
});
//确认删除
$('#delBtn').on('click',function(){
	delStoreData($('body').data('id'));
	$('.del-pop,.mask').hide();
});
//新建
$('#addSite').on('click',function(){
	$('.add-pop,.mask').show();
});
//新建数据存储
$('#saveBtn').on('click',function(){
	let name = $('#addName').val();
	let url = $('#addUrl').val();
	let id = [...siteList].pop().id*1 + 1;
	siteList.push({
		name : name,
		url : url,
		id : id
	});
	localStorage.setItem('siteList',JSON.stringify(siteList));
	$('.add-pop,.mask').hide();
	getStoreData();
});
//渲染数据
function getStoreData(){
	//从本地存储中读取相关数据
	let demoStr = '';
	if(localStorage.getItem('siteList')){
		siteList = JSON.parse(localStorage.getItem('siteList'));
	}
	//循环遍历进入demo
	siteList.forEach((item)=>{
		demoStr = demoStr + `<div class="site-item" title="${item.name}">
			<div class="site-name" data-url="${item.url}">${item.name}</div>
			<div class="del-site" data-id="${item.id}" >删除</div>
		</div>`;
	});
	$('.site-list').html(demoStr);
	//设置导出链接
	initExport();
}
//删除数据 
function delStoreData(id){
	siteList.some((item,index)=>{
		if(item.id == id){
			siteList.splice(index,1);
			return true;
		}else{
			return false;
		}
	});
	localStorage.setItem('siteList',JSON.stringify(siteList));
	getStoreData();
}
//导出文件
function initExport(){
 	$('#exportJson').attr('href',window.URL.createObjectURL(new Blob([JSON.stringify(siteList)])));
}
