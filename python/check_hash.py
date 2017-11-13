#!/usr/bin/env python
# -*- utf-8 -*- 

'check MD5'

import hashlib
import os
import sys
sys.path.append('.')
from check_ver import find_dlls_has_diff_time 

def check_dlls_version(src_path, filelist):
	file_to_md5 = {}
	for (root, dirs, files) in os.walk(src_path):
		for file in files:
			if file in filelist:
				full_path = os.path.join(root, file)
				# print(full_path)
				hash = calc_md5(full_path)
				if file in file_to_md5:
					if hash not in file_to_md5[file]:
						file_to_md5[file].append(hash)
				else:
					file_to_md5[file] = [hash]

	for (file, md5_list) in file_to_md5.items():
		distinct_items = list(set(md5_list))
		if len(distinct_items) > 1:
			print('')
			print(file)
			for md5 in md5_list:
				print(md5)

def calc_md5(filepath):
	with open(filepath, 'rb') as f:
		md5obj = hashlib.md5()
		md5obj.update(f.read())
		hash = md5obj.hexdigest()
		return hash

def main():

	if len(sys.argv) != 2:
		print('Usage: python check_hash.py [path of build package]')
		sys.exit(1)
	filepath = os.path.normcase(sys.argv[1])
	if not os.path.exists(filepath):
		print('Error: path {0} does not exist.'.format(filepath))
		sys.exit(1)

	print(' Check duplidated dll in package: ' + filepath)

	files = find_dlls_has_diff_time(filepath)

	print('check MD5 for directory: ' + filepath)
	check_dlls_version(filepath, files)

if __name__ == '__main__':
	main()


