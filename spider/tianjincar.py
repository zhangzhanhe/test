from io import StringIO
from io import open
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, process_pdf

import re
import math
 
 
def read_pdf(pdf):
    # resource manager
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    # device
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)
    process_pdf(rsrcmgr, device, pdf)
    device.close()
    content = retstr.getvalue()
    retstr.close()
    # 获取所有行
    lines = str(content).split("\n")
    return lines
 
def writeFile(fileContent):
    fo = open("201901.txt", "w");
    lenNum = 10;
    numList = [0]*lenNum;
    for lineStr in fileContent:
        lineArray = ' '.join(lineStr.strip().split()).split();
        try:
            if(len(lineArray) == 3 and int(lineArray[0])):
                num = int(int(lineArray[1])/1000000000000);
                lineArray.append(str(num));
                fo.write(' '.join(lineArray)+'\n');
                numList[num] = numList[num] + 1;
        except ValueError:
            print(ValueError);
    #输出结果
    fo.write('################统计结果##############\n');
    for item in range(lenNum):
        fo.write(str(item) + ' '+ str(numList[item])+'\n');
    fo.close();
 
if __name__ == '__main__':
    with open('./carList201901.pdf', "rb") as my_pdf:
        writeFile(read_pdf(my_pdf));