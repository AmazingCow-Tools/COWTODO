#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███                                                  ##
##            █ █        █ █        cowtodo.py                                ##
##             ████████████         COWTODO                                   ##
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
import termcolor;
import getopt;
import sys;

################################################################################
## Constants                                                                  ##
################################################################################
class Constants:
    #Color.
    COLOR_FILE                 = "yellow";
    COLOR_ISSUE                = "green";
    COLOR_NUMBER               = "cyan";
    COLOR_TAG                  = "red";
    COLOR_VERBOSE_TITLE        = "blue";
    COLOR_VERBOSE_MSG          = "magenta";
    COLOR_VERBOSE_IGNORE_TITLE = "red";
    COLOR_VERBOSE_IGNORE_MSG   = "yellow";

    #App
    APP_NAME      = "cowtodo";
    APP_VERSION   = "0.1";
    APP_AUTHOR    = "N2OMatt <n2omatt@amazingcow.com>"
    APP_COPYRIGHT = "\n".join(("Copyright (c) 2015 - Amazing Cow",
                               "This is a free software (GPLv3) - Share/Hack it",
                               "Check opensource.amazingcow.com for more :)"));

    #FLags
    FLAG_HELP    = "h", "help";
    FLAG_VERSION = "v", "version";
    FLAG_SHORT   = "s", "short";
    FLAG_LONG    = "l", "long";
    FLAG_VERBOSE = "V", "verbose";
    FLAG_EXCLUDE = "e", "exclude";

    FLAGS_SHORT = "hvslVe:";
    FLAGS_LONG  = ["help", "version", "short", "long", "verbose", "exclude="];

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
    verbose        = False;
    exclude_dirs   = [];

################################################################################
## Helper                                                                     ##
################################################################################
class Helper:
    @staticmethod
    def print_help():
        print "Usage:";
        print "  cowtodo [-hv] [-sl] [-e <path>] <search_path>";
        print;
        print "  -h --help    : Show this screen.";
        print "  -v --version : Show app version and copyright.";
        print "  -s --short   : Output the short listing.";
        print "  -l --long    : Output the long listing. (Default)";
        print "  -v --verbose : Verbose mode, helps to see what it's doing";
        print "  -e --exclude <path> : Exclude the path from scan.";
        print;
        print "  Note: If <search_path> is blank the current dir is assumed.";
        print "        Mutiple --exclude <path> can be added.";
        print;


    @staticmethod
    def print_version():
        print "{} - {} - {}".format(Constants.APP_NAME,
                                    Constants.APP_VERSION,
                                    Constants.APP_AUTHOR);
        print Constants.APP_COPYRIGHT;
        print;

    @staticmethod
    def colored(msg, color):
        return termcolor.colored(msg, color);

    @staticmethod
    def print_output(*args):
        print "".join(map(str,args)),

    @staticmethod
    def print_verbose(*args):
        if(Globals.verbose):
            print " ".join(map(str,args));

    @staticmethod
    def clean_str(s, tag):
        s = s.replace(tag, "");
        s = s.rstrip(" ").lstrip(" ");
        s = s.lstrip("#").lstrip("/");
        s = s.lstrip(":").lstrip(" ");
        s = s.rstrip("\n");
        return s;

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
    for root, dirs, files in os.walk(start_path, topdown=True):

        #Check if current root path is in our exclude list of if it is hidden.
        is_in_exclude_list = os.path.abspath(root) in Globals.exclude_dirs;
        is_hidden          = "." in os.path.split(root)[1] and len(root) != 1;

        if(is_in_exclude_list or is_hidden):
            #Log if verbose.
            Helper.print_verbose(
                Helper.colored("Ignoring:", Constants.COLOR_VERBOSE_IGNORE_TITLE),
                Helper.colored(root, Constants.COLOR_VERBOSE_IGNORE_MSG));

            #Remove the os.walk dirs.
            dirs[:] = [];

            #Remove the path from the exclude paths since we're already hit it.
            #So it will be perform better because we gonna search a lot of dirs
            #without test a path that makes no sense anymore.
            if(is_in_exclude_list):
                Globals.exclude_dirs.remove(os.path.abspath(root));

            continue; #Skip the rest of for block.

        Helper.print_verbose(Helper.colored("Scanning:", Constants.COLOR_VERBOSE_TITLE),
                             Helper.colored(root, Constants.COLOR_VERBOSE_MSG));

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
                    Helper.print_verbose(
                             Helper.colored("\tParsing:", Constants.COLOR_VERBOSE_TITLE),
                             Helper.colored(file, Constants.COLOR_VERBOSE_MSG));

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
def output_long():
    #Output the messages for all tag names.
    for tag_name in Globals.tag_names:
        #Get the list of entries for this tag.
        tag_entry_list     = Globals.tag_entries[tag_name];
        tag_entry_list_len = len(tag_entry_list);
        if(tag_entry_list_len == 0): #Have nothing to show.
            continue;

        #Print the Tag name and count of files with it.
        out = "{} - Files({})";
        out = out.format(Helper.colored(tag_name, Constants.COLOR_TAG),
                         Helper.colored(tag_entry_list_len, Constants.COLOR_NUMBER));
        print out;

        #For each entry for this tag.
        for entry in tag_entry_list:
            entry_data     = entry.data[tag_name];
            entry_data_len = len(entry_data);

            #Print the file name and the count of issues.
            out = "{} - Issues({}):";
            out = out.format(Helper.colored(entry.filename, Constants.COLOR_FILE),
                             Helper.colored(entry_data_len, Constants.COLOR_NUMBER));
            print out;

            for entry_info in entry_data:
                #Print the line of issue and its message.
                out = "\t ({}) {}";
                out = out.format(Helper.colored(entry_info[0], Constants.COLOR_NUMBER),
                                 Helper.colored(entry_info[1], Constants.COLOR_ISSUE));
                print out;

def output_short():
    #Output the messages for all tag names.
    for tag_name in Globals.tag_names:
        #Get the list of entries for this tag.
        tag_entry_list     = Globals.tag_entries[tag_name];
        tag_entry_list_len = len(tag_entry_list);
        if(tag_entry_list_len == 0): #Have nothing to show.
            continue;

        #Print the Tag name and count of files with it.
        out = "{} - Files({})";
        out = out.format(Helper.colored(tag_name, Constants.COLOR_TAG),
                         Helper.colored(tag_entry_list_len, Constants.COLOR_NUMBER));
        print out;

        #For each entry for this tag.
        for entry in tag_entry_list:
            entry_data     = entry.data[tag_name];
            entry_data_len = len(entry_data);

            for entry_info in entry_data:
                #Print the line of issue and its message.
                out = "{} - ({}) {}";
                out = out.format(Helper.colored(entry.filename,Constants.COLOR_FILE),
                                 Helper.colored(entry_info[0], Constants.COLOR_NUMBER),
                                 Helper.colored(entry_info[1], Constants.COLOR_ISSUE));
                print out;


################################################################################
## Script Initialization                                                      ##
################################################################################
def main():
    #Get the command line options.
    options = getopt.gnu_getopt(sys.argv[1:],
                                Constants.FLAGS_SHORT,
                                Constants.FLAGS_LONG);

    #Optiongs switches.
    help_resquested   = False;
    version_requested = False;
    long_requested    = False;
    short_requested   = False;
    verbose_requested = False;

    #Parse the options.
    for option in options[0]:
        key, value = option;
        key = key.lstrip("-");

        #Check if flags are present.
        if  (key in Constants.FLAG_HELP):    help_resquested   = True;
        elif(key in Constants.FLAG_VERSION): version_requested = True;
        elif(key in Constants.FLAG_LONG):    long_requested    = True;
        elif(key in Constants.FLAG_SHORT):   short_requested   = True;
        elif(key in Constants.FLAG_VERBOSE): verbose_requested = True;
        elif(key in Constants.FLAG_EXCLUDE):
            path = os.path.expanduser(value);
            path = os.path.abspath(path);
            if(os.path.isdir(path)):
                Globals.exclude_dirs.append(path);

    #Check if the exclusive operations are requested.
    if(help_resquested):
        Helper.print_help();
        exit(0);
    if(version_requested):
        Helper.print_version();
        exit(0);

    #Set the output function based upon the flag.
    output_f = output_long;
    if(short_requested): output_f = output_short;
    if(long_requested):  output_f = output_long;

    #Check if the path is present.
    path = ".";
    if(len(options[1]) > 0):
        path = options[1][0];

    #Set the verbose flag.
    Globals.verbose = verbose_requested;

    #Do a scan and present the results.
    scan(path);
    Helper.print_verbose("\n\n");
    output_f();

if(__name__ == "__main__"):
    main();
