## Description
A Sublime Text 2/3 plugin to enable the syncing of local files to another location (remote or local).

Tested and verified working on Windows and Ubuntu, realistically it should work on most any OS, there is nothing really system-specific about this plugin.  

**Requires scp and rsync binaries.**

## Installation
The recommended method is by using Sublime Package Manager [See Here](http://wbond.net/sublime_packages/package_control/installation). Otherwise, you can clone the repository yourself. 

* cd into your Sublime packages directory.
* run: git clone https://wiggitywiener@bitbucket.org/wiggitywiener/devsync.git


## Usage
There is a dev_sync command that will push your current project directory (as specified by the "source" path in the settings file) to the specified destination.  This is only required once per project, after that, the  individual files will transfered be on save. 

## Key Mapping
There is only one command that is called via key-stroke, the dev_sync command.  

Add something like this to your keymap:

```
#!JSON

{ "keys": ["alt+s"], "command": "dev_sync" }
```

## Settings
Work with the included template, it should be fairly self-explanatory (I hope). 


## Things of Note
* You will need password-less SSH enabled to use this plugin (google it)
* paths in the settings file are case-sensitive; be sure to escape window's paths as per the example settings file.
* if you're having problems getting the plugin working, enable the debug setting and watch the sublime console (ctrl+`).  All commands will be printed to the console, you can try running them manually to see what is happening.
* Any fatal errors from ssh/rsync will be displayed in a popup window, read them and act accordingly.
* When syncing a large amount of files to a remote server (with the dev_sync command) it may look like sublime has hung/crashed, it will begin responding again when the sync is complete, be patient as this can take a long time depending on the speed of your connection and the number of items to transfer.
