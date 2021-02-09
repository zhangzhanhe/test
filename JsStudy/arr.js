//此文件记录js数组的常用方法
//push方法，向数组尾部添加元素，改变原数组，返回增加后的数组长度
arr = ['a','b','c','d'];
num = arr.push('e');
console.log(arr,num); //["a", "b", "c", "d", "e"] 5
//pop方法，删除数组最后一个元素，改变原数组，返回被删除的条目，
item = arr.pop();
console.log(arr,item); //["a", "b", "c", "d"] 'e'
//unshift，向元素首添加元素，改变原数组，返回增加后的数组长度
num = arr.unshift('z');
console.log(arr,num); //["z","a", "b", "c", "d"] 5
//shift方法，删除数组首部元素，改变原数组，返回被删除的数组条目，
item = arr.shift();
console.log(arr,item); //["a", "b", "c", "d"] 'z'
//splice，删除数组的指定元素，参数有pos（位置）和n（个数），改变原数组
