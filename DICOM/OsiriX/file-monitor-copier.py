#!/usr/bin/env python
# -*- coding: UTF-8 -*-
__author__ = 'AlexanderK'

'''
Script to monitor OsiriX image folder for new files and to copy them to the needed folder
Written because no PACS server on the other end is available.
used to transfer images to dropbox-like services
'''
import ConfigParser, codecs
import os
import time
import shutil


def open_config():
    # открывает файл конфига, если такового нет - записывает значения из примера
    localDir = os.path.dirname(__file__)
    configFile = os.path.join(localDir, "file-monitor-copier.ini")
    if os.path.exists(configFile):
        Config.readfp(codecs.open(configFile, 'r', 'utf-8'))
    else:
        print "Fill in the sample config file and restart"       

        
def find_greatest_folder(folders):
    greatest = 0
    for folder in folders:
        tmp = int(folder)
        #print tmp.__str__() + " - " + greatest.__str__()
        if int(folder) > greatest:
            greatest = tmp

    return greatest


def list_folders(path):
    return [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]


def list_files(path):
    return [(f, None) for f in os.listdir(path)]


def process_file(file, path):
    fullpath = os.path.join(path, file)
    size = os.stat(fullpath).st_size
    if size > size_threshold:
        full_dest_path = get_dest_path()
        print "To process - " + file + " size - " + size.__str__()
        shutil.copyfile(fullpath, os.path.join(full_dest_path, file))
    else:
        print "Skip - " + file + " size - " + size.__str__()
    return 1


def get_dest_path():
    datepath = time.strftime("%Y-%m-%d").__str__()
    timepath = time.strftime("%H-%M").__str__()
    tmpdatepath = os.path.join(dest_path, datepath)
    tmptimepath = os.path.join(tmpdatepath, timepath)
    #if not os.path.isdir(tmpdatepath):
    #    os.mkdir(tmpdatepath)
    if not os.path.isdir(tmptimepath):
        os.makedirs(tmptimepath)

    return tmptimepath

print "###########################"
print "# Monitoring script start #"    
print "#     ver. 2014-02-06     #" 
print "###########################"
    
path_to_watch = ""
dest_path = ""
size_threshold = ""

Config = ConfigParser.ConfigParser()
open_config()
path_to_watch = Config.get("Local", "path_to_watch")
dest_path = Config.get("Local", "dest_path")
size_threshold = int(Config.get("Local", "size_threshold"))

#folders listing init    
folders_before = list_folders(path_to_watch)

#find main monitor folder
greatest_folder = find_greatest_folder(folders_before)

#initial file listing
files_in_folder = list_files(os.path.join(path_to_watch, greatest_folder.__str__()))

while 1:
    time.sleep(5)

    files_after = list_files(os.path.join(path_to_watch, greatest_folder.__str__()))
    added = [f for f in files_after if not f in files_in_folder]
    removed = [f for f in files_in_folder if not f in files_after]
    if added:
        print '###################################### ' + time.strftime("%H-%M-%S")
        for file in added:
            process_file(file[0], os.path.join(path_to_watch, greatest_folder.__str__()))
    if removed:
        pass
    files_in_folder = files_after

    # check for new folder to monitor
    after = list_folders(path_to_watch)
    after_greatest_folder = find_greatest_folder(after)

    if greatest_folder != after_greatest_folder:
        greatest_folder = after_greatest_folder
        print "Next monitor folder - " + greatest_folder.__str__()
