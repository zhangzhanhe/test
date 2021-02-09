//遍历是否
let tabLinkList = localStorage.tabLinkList;
if(tabLinkList){
	rendList(JSON.parse(tabLinkList))
}else{
	document.querySelector('.link-list').innerHTML = '<div>暂无保存记录</div>';
}
function rendList(list){
	let linkDom = '';
	list.forEach((item,index)=>{
		linkDom = `${linkDom}<div class="link-item"><a class="item-link" id="link${index}" href="${item.link}">${item.title}</a><span class="del-item" id="del${index}">删除</span></div>`;
	})
	document.querySelector('.link-list').innerHTML = linkDom;
}
document.querySelector('.add-link').addEventListener('click',()=>{
	let tabLinkList = localStorage.tabLinkList;
	chrome.tabs.getSelected(null,function(tab){
		tabLinkList = tabLinkList ? JSON.parse(tabLinkList) : [];
		tabLinkList.push({
			title : tab.title,
			link : tab.url
		})
		rendList(tabLinkList);
		localStorage.tabLinkList = JSON.stringify(tabLinkList);
	})
})
document.querySelector('.link-list').addEventListener('click',(e)=>{
	let index = e.target.id.replace(/[^0-9]/ig,"");
	let tabLinkList = JSON.parse(localStorage.tabLinkList);
	if(e.target.className.indexOf('del-item') > -1){
		tabLinkList.splice(index,1);
		rendList(tabLinkList);
		localStorage.tabLinkList = JSON.stringify(tabLinkList);
	}else if(e.target.className.indexOf('item-link') > -1){
		chrome.tabs.create({
			url : tabLinkList[index].link
		});
	}
})
