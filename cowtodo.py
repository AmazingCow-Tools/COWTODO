#!/usr/bin/python

## Imports ##
import os
from os.path import join, getsize
from pprint import pprint
import re;
from termcolor import colored;
import time;

extensions = [".py",         #python
              ".h", ".c",    #C
              ".cpp",        #C++
              ".m", ".mm",   #ObjC
              ".js", ".jsx", #Javascript
              ".php",        #PHP
              ];

tag_names = ["COWTODO",
             "COWFIX",
             "COWHACK"];

this_file_name = "cowtodo.py";

selected_files     = [];
tags_matching_dict = {};

dirs_scanned_count   = 0;
files_scanned_count  = 0;
files_selected_count = 0;
time_begin = time.clock();

for tag_name in tag_names:
    tags_matching_dict[tag_name] = [];

## Scan the directories.
for root, dirs, files in os.walk('.'):
    #Ignore hidden dirs.
    if(len(dirs) > 0 and dirs[0][0] == "."):
        dirs.remove(dirs[0]);

    dirs_scanned_count += 1;

    #For each file check if it matches with
    #our file extensions.
    for file in files:
        if(file == this_file_name):
            continue;

        files_scanned_count += 1;

        for ext in extensions:
            filename, fileext = os.path.splitext(file);
            if(ext == fileext):
                files_selected_count += 1;
                #Match, so put the file in the selected files
                #to we examinate it later.
                selected_files.append(os.path.join(root, file));


## Scan is complete, so now start check
## if the selected files has our tags.
for filename in selected_files:
    #Open the file and check each line of it.
    lines = open(filename).readlines();

    for line_no in xrange(0, len(lines)):
        line = lines[line_no];
        #Check if any tag was found.
        for tag_name in tag_names:
            search_str = ".*%s.*" %(tag_name);

            if(re.search(search_str, line) is not None):
                data = [filename, line_no, line];
                tags_matching_dict[tag_name].append(data);
                break;


## We found all tags so now format it.
# pprint(tags_matching_dict);
for tag in tags_matching_dict:
    length = len(tags_matching_dict[tag]);
    if(length == 0):
        continue;

    print "{}({}):".format(
        colored(tag, "cyan"),
        colored(length, "blue"));
    for info in tags_matching_dict[tag]:
        file = info[0];
        line = info[1];
        text = info[2].rstrip(" ").lstrip(" ").replace(tag, "").replace("\n", "");
        text = text.lstrip("#").lstrip("/").lstrip(":").lstrip(" ");

        print " {} ({}) - {}".format(
            colored(file, "red"),
            colored(line, "blue"),
            colored(text, "green"));

time_end = time.clock();
print;
print "Directories Scanned:", dirs_scanned_count;
print "Files Scanned:      ", files_scanned_count;
print "Files Selected:     ", files_selected_count;
print "Elapsed:            ", time_end - time_begin;
print;
# pprint(tags_matching_dict);
