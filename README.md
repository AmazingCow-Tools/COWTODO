# COWTODO

**Made with <3 by [Amazing Cow](http://www.amazingcow.com).**



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Description:

```cowtodo``` - Search and display tags in source files

```cowtodo``` helps to extract from source code, all the _cow tags_ and 
print them in a very organized way.   
It will scan recursively all directories from the _start path_ that aren't 
in the _exclude paths_ searching for files with recognizable extensions.   

If such file is found ```cowtodo``` will seek for _tags_ on the file collecting
information about the _tag_ like the filename, the description and line number.


### COWTAGS:

Currently ```cowtodo``` is collect the information about the following tags:

* COWTODO
* COWFIX
* COWHACK
* COWNOTE

So a piece of C++ code that contains those tags could be:

```c++
void SomeClass::AmazingMethod(int what)
{
    //COWTODO: We must mark this method as deprecated...
    moreAmazingMethod(what);
}
```

The comments containing _cow tags_ can be multi line if them ends with the ```\```
(backslash) char.    
For example:

```python
def some_function():
    #COWNOTE: We're deliberated ignoring that some stuff can happen \
    #         while this is ok for this, and that situation         \
    #         this function could be much more robust by treating   \
    #         this and that according with the original intent      \

    #Some python code...
    return;
```

### Extension Supported:

```cowtodo``` try hard to understand the myriad of types of comments in various
languages that it supports. 

* C            - ```   .h```, ```  .c``` 
* C++          - ``` .cpp```, ``` .cc``` 
* HTML         - ```.html```, ```.htm``` 
* Javascript   - ```  .js```, ```.jsx``` 
* Markdown     - ```  .md```             
* ObjC         - ```   .m```, ``` .mm``` 
* PHP          - ``` .php```             
* Python       - ```  .py```             
* Shell Script - ```  .sh```             


<br>

As usual, you are **very welcomed** to **share** and **hack** it.


<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Usage:

``` 
Usage:
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

 *--list-exclude-dir          : List all exclude path in (RC_PATH).
  --add-exclude-dir    <path> : Add exclude path to (RC_PATH).
  --remove-exclude-dir <path> : Remove exclude path from (RC_PATH).

Notes:
  If <search_path> is blank the current dir is assumed.
  Multiple --exclude <path> can be used.
  Multiple --add-exclude-dir <path> can be used.
  Multiple --remove-exclude-dir <path> can be used.

  Options marked with * are exclusive, i.e. the cowtodo will run that
  and exit successfully after the operation.

```



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Install:

Use the Mafefile.

``` bash
    make install
```

Or to uninstall

``` bash
    make uninstall
```



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Dependencies:

This project uses / depends on:

* Amazing Cow's 
[cowtermcolor](http://www.github.com/AmazingCow-Libs/cowtermcolor_py/)
package to coloring the terminal.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Environment and Files: 

### Files:

* ```~/.cowtodorc``` - Directory containing ```cowtodo``` info.
* ```~/.cowgoshrc/cowtodorc.txt``` - ```cowtodo``` exclude path list.

### Environments:

```cowtodo``` do not create any environments vars.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## License:

This software is released under GPLv3.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## TODO:

Check the TODO file for general things.

This projects uses the COWTODO tags.   
So install [cowtodo](https://github.com/AmazingCow-Tools/COWTODO/) and run:

``` bash
$ cd path/for/the/project
$ cowtodo 
```

That's gonna give you all things to do :D.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## BUGS:

We strive to make all our code the most bug-free as possible - But we know 
that few of them can pass without we notice ;).

Please if you find any bug report to [bugs_opensource@amazingcow.com]() 
with the name of this project and/or create an issue here in Github.



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Source Files:

* AUTHORS.txt
* CHANGELOG.txt
* COPYING.txt
* cowtodo.py
* Makefile
* README.md
* TODO.txt



<!-- ####################################################################### -->
<!-- ####################################################################### -->

## Others:
Check our repos and take a look at our [open source site](http://opensource.amazingcow.com).
