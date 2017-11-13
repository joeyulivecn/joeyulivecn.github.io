#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import xml.dom.minidom
import os
import sys

def check_duplicates(filepath):
	project_duplicated = []
	with open(filepath) as f:
		project_list = []
		index = 0
		for line in f.readlines():
			index = index + 1
			if 'ProjectToBuild Include=' in line and line in project_list:
				tmp_str = ''
				tmp_str = tmp_str + str(index)
				tmp_str = tmp_str + ' ' + line
				project_duplicated.append(tmp_str)
			else:
				project_list.append(line)
	return project_duplicated

def check_duplicates_xml(filepath):
	dom = xml.dom.minidom.parse(filepath)
	root = dom.documentElement
	projects_to_build = root.getElementsByTagName('ProjectToBuild')
	project_duplicated = []
	project_list = []
	
	index = 0
	for p in projects_to_build:
		index = index + 1
		project = p.getAttribute('Include')

		if project in project_list:
			tmp_str = ''
			tmp_str = tmp_str + str(index)
			tmp_str = tmp_str + ' ' + project
			project_duplicated.append(tmp_str)
		else:
			project_list.append(project)
	
	return project_duplicated

def main():
	if len(sys.argv) != 2:
		print('Usage: python check_duplicates.py [path of all-in-one.proj]')
		sys.exit(1)

	filepath = os.path.normcase(sys.argv[1])

	if not os.path.exists(filepath):
		print('Error: path {0} does not exist.'.format(filepath))
		sys.exit(1)

	print(' Check duplidated projects in build list for file: ' + filepath)

	result = check_duplicates_xml(filepath)

	if len(result) == 0:
		print('\n Result: There is no duplicated project in build list.')
	else:
		print('\n Result: You have duplicated project in build list.')
		for line in result:
			print(' --> line #' + line)
			sys.exit(1)

if __name__ == "__main__":
	main()