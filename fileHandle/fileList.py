import os;
def mapDir(dirName,resultList):
	for item in os.listdir(dirName):
		absoulteItem = os.path.join(dirName,item);
		if os.path.isfile(absoulteItem):
			resultList.append(item);
		else:
			result = mapDir(absoulteItem,[]);
			resultList.append({item:result});
	return resultList;

exeDir = input('请输入执行目录');

print(mapDir(exeDir,[]));