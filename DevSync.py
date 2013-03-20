import sublime, sublime_plugin, subprocess, re, os

class DevSyncCommand(sublime_plugin.EventListener):
    def on_post_save(self, view):
        settings = sublime.load_settings('DevSync.sublime-settings');
        pathMaps = settings.get('pathMapping');

        # Get the current file path and determine if it is in
        # the user's pathMapping array
        localPath = view.file_name();
        foundMap = None;
        for pathMap in pathMaps:
            if (pathMap["source"] in localPath):
                print('Found sync mapping.');
                foundMap = True;
                # replace the src path with dest path
                destPath = localPath.replace(pathMap["source"], pathMap["destination"]);

                # determine the path (without file name) of the destination
                lastFolderIndex = destPath.rfind("/");
                if (lastFolderIndex == -1):
                    lastFolderIndex = destPath.rfind("\\")
                destFolder = destPath[0:lastFolderIndex];

                osVariant = pathMap["destOS"];
                mkdir = " mkdir ";
                if (osVariant == 'linux'):
                    mkdir = mkdir + "-p ";
                    destPath = destPath.replace('\\', '/');

                if (pathMap["type"] == 'remote'):
                    hostString = pathMap["username"] + "@" + pathMap["serverAddress"];

                    # attempt to create directories in case they do not exist already
                    subprocess.call(settings.get('sshBinary') + " " + hostString + " \"" + mkdir + destFolder + " && exit\"", shell=True);

                    # cygwin executables cannot use windows paths. if the cygwinPath variable is set use that instead
                    if ("cygwinSourcePath" in pathMap and pathMap["cygwinSourcePath"] != "null"):
                        localPath = localPath.replace(pathMap["source"], pathMap["cygwinSourcePath"]);
                        localPath = localPath.replace('\\', '/');

                    # Sync file across
                    command = settings.get('scpBinary') + " -Cr " + localPath + " " + hostString + ":" + destPath;
                    subprocess.call(command, shell=True);
                elif (pathMap["type"] == 'local'):
                    # attempt to create directories in case they do not exist already
                    subprocess.call(mkdir + destFolder, shell=True);

                    # copy the file
                    subprocess.call("cp " + localPath + " " + destPath, shell=True);
        if (foundMap == None):
            print("No source configured for this file.");


class devSyncCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        settings = sublime.load_settings('DevSync.sublime-settings');
        pathMaps = settings.get('pathMapping');

        # Get the current file path and determine if it is in
        # the user's pathMapping array
        localPath = self.view.file_name();
        foundMap = None;
        for pathMap in pathMaps:
            if (pathMap["source"] in localPath):
                source = pathMap["source"]
                print('Found sync mapping.');
                foundMap = True;

                # get the name of the project / the base folder
                index = source.rfind("\\")
                if (index == -1):
                    index = source.rfind("/")

                folderName = source[index:len(source)]
                folderName = folderName.strip("\\")
                folderName = folderName.strip("/")

                # execute the bash script (if necessary)
                if ("bashScript" in pathMap and pathMap["bashScript"] != "null"):
                    command = settings.get('bashBinary') + " \"" + pathMap["bashScript"] + " " + folderName +"\""
                    print(command)
                    subprocess.call(command, shell=True)

                if (pathMap["type"] == 'remote'):
                    hostString = pathMap["username"] + "@" + pathMap["serverAddress"];

                    source = pathMap["source"]

                    # cygwin executables cannot use windows paths. if the cygwinPath variable is set use that instead
                    if ("cygwinSourcePath" in pathMap and pathMap["cygwinSourcePath"] != "null"):
                        source = pathMap["cygwinSourcePath"]

                    command = settings.get('rsyncBinary') + " --exclude-from=" + settings.get('rsyncExcludes') + " -avz -e " + settings.get('sshBinary') + " " + source + "/* " + hostString + ":" + pathMap["destination"];
                    print(command)
                    subprocess.call(command, shell=True);
        if (foundMap == None):
            print("No source configured for this file.");