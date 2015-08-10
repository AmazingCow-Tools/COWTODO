#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █                                                  ##
##             ████████████         applepy.py - ApplePy                      ##
##           █              █       Copyright (c) 2015 AmazingCow             ##
##          █     █    █     █      www.AmazingCow.com                        ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
##                                                                            ##
##                                                                            ##
##                  This software is licensed as GPLv3                        ##
##                 CHECK THE COPYING FILE TO MORE DETAILS                     ##
##                                                                            ##
##    Permission is granted to anyone to use this software for any purpose,   ##
##   including commercial applications, and to alter it and redistribute it   ##
##               freely, subject to the following restrictions:               ##
##                                                                            ##
##     0. You **CANNOT** change the type of the license.                      ##
##     1. The origin of this software must not be misrepresented;             ##
##        you must not claim that you wrote the original software.            ##
##     2. If you use this software in a product, an acknowledgment in the     ##
##        product IS HIGHLY APPRECIATED, both in source and binary forms.     ##
##        (See opensource.AmazingCow.com/acknowledgment.html for details).    ##
##        If you will not acknowledge, just send us a email. We'll be         ##
##        *VERY* happy to see our work being used by other people. :)         ##
##        The email is: acknowledgmentopensource@AmazingCow.com               ##
##     3. Altered source versions must be plainly marked as such,             ##
##        and must notbe misrepresented as being the original software.       ##
##     4. This notice may not be removed or altered from any source           ##
##        distribution.                                                       ##
##     5. Most important, you must have fun. ;)                               ##
##                                                                            ##
##      Visit opensource.amazingcow.com for more open-source projects.        ##
##                                                                            ##
##                                  Enjoy :)                                  ##
##----------------------------------------------------------------------------##
## Imports ##
import os
import os.path;
import time;
import re;
from pprint import pprint
import termcolor;

################################################################################
## Globals                                                                    ##
################################################################################
class Globals:
    extensions = [".py",          #python
                  ".h", ".c",     #C
                  ".cpp",         #C++
                  ".m", ".mm",    #ObjC
                  ".js", ".jsx",  #Javascript
                  ".php",         #PHP
                  ".htm", ".html" #html
                  ];

    tag_names      = ["COWTODO", "COWFIX", "COWHACK"];
    this_file_name = "cowtodo.py";
    tag_entries    = {
        "COWTODO" : [],
        "COWHACK" : [],
        "COWFIX"  : []
    }

################################################################################
## Helper                                                                     ##
################################################################################
class Helper:
    @staticmethod
    def print_help():
        pass;
    
    @staticmethod
    def print_version():
        pass;

    @staticmethod    
    def clean_str(s, tag):
        s = s.replace(tag, "");
        s = s.rstrip(" ").lstrip(" ");
        s = s.lstrip("#").lstrip("/");
        s = s.lstrip(":").lstrip(" ");
        s = s.rstrip("\n");
        return s;

    @staticmethod
    def colored( msg, color):
        return termcolor.colored(msg, color);
    
    @staticmethod
    def print_output(*args):
        print "".join(map(str,args)),

################################################################################
## Tag Entry                                                                  ##
################################################################################
class TagEntry:
    def __init__(self, filename):
        self.filename = filename;
        self.data     = {};
    
    def add(self, tag_type, line_no, line_str):
        #Check if we already added something in this tag.
        if(tag_type not in self.data):
            self.data[tag_type] = [];            
        self.data[tag_type].append([line_no, line_str]);


################################################################################
## Scan/Parse Functions                                                       ##
################################################################################
def scan(start_path):
    ## Scan the directories.
    for root, dirs, files in os.walk(start_path):
        #Ignore hidden dirs.
        if(len(dirs) > 0 and dirs[0][0] == "."):
            dirs.remove(dirs[0]);

        #For each file check if it matches with our file extensions.
        for file in files:
            #We found this file. Ignore it :)
            if(file == Globals.this_file_name):
                continue;

            for ext in Globals.extensions:
                #Get the filename and its extension.
                filename, fileext = os.path.splitext(file);
                #Extension matches.
                if(fileext == ext):
                    #Parse the file to get all tags.
                    parse(os.path.join(root, file));

def parse(filename):
    tag_entry = TagEntry(filename);    
    
    #Open the file and get the lines.
    lines = open(filename).readlines();
    #For all lines.
    for line_no in xrange(0, len(lines)):
        line = lines[line_no];
        
        #Check if any tag was found.
        for tag_name in Globals.tag_names:
            search_str = ".*%s.*" %(tag_name); #Build a regex
            if(re.search(search_str, line) is not None):
                clean_line = Helper.clean_str(line, tag_name);
                tag_entry.add(tag_name, line_no, clean_line);
                break;

    for tag_name in tag_entry.data.keys():
        Globals.tag_entries[tag_name].append(tag_entry);

################################################################################
## Output Functions                                                           ##
################################################################################
def output_log():
    for tag_name in Globals.tag_names:
        tag_list     = Globals.tag_entries[tag_name];        
        tag_list_len = len(tag_list);
        if(tag_list_len == 0):
            continue;

        print "{} - Files({})".format(Helper.colored(tag_name, "red"), 
                                      Helper.colored(tag_list_len, "cyan"));

        for entry in tag_list:
            entry_data     = entry.data[tag_name];
            entry_data_len = len(entry_data);

            print "{} - Issues({}):".format(Helper.colored(entry.filename, "yellow"),
                                             Helper.colored(entry_data_len, "cyan"));

            for entry_info in entry_data:
                print "\t ({}) {}".format(Helper.colored(entry_info[0], "cyan"),
                                          Helper.colored(entry_info[1], "green"));

def output_short():
    pass;

################################################################################
## Script Initialization                                                      ##
################################################################################
def main():
    scan(".");
    output_log();

if(__name__ == "__main__"):
    main();
