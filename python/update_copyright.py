#! /usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import re
import sys

def update_copyright(dir):
	for root, dirs, files in os.walk(dir):
		for file in files:
			if file == 'AssemblyInfo.cs':
				full_file_path = os.path.join(root, file)
				print(full_file_path)
				lines = []
				with open(full_file_path, 'r', encoding='UTF-8') as f_r:
					for line in f_r.readlines():
						lines.append(line)

				with open(full_file_path, 'w', encoding='UTF-8') as f:
					for line in lines:
						if 'AssemblyCopyright' in line:
							line= re.sub(r'\[assembly: AssemblyCopyright[\S|\s]+\]', '[assembly: AssemblyCopyright("")]', line)
						elif 'AssemblyCompany' in line:
							line= re.sub(r'\[assembly: AssemblyCompany[\S|\s]+\]', '[assembly: AssemblyCompany("")]', line)
						f.write(line)

def main():
	if len(sys.argv) != 2:
		print('Usage: python update_copyright.py path')
		sys.exit(1)

	path = os.path.normcase(sys.argv[1])

	if not os.path.exists(path):
		print('Error: path {0} does not exist.'.format(path))
		sys.exit(1)

	print('begin updating copyright in path: ' + path)

	os.system('pause')

	update_copyright(path)

if __name__ == '__main__':
	main()