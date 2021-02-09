import os;
def mapDir(dirName):
	resultList = set(); 
	for item in os.listdir(dirName):
		absoulteItem = os.path.join(dirName,item);
		if os.path.isfile(absoulteItem):
			resultList.add(os.path.splitext(item)[1]);
		else:
			result = mapDir(absoulteItem);
			resultList = set.union(result,resultList);

	return resultList;

exeDir = input('请输入执行目录');

print(mapDir(exeDir));
