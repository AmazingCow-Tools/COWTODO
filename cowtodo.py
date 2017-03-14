#!/usr/bin/python
#coding=utf8
##----------------------------------------------------------------------------##
##               █      █                                                     ##
##               ████████                                                     ##
##             ██        ██                                                   ##
##            ███  █  █  ███        cowtodo.py                                ##
##            █ █        █ █        COWTODO                                   ##
##             ████████████                                                   ##
##           █              █       Copyright (c) 2015, 2016                  ##
##          █     █    █     █      AmazingCow - www.AmazingCow.com           ##
##          █     █    █     █                                                ##
##           █              █       N2OMatt - n2omatt@amazingcow.com          ##
##             ████████████         www.amazingcow.com/n2omatt                ##
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
##        The email is: acknowledgment_opensource@AmazingCow.com              ##
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

#COWTODO: #01 - Check if the output is a terminal, if not does not put color.
#COWTODO: #02 - Add an option to specify more tags if needed.
#COWTODO: #03 - Better error checking.
#COWTODO: #04 - Refactor the issues output methods.
#COWTODO: #05 - Output to a sql statements, xml, json etc.
#COWTODO: #06 - Make a setup file.
#COWTODO: #09 - Normalize the output messages (Color and style)
#COWTODO: #10 - Change the termcolor to cowtermcolor.

## Imports ##
import getopt;
import os
import os.path;
import pdb;
import re;
import sys;
import time;


################################################################################
## Don't let the standard import error to users - Instead show a              ##
## 'nice' error screen describing the error and how to fix it.                ##
################################################################################
def __import_error_message_print(pkg_name, pkg_url):
    print "Sorry, "
    print "cowtodo depends on {} package.".format(pkg_name);
    print "Visit {} to get it.".format(pkg_url);
    print "Or checkout the README.md to learn other ways to install {}.".format(pkg_name);
    Helper.exit(1);


## cowtermcolor ##
try:
    from cowtermcolor import *;
except ImportError, e:
    __import_error_message_print(
        "cowtermcolor",
        "http//opensource.amazingcow.com/cowtermcolor.html");


################################################################################
## Color                                                                      ##
################################################################################
ColorPath               = Color(MAGENTA);
ColorError              = Color(RED);
ColorInfo               = Color(BLUE);
ColorProcess            = Color(YELLOW);
ColorFile               = Color(CYAN);
ColorIssue              = Color(GREEN);
ColorNumber             = Color(BLUE);
ColorTag                = Color(RED);


################################################################################
## Constants                                                                  ##
################################################################################
class Constants:
    #App
    APP_NAME      = "cowtodo";
    APP_VERSION   = "0.4.0";
    APP_AUTHOR    = "N2OMatt <n2omatt@amazingcow.com>"
    APP_COPYRIGHT = "\n".join(("Copyright (c) 2015, 2016 - Amazing Cow",
                               "This is a free software (GPLv3) - Share/Hack it",
                               "Check opensource.amazingcow.com for more :)"));

    #FLags
    FLAG_HELP               = "h", "help";
    FLAG_VERSION            = "v", "version";
    FLAG_SHORT              = "s", "short";
    FLAG_LONG               = "l", "long";
    FLAG_VERBOSE            = "V", "verbose";
    FLAG_NO_COLORS          =  "", "no-colors";
    FLAG_EXCLUDE            = "e", "exclude";
    FLAG_EXCLUDE_EXT        = "E", "exclude-ext";
    FLAG_ADD_EXCLUDE_DIR    =  "", "add-exclude-dir";
    FLAG_REMOVE_EXCLUDE_DIR =  "", "remove-exclude-dir";
    FLAG_LIST_EXCLUDE_DIR   =  "", "list-exclude-dir";
    FLAG_TAG                = "t", "tag";

    FLAGS_SHORT = "".join([
        FLAG_HELP              [0]      ,
        FLAG_VERSION           [0]      ,
        FLAG_SHORT             [0]      ,
        FLAG_LONG              [0]      ,
        FLAG_VERBOSE           [0]      ,
        FLAG_NO_COLORS         [0]      ,
        FLAG_EXCLUDE           [0] + ":",
        FLAG_EXCLUDE_EXT       [0] + ":",
        FLAG_ADD_EXCLUDE_DIR   [0]      ,
        FLAG_REMOVE_EXCLUDE_DIR[0]      ,
        FLAG_LIST_EXCLUDE_DIR  [0]      ,
        FLAG_TAG               [0] + ":"
    ]);

    FLAGS_LONG = [
        FLAG_HELP              [1]      ,
        FLAG_VERSION           [1]      ,
        FLAG_SHORT             [1]      ,
        FLAG_LONG              [1]      ,
        FLAG_VERBOSE           [1]      ,
        FLAG_NO_COLORS         [1]      ,
        FLAG_EXCLUDE           [1] + "=",
        FLAG_EXCLUDE_EXT       [1] + "=",
        FLAG_ADD_EXCLUDE_DIR   [1] + "=",
        FLAG_REMOVE_EXCLUDE_DIR[1] + "=",
        FLAG_LIST_EXCLUDE_DIR  [1]      ,
        FLAG_TAG               [1] + "="
    ];


    #Exclude Dir RC Paths.
    RC_DIR_PATH  = os.path.expanduser("~/.cowtodorc");
    RC_FILE_PATH = os.path.join(RC_DIR_PATH,"cowtodorc.txt");


################################################################################
## Globals                                                                    ##
################################################################################
class Globals:
    extensions = [ ".h"   , ".c",   #C
                   ".cpp" , ".cc",  #C++
                   ".cs",           #C#
                   ".html", ".htm", #HTML
                   ".js"  , ".jsx", #Javascript
                   ".md",           #Markdown
                   ".m"   , ".mm",  #ObjC
                   ".php" ,         #PHP
                   ".py"  ,         #Python
                   ".sh"            #Shell Script.
                ];

    tag_names = [ "COWTODO",
                  "COWFIX",
                  "COWHACK",
                  "COWNOTE", ];

    this_file_name = "cowtodo.py";

    tag_entries    = {
        "COWTODO" : [],
        "COWHACK" : [],
        "COWFIX"  : [],
        "COWNOTE" : [],
    };

    verbose                       = False;
    exclude_dirs                  = [];
    paths_to_add_in_exclude_rc    = [];
    paths_to_remove_in_exclude_rc = [];

    tags_to_search  = [];
    tags_to_exclude = [];


################################################################################
## Helper                                                                     ##
################################################################################
class Helper:
    @staticmethod
    def print_help(exit_code = -1):
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
     --no-colors      : Make the output uncolored.
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

        if(exit_code != -1):
            Helper.exit(exit_code);

    @staticmethod
    def print_version(exit_code = -1):
        print "{} - {} - {}".format(Constants.APP_NAME,
                                    Constants.APP_VERSION,
                                    Constants.APP_AUTHOR);
        print Constants.APP_COPYRIGHT;
        print;

        if(exit_code != -1):
            Helper.exit(exit_code);

    @staticmethod
    def print_output(*args):
        print "".join(map(str,args)),

    @staticmethod
    def print_verbose(*args):
        if(Globals.verbose):
            print " ".join(map(str,args));

    @staticmethod
    def print_error(*args):
        print ColorError("[ERROR]"),
        print " ".join(map(str, args));

    @staticmethod
    def print_fatal(*args):
        print ColorError("[FATAL]"),
        print " ".join(map(str, args));
        Helper.exit(1);

    @staticmethod
    def expand_normalize_path(path):
        if(len(path) == 0):
            Helper.print_fatal("Invalid empty path.");

        path = os.path.expanduser(path);
        path = os.path.abspath(path);
        path = os.path.normpath(path);
        return path;

    @staticmethod
    def clean_str(s, tag):
        s = s.replace("\n", "");

        #Check if the comment end with a backslash.
        has_end_backslash = False;
        s2 = s.strip("\\");
        if(s2 != s):
            has_end_backslash = True;
            s = s2;

        #Remove comments.
        s = s.strip(" # " );  # PYTHON comments
        s = s.strip(" /*/ "); # C comments
        s = s.strip(" / ");   # C++ comments
        s = s.lstrip(" <!-- ").rstrip(" -->");

        #Remove the spacing.
        s = s.strip(" ");

        #Remove the current tag.
        s = s.replace(tag, "");
        s = s.strip(" : ");

        #If ends with backslash add a new line.
        if(has_end_backslash):
            s += "\n";

        #Clean up lines that are empty...
        if(s == "\n"):
            s = "";

        return s;

    @staticmethod
    def exit(code):
        exit(code);


################################################################################
## Exclude Dirs RC                                                            ##
################################################################################
class ExcludeDirRC:
    @staticmethod
    def get_excluded_dirs():
        ExcludeDirRC.check_dir_and_file();

        lines = open(Constants.RC_FILE_PATH).readlines();
        return map(lambda x: x.replace("\n", ""), lines);

    @staticmethod
    def check_dir_and_file():
        #Check if the rc folder exists.
        if(not os.path.isdir(Constants.RC_DIR_PATH)):
            msg = "Missing folder at: ({})\n  Creating one now.";
            msg = msg.format(ColorPath(Constants.RC_DIR_PATH));
            Helper.print_error(msg);

            try:
                os.mkdir(Constants.RC_DIR_PATH);
            except Exception, e:
                Helper.print_fatal(e);

        #Check if the database exists.
        if(not os.path.isfile(Constants.RC_FILE_PATH)):
            msg = "Missing database file at ({})\n  Your dirs are gone - Creating one now.";
            msg = msg.format(ColorPath(Constants.RC_FILE_PATH));
            Helper.print_error(msg);

            cmd = "touch {}".format(Constants.RC_FILE_PATH);
            ret = os.system(cmd);
            if(ret != 0):
                Helper.print_fatal("cmd: ({}) failed.".format(ColorInfo(cmd)));

    @staticmethod
    def verify_paths():
        ExcludeDirRC.check_dir_and_file();

        #Get all paths and check if them refer to a directory.
        invalid_paths = [];
        line = 1;
        for path in ExcludeDirRC.get_excluded_dirs():
            fullpath = Helper.expand_normalize_path(path);
            if(os.path.isdir(fullpath) == False):
                invalid_paths.append({"line" : line, "path" : path});
            line += 1;

        #If any of them is invalid, show a fatal error log.
        if(len(invalid_paths) != 0):
            rc_path = ColorPath(Constants.RC_FILE_PATH);

            msg  = "Invalid Paths in ({}):\n".format(rc_path);

            for d in invalid_paths:
                msg += "  {} - line:({})\n".format(ColorError(d["path"]),
                                                   ColorInfo(d["line"]));

            msg += "\nFix it... then cowtodo can run."
            Helper.print_fatal(msg);

    @staticmethod
    def print_list():
        ExcludeDirRC.check_dir_and_file();

        print "Excluded dirs - (Will be ignored in all cowtodo calls):";

        lines = ExcludeDirRC.get_excluded_dirs();
        if(len(lines) == 0):
            print "Empty...";
            return;

        for line in lines:
            print " ", ColorPath(line.replace("\n", ""));

    @staticmethod
    def add_path(path):
        ExcludeDirRC.check_dir_and_file();

        msg = "Adding path in exclude dirs rc: ({})".format(ColorPath(path));
        Helper.print_verbose(msg);

        fullpath = Helper.expand_normalize_path(path);

        #Check if path is valid.
        if(not os.path.isdir(fullpath)):
            Helper.print_fatal("Invalid path:({})".format(ColorPath(path)));

        #Check if we already have this path included.
        #If included log and return.
        grep_cmd = "grep -q \"{}\" \"{}\"".format(fullpath, Constants.RC_FILE_PATH);
        ret = os.system(grep_cmd);
        if(ret == 0):
            msg = "Path ({}) is already added...".format(ColorPath(path));
            Helper.print_verbose(msg);
            return;

        #Path is not included add it.
        echo_cmd = "echo \"{}\" >> \"{}\"".format(fullpath, Constants.RC_FILE_PATH);
        os.system(echo_cmd);

    @staticmethod
    def remove_path(path):
        ExcludeDirRC.check_dir_and_file();

        msg = "Removing path in exclude dirs rc: ({})".format(ColorPath(path));
        Helper.print_verbose(msg);

        fullpath = Helper.expand_normalize_path(path);

        #Check if we already have this path included.
        #If not included log and fail.
        grep_cmd = "grep -q \"{}\" \"{}\"".format(fullpath, Constants.RC_FILE_PATH);

        ret = os.system(grep_cmd);
        if(ret != 0):
            msg = "Path ({}) is not added...".format(ColorPath(path));
            Helper.print_fatal(msg);


        #Path included, so grep the inverse to a temp file
        #move the temp over the original one.
        cmd = "grep -v \"{search}\" \"{original}\" > \"{temp}.temp\"";
        grep_inv_cmd = cmd.format(search   = fullpath,
                                  original = Constants.RC_FILE_PATH,
                                  temp     = Constants.RC_FILE_PATH);
        os.system(grep_inv_cmd);

        #Now move the temp over the original
        mv_cmd = "mv {temp}.temp {original}".format(temp     = Constants.RC_FILE_PATH,
                                                    original = Constants.RC_FILE_PATH);
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
    #Check if start path is valid.
    start_path = Helper.expand_normalize_path(start_path);
    if(not os.path.isdir(start_path)):
        Helper.print_fatal("{} ({})".format(
            "start path is not valid directory - ",
            ColorPath(start_path)));

    ## Scan the directories.
    for root, dirs, files in os.walk(start_path, topdown=True):

        #Check if current root path is in our exclude list of if it is hidden.
        is_in_exclude_list = Helper.expand_normalize_path(root) in Globals.exclude_dirs;
        is_hidden          = os.path.split(root)[1][0] == "." and len(root) != 1;

        if(is_in_exclude_list or is_hidden):
            #Log if verbose.
            Helper.print_verbose("{} ({})".format(ColorInfo("Ignoring:"),
                                                  ColorPath(root)));

            #Remove the os.walk dirs.
            dirs[:] = [];

            #Remove the path from the exclude paths since we're already hit it.
            #So it will be perform better because we gonna search a lot of dirs
            #without test a path that makes no sense anymore.
            if(is_in_exclude_list):
                Globals.exclude_dirs.remove(os.path.abspath(root));

            continue; #Skip the rest of for block.


        Helper.print_verbose("{} ({})".format(ColorProcess("Scanning:"),
                                              ColorPath(root)));

        #For each file check if it matches with our file extensions.
        for file in files:
            #We found this file. Ignore it :)
            if(file == Globals.this_file_name):
                continue;

            #Get the filename and its extension.
            filename, fileext = os.path.splitext(file);

            #Check if the fileext is in our extensions list.
            for ext in Globals.extensions:
                if(fileext == ext):
                    Helper.print_verbose("  {} ({})".format(ColorProcess("Parsing"),
                                                            ColorFile(file)));
                    #Parse the file to get all tags.
                    parse(os.path.join(root, file));


def parse(filename):
    tag_entry = TagEntry(filename);

    #Open the file and get the lines.
    lines = open(filename).readlines();

    #For all lines.
    for line_no in xrange(0, len(lines)):
        line = lines[line_no];

        #Iterate for all of our tags in this line.
        for tag_name in Globals.tag_names:

            #This current Tag in in the exclude list.
            #   We don't need keep any track of it.
            if(tag_name in Globals.tags_to_exclude):
                continue;

            #If user didn't set any tags to search, means that he wants to
            #search every tag, so we don't do nothing in this case.
            #But if it set any tag, means that ONLY that tag should be tracked.
            if(len(Globals.tags_to_search) != 0 and tag_name not in Globals.tags_to_search):
                continue;

            search_str = ".*%s.*" %(tag_name); #Build a regex.

            #Check if any tag was found.
            if(re.search(search_str, line) is not None):
                clean_line = ""; #Start with a blank line.

                #Keep consuming the lines while them
                #end with the \ (backslash) char.
                #Or the end of file is reached.
                while(True):
                    clean_line += Helper.clean_str(line, tag_name);
                    #End of file OR
                    #empty (Just a new line) OR
                    ## line not ending with \ backslash
                    if(line_no >= len(lines) or len(line) < 2 or line[-2] != "\\"):
                        break;

                    line_no += 1;
                    line = lines[line_no];

                #Ops... This comment is empty, but we cannot discard it because
                #it's author may put it like a mark on code.
                if(len(clean_line) == 0):
                    clean_line += "__EMPTY [{}] COMMENT__".format(tag_name);

                tag_entry.add(tag_name, line_no, clean_line);

                #We just take in account on type of tag for each time.
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
        out = out.format(ColorTag(tag_name), ColorNumber(tag_entry_list_len));
        print out;

        #For each entry for this tag.
        for entry in tag_entry_list:
            entry_data     = entry.data[tag_name];
            entry_data_len = len(entry_data);

            #Print the file name and the count of issues.
            out = "{} - Issues({}):";
            out = out.format(ColorFile(entry.filename),
                             ColorNumber(entry_data_len));
            print out;

            digits_on_greater_entry_no =  len(str(entry_data[-1][0]));
            for entry_info in entry_data:
                entry_file  = entry.filename;
                entry_no    = entry_info[0];
                entry_issue = entry_info[1];

                spacing_chars = " " * 8;

                #Left padding the entry number with zeros.
                number_of_zeros = (digits_on_greater_entry_no - len(str(entry_no)));
                entry_no = ("0" * number_of_zeros) + str(entry_no);

                #Padding them entry issue to make it aligned.
                padding = " " * (len(entry_no) + 3);
                entry_issue = entry_issue.replace("\n", "\n" + spacing_chars + padding)

                #Put colors.
                colored_entry_no    = ColorNumber(entry_no);
                colored_entry_issue = ColorIssue(entry_issue);

                out = "{}({}) {}";
                out = out.format(spacing_chars,
                                 colored_entry_no,
                                 colored_entry_issue);

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
        out = out.format(ColorTag(tag_name), ColorNumber(tag_entry_list_len));
        print out;

        #For each entry for this tag.
        for entry in tag_entry_list:
            entry_data     = entry.data[tag_name];
            entry_data_len = len(entry_data);

            digits_on_greater_entry_no =  len(str(entry_data[-1][0]));
            for entry_info in entry_data:
                entry_file  = entry.filename;
                entry_no    = entry_info[0];
                entry_issue = entry_info[1];

                #Left padding the entry number with zeros.
                number_of_zeros = (digits_on_greater_entry_no - len(str(entry_no)));
                entry_no = ("0" * number_of_zeros) + str(entry_no);

                #Padding the entry issue to make them aligned
                entry_issue_offset = " " * (len(entry_file) + len(entry_no) + 3);
                entry_issue = entry_issue.replace("\n", "\n" + entry_issue_offset);

                #Print the line of issue and its message.
                colored_entry_file  = ColorFile(entry_file);
                colored_entry_no    = ColorNumber(entry_no);
                colored_entry_issue = ColorIssue(entry_issue);

                out = "{}({}) {}";
                out = out.format(colored_entry_file,
                                 colored_entry_no,
                                 colored_entry_issue);
                print out;


################################################################################
## Script Initialization                                                      ##
################################################################################
def main():
    try:
        #Get the command line options.
        options = getopt.gnu_getopt(sys.argv[1:],
                                    Constants.FLAGS_SHORT,
                                    Constants.FLAGS_LONG);
    except Exception, e:
        Helper.print_fatal(e);

    #Options switches.
    long_requested      = False;
    short_requested     = False;

    #Parse the options.
    for option in options[0]:
        key, value = option;
        key = key.lstrip("-");

        #Help / Version / List exclude dirs - Exclusives.
        if(key in Constants.FLAG_HELP):
            Helper.print_help(0);
        elif(key in Constants.FLAG_VERSION):
            Helper.print_version(0);
        elif(key in Constants.FLAG_LIST_EXCLUDE_DIR):
            ExcludeDirRC.print_list();
            exit(0);

        #Long / Short output - Optionals.
        elif(key in Constants.FLAG_LONG  ): long_requested = True;
        elif(key in Constants.FLAG_SHORT ): short_requested = True;

        #Verbose / No Colors - Optionals.
        elif(key in Constants.FLAG_VERBOSE):
            Globals.verbose = True;
        elif(key in Constants.FLAG_NO_COLORS):
            ColorMode.mode = ColorMode.NEVER;

        #Exclude dir - Optional
        elif(key in Constants.FLAG_EXCLUDE):
            path = Helper.expand_normalize_path(value);
            if(not os.path.isdir(path)):
                msg = "Path to exclude is invalid ({})";
                Helper.print_fatal(msg.format(ColorPath(path)));
            Globals.exclude_dirs.append(path);

        #Exclude ext - Optional
        elif(key in Constants.FLAG_EXCLUDE_EXT):
            if(value[0] != "."):
                value = "." + value;
            if(Globals.extensions.count(value) == 0):
                msg = "Extension not recognized: ({})".format(ColorInfo(value));
                Helper.print_fatal(msg);
            Globals.extensions.remove(value);

        #Add / Remove the dir to exclude rc - Optionals
        #Error checking about paths will be done when adding the paths.
        elif(key in Constants.FLAG_ADD_EXCLUDE_DIR):
            Globals.paths_to_add_in_exclude_rc.append(value);
        elif(key in Constants.FLAG_REMOVE_EXCLUDE_DIR):
            Globals.paths_to_remove_in_exclude_rc.append(value);

        #Tag - Optional
        elif(key in Constants.FLAG_TAG):
            if(value[0] == "~"):
                Globals.tags_to_exclude.append(value[1:]);
            else:
                Globals.tags_to_search.append(value);


    #Add/Remove all paths to/from rc before start the run.
    for path in Globals.paths_to_add_in_exclude_rc:
        ExcludeDirRC.add_path(path);
    for path in Globals.paths_to_remove_in_exclude_rc:
        ExcludeDirRC.remove_path(path);

    #Add all the Excluded paths in rc to the list of excluded paths.
    Globals.exclude_dirs += ExcludeDirRC.get_excluded_dirs();

    #Set the output function based upon the flag.
    output_func = output_long;
    if(short_requested ): output_func = output_short;
    if(long_requested  ): output_func = output_long;

    #Check if the path is present.
    path = ".";
    if(len(options[1]) > 0):
        path = options[1][0];

    #Do a scan and present the results.
    scan(path);
    Helper.print_verbose("\n\n");
    output_func();

if(__name__ == "__main__"):
    main();

