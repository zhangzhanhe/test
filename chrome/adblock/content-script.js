(function() {
	function removeAd(){
		var itemList = document.querySelector('#content_left').querySelectorAll('.c-container')
	    itemList.forEach((item,index)=>{
	    	if(item.querySelector('.ec_tuiguang_container')){
	    		item.style.display = 'none';
	    	}
	    	if(item.querySelector('.ec_tuiguang_pplink')){
	    		item.style.display = 'none';
	    	}    	
	    });
	}
	removeAd();
	setInterval(removeAd,2000);
})()