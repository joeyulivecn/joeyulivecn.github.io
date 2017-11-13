import os
import sys

std = sys.stdout
output = open('output.txt', 'w')
sys.stdout = output

currentPath=os.path.abspath('.')
print currentPath
pathDisk='E:\\git_emr\\si\src\\'
buildList=pathDisk + '\\BuildList_siHis.txt'

for line in open(buildList, 'r'):
	if line != '\n':
   		print "<ProjectToBuild Include=\"$(Root)\\" + line.replace('\n', '') + "\" />"
