COWTODO
====
Made with <3 by [Amazing Cow](http://www.amazingcow.com).

## Intro:
Search specific tags in our source code and print in a formated way.

## Install:
```$ sudo cp -f path/to/cowtodo.py /usr/local/bin/cowtodo```

or use the makefile

```$ make install```

## Usage:
```
cowtodo [-hv] [-sl] [-e <path>] <search_path>
cowtodo [--list-exclude-dir]
cowtodo [--add-exclude-dir|remove-exclude-dir] <path>

Options:
 *-h --help           : Show this screen.
 *-v --version        : Show app version and copyright.
  -s --short          : Output the short listing.
  -l --long           : Output the long listing. (Default)
  -v --verbose        : Verbose mode, helps to see what it's doing.
     --no-colors      : Make the output uncolored.
  -e --exclude <path> : Exclude the path from scan.

 *--list-exclude-dir          : List all exclude path in (rcpath).
  --add-exclude-dir    <path> : Add exclude path to (rcpath).
  --remove-exclude-dir <path> : Remove exclude path from (rcpath).
```

#####Notes:
  If ```<search_path>``` is blank the current dir is assumed.
  Multiple ```--exclude <path>``` can be used.
  Multiple ```--add-exclude-dir <path>``` can be used.
  Multiple ```--remove-exclude-dir <path>``` can be used.

  Options marked with * are exclusive, i.e. the ```cowtodo``` will run that
  and exit successfully after the operation.

## License:
This software is released under GPLv3.

## TODO:
Check the TODO file.

## Others:
Check our repos and take a look at our [open source site](http://opensource.amazingcow.com).
