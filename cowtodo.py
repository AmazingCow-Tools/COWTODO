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
    APP_VERSION   = "0.1.3";
    APP_AUTHOR    = "N2OMatt <n2omatt@amazingcow.com>"
    APP_COPYRIGHT = "\n".join(("Copyright (c) 2015 - Amazing Cow",
                               "This is a free software (GPLv3) - Share/Hack it",
                               "Check opensource.amazingcow.com for more :)"));

    #FLags
    FLAG_HELP               = "h", "help";
    FLAG_VERSION            = "v", "version";
    FLAG_SHORT              = "s", "short";
    FLAG_LONG               = "l", "long";
    FLAG_VERBOSE            = "V", "verbose";
    FLAG_EXCLUDE            = "e", "exclude";
    FLAG_ADD_EXCLUDE_DIR    = "add-exclude-dir";
    FLAG_REMOVE_EXCLUDE_DIR = "remove-exclude-dir";
    FLAG_LIST_EXCLUDE_DIR   = "list-exclude-dir";

    FLAGS_SHORT = "hvslVe:";
    FLAGS_LONG  = ["help",
                   "version",
                   "short",
                   "long",
                   "verbose",
                   "exclude=",
                   "add-exclude-dir=",
                   "remove-exclude-dir=",
                   "list-exclude-dir",
                   ];

    #Exclude Dir RC Paths.
    RC_DIR_PATH  = os.path.expanduser("~/.cowtodorc");
    RC_FILE_PATH = os.path.join(RC_DIR_PATH,"cowtodorc.txt");


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
    verbose                       = False;
    exclude_dirs                  = [];
    paths_to_add_in_exclude_rc    = [];
    paths_to_remove_in_exclude_rc = [];

################################################################################
## Helper                                                                     ##
################################################################################
class Helper:
    @staticmethod
    def print_help():
        msg = "Usage:" +"""
  cowtodo [-hv] [-sl] [-e <path>] <search_path>
  cowtodo [--list-exclude-dir]
  cowtodo [--add-exclude-dir|remove-exclude-dir] <path>

Options:
 *-h --help           : Show this screen.
 *-v --version        : Show app version and copyright.
  -s --short          : Output the short listing.
  -l --long           : Output the long listing. (Default)
  -V --verbose        : Verbose mode, helps to see what it's doing.
  -e --exclude <path> : Exclude the path from scan.

 *--list-exclude-dir          : List all exclude path in ({rcpath}).
  --add-exclude-dir    <path> : Add exclude path to ({rcpath}).
  --remove-exclude-dir <path> : Remove exclude path from ({rcpath}).

Notes:
  If <search_path> is blank the current dir is assumed.
  Multiple --exclude <path> can be used.
  Multiple --add-exclude-dir <path> can be used.
  Multiple --remove-exclude-dir <path> can be used.

  Options marked with * are exclusive, i.e. the cowtodo will run that
  and exit successfully after the operation.
  """;
        msg = msg.format(rcpath=Constants.RC_FILE_PATH);
        print msg;

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
    def print_error(*args):
        print Helper.colored("[ERROR]", "red"),
        print " ".join(map(str, args));

    @staticmethod
    def print_fatal(*args):
        print Helper.colored("[FATAL]", "red"),
        print " ".join(map(str, args));
        exit(1);

    @staticmethod
    def clean_str(s, tag):
        s = s.replace(tag, "");
        s = s.rstrip(" ").lstrip(" ");
        s = s.lstrip("#").lstrip("/");
        s = s.lstrip(":").lstrip(" ");
        s = s.rstrip("\n");
        return s;

    @staticmethod
    def expand_normalize_path(path):
        if(len(path) == 0):
            Helper.print_fatal("Invalid empty path.");

        path = os.path.expanduser(path);
        path = os.path.abspath(path);
        path = os.path.normpath(path);
        return path;

################################################################################
## Exclude Dirs RC                                                            ##
################################################################################
class ExcludeDirRC:
    def __init__(self):
        self.check_dir_and_file();

    def get_excluded_dirs(self):
        lines = open(Constants.RC_FILE_PATH).readlines();
        return map(lambda x: x.replace("\n", ""), lines);

    def check_dir_and_file(self):
        #Check if the rc folder exists.
        if(not os.path.isdir(Constants.RC_DIR_PATH)):
            msg = "Missing folder at: {} - creating one now";
            Helper.print_error(msg.format(Constants.RC_DIR_PATH));
            try:
                os.mkdir(Constants.RC_DIR_PATH);
            except Exception, e:
                Helper.print_fatal(e);

        #Check if the database exists.
        if(not os.path.isfile(Constants.RC_FILE_PATH)):
            msg = "Missing database file at {} - your dirs are gone - creating one now.";
            Helper.print_error(msg.format(Constants.RC_FILE_PATH));

            cmd = "touch {}".format(Constants.RC_FILE_PATH);
            ret = os.system(cmd);
            if(ret != 0):
                Helper.print_fatal("cmd:({}) failed.".format(cmd));

        self.verify_paths();

    def verify_paths(self):
        #Get all paths and check if them refer to a directory.
        invalid_paths = [];
        for path in self.get_excluded_dirs():
            if(os.path.isdir(path) == False):
                invalid_paths.append(path);

        #If any of them is invalid, show a faltal error log.
        if(len(invalid_paths) != 0):
            rc_path = Helper.colored(Constants.RC_FILE_PATH, "magenta");
            msg = "Invalid Paths in ({}):\n  ".format(rc_path);
            msg += Helper.colored("\n  ".join(invalid_paths), "red");
            msg += "\nFix it to so cowtodo can run."
            Helper.print_fatal(msg);

    def print_list(self):
        self.check_dir_and_file();
        print "Excluded dirs - (Will be ignored in all cowtodo calls):";

        lines = open(Constants.RC_FILE_PATH).readlines();
        if(len(lines) == 0):
            print "Empty...";
            return;

        for line in lines:
            print " ", Helper.colored(line, "blue").replace("\n", "");

    def add_path(self, path):
        msg = "Adding path in exclude dirs rc:({})".format(Helper.colored(path, "blue"));
        Helper.print_verbose(msg);

        #Check if path is valid.
        if(not os.path.isdir(path)):
            Helper.print_fatal("Invalid path:({})".format(Helper.colored(path, "red")));

        #Check if we already have this path included.
        #If included log and return.
        grep_cmd = "grep -q \"{}\" \"{}\"".format(path, Constants.RC_FILE_PATH);
        ret = os.system(grep_cmd);
        if(ret == 0):
            msg = "{}{}{}".format("  Path(",
                                  Helper.colored(path, "blue"),
                                  ") is already added...");
            Helper.print_verbose(msg);
            return;

        #Path is not included add it.
        echo_cmd = "echo \"{}\" >> \"{}\"".format(path, Constants.RC_FILE_PATH);
        os.system(echo_cmd);

    def remove_path(self, path):
        msg = "Removing path in exclude dirs rc:({})".format(Helper.colored(path, "blue"));
        Helper.print_verbose(msg);

        #Check if we already have this path included.
        #If not included log and fail.
        grep_cmd = "grep -q \"{}\" \"{}\"".format(path, Constants.RC_FILE_PATH);

        ret = os.system(grep_cmd);
        if(ret != 0):
            msg = "{}{}{}".format("Path(",
                                  Helper.colored(path, "red"),
                                  ")is not added...");
            Helper.print_fatal(msg);

        #Path included, so grep the inverse to a temp file
        #move the temp over the original one.
        cmd = "grep -v \"{search}\" \"{original}\" > \"{temp}.temp\"";
        grep_inv_cmd = cmd.format(search=path,
                                  original=Constants.RC_FILE_PATH,
                                  temp=Constants.RC_FILE_PATH);
        os.system(grep_inv_cmd);
        #Now move the temp over the original
        mv_cmd = "mv {temp}.temp {original}".format(temp=Constants.RC_FILE_PATH,
                                                    original=Constants.RC_FILE_PATH);
        os.system(mv_cmd);


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
    #COWTODO: Put this in a try/except.
    #Get the command line options.
    options = getopt.gnu_getopt(sys.argv[1:],
                                Constants.FLAGS_SHORT,
                                Constants.FLAGS_LONG);

    #Optiongs switches.
    help_resquested              = False;
    version_requested            = False;
    long_requested               = False;
    short_requested              = False;
    verbose_requested            = False;
    list_exclude_paths_requested = False;

    #Parse the options.
    for option in options[0]:
        key, value = option;
        key = key.lstrip("-");

        #Check if flags are present.
        #Help.
        if(key in Constants.FLAG_HELP):
            help_resquested = True;
        #Version.
        elif(key in Constants.FLAG_VERSION):
            version_requested = True;
        #Long output.
        elif(key in Constants.FLAG_LONG):
            long_requested = True;
        #Short output.
        elif(key in Constants.FLAG_SHORT):
            short_requested = True;
        #Verbose.
        elif(key in Constants.FLAG_VERBOSE):
            verbose_requested = True;
        #Exclude dir.
        elif(key in Constants.FLAG_EXCLUDE):
            #COWTODO: If not a valid path exit.
            path = Helper.expand_normalize_path(value);
            if(os.path.isdir(path)):
                Globals.exclude_dirs.append(path);
        #List exclude dirs in rc.
        elif(key in Constants.FLAG_LIST_EXCLUDE_DIR):
            list_exclude_paths_requested = True;
        #Add the dir to exclude rc.
        elif(key in Constants.FLAG_ADD_EXCLUDE_DIR):
            #Error checking about paths will be done when adding the paths.
            path = Helper.expand_normalize_path(value);
            Globals.paths_to_add_in_exclude_rc.append(path);
        #Remove the dir in exclude rc.
        elif(key in Constants.FLAG_REMOVE_EXCLUDE_DIR):
            #Error checking about paths will be done when removing the paths.
            path = Helper.expand_normalize_path(value);
            Globals.paths_to_remove_in_exclude_rc.append(path);

    #Check if the exclusive operations are requested.
    if(help_resquested):
        Helper.print_help();
        exit(0);
    if(version_requested):
        Helper.print_version();
        exit(0);
    if(list_exclude_paths_requested):
        ExcludeDirRC().print_list();
        exit(0);

    #Set the verbose flag.
    Globals.verbose = verbose_requested;

    #Add/Remove all paths to/from rc before start the run.
    rc = ExcludeDirRC();
    for path in Globals.paths_to_add_in_exclude_rc:
        rc.add_path(path);
    for path in Globals.paths_to_remove_in_exclude_rc:
        rc.remove_path(path);

    #Add all the Excluded paths in rc to the list of excluded paths.
    Globals.exclude_dirs += rc.get_excluded_dirs();

    #Set the output function based upon the flag.
    output_f = output_long;
    if(short_requested): output_f = output_short;
    if(long_requested):  output_f = output_long;

    #Check if the path is present.
    path = ".";
    if(len(options[1]) > 0):
        path = options[1][0];

    # Do a scan and present the results.
    scan(path);
    Helper.print_verbose("\n\n");
    output_f();

if(__name__ == "__main__"):
    main();
