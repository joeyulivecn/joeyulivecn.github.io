#!/usr/bin/env python
# -*- coding: UTF-8 -*-

# check duplicated version of dlls in same solution

import os
import sys
import datetime

sys.path.append('.')
import clr
import System
from System.Diagnostics import FileVersionInfo

def find_dlls_has_diff_time(src_path):
    dll_dict = {}
    dll_list =[]
    
    for root, dirs, files in os.walk(src_path):       
        for file in files:
            if os.path.splitext(file)[1] == '.dll':
                full_path = os.path.join(root, file)
                mtime = os.stat(full_path).st_mtime
                mtime_str = datetime.datetime.fromtimestamp(mtime)
                filemtime = mtime_str.strftime('%Y-%m-%d %H:%M')
                if file in dll_dict:
                    dll_dict[file].append(filemtime)
                else:
                    mtimelist = []
                    mtimelist.append(filemtime)
                    dll_dict[file] = mtimelist                    

    for (file, mtimes) in dll_dict.items():
        distinct_items = list(set(mtimes))
        if len(distinct_items) > 1:
            print(file)
            dll_list.append(file)
            distinct_items.sort();
            for mtime in distinct_items:
                print(mtime)
    return dll_list   

def find_dlls_has_diff_ver(src_path, version):
    dll_dict = {}
    dll_list =[]
    
    for root, dirs, files in os.walk(src_path):       
        for file in files:
            if os.path.splitext(file)[1] == '.dll' and (file.startswith('HisClient.') or file.startswith('HisProxy.') or file.startswith('HisService.') or file.startswith('SI.') or file.startswith('His.')):
                full_path = os.path.join(root, file)
                ver = FileVersionInfo.GetVersionInfo(full_path).FileVersion

                if ver != version and ver != '1.0.0.0':
                    print(file)
                    print(ver)

                if file in dll_dict:
                    dll_dict[file].append(ver)
                else:
                    verlist = []
                    verlist.append(ver)
                    dll_dict[file] = verlist                    

    for (file, versions) in dll_dict.items():
        distinct_items = list(set(versions))
        if len(distinct_items) > 1:
            print(file)
            dll_list.append(file)
            distinct_items.sort();
            for ver in distinct_items:
                print(ver)
    return dll_list   

def main():
    if len(sys.argv) != 2:
        print('Usage: python check_ver.py [path of build package]')
        sys.exit(1)

    filepath = os.path.normcase(sys.argv[1])

    if not os.path.exists(filepath):
        print('Error: path {0} does not exist.'.format(filepath))
        sys.exit(1)

    print(' Check duplidated dll in package: ' + filepath)

    dll_list = find_dlls_has_diff_ver(filepath, '1.0.0.467')

    if len(dll_list) > 0:
        print('Error')
        sys.exit(1)

    print('No Issue.')

if __name__ == '__main__':
    main()

