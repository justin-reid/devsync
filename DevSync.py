import sublime, sublime_plugin, subprocess, re, os

class DevSyncCommand(sublime_plugin.EventListener):
    def on_post_save(self, view):
        settings = sublime.load_settings('DevSync.sublime-settings');
        pathMaps = settings.get('pathMapping');

        # Get the current file path and determine if it is in
        # the user's pathMapping array
        localPath = view.file_name();
        for pathMap in pathMaps:
            if (pathMap["source"] in localPath):
                # replace the src path with dest path
                destPath = localPath.replace(pathMap["source"], pathMap["destination"]);

                # determine the path (without file name) of the destination
                lastFolderIndex = destPath.rfind("/");
                destFolder = destPath[0:lastFolderIndex];

                osVariant = pathMap["destOS"];
                mkdir = " mkdir ";
                if (osVariant == 'linux'):
                    mkdir = mkdir + "-p ";

                if (pathMap["type"] == 'remote'):
                    hostString = pathMap["username"] + "@" + pathMap["serverAddress"];

                    # attempt to create directories in case they do not exist already
                    os.system(settings.get('sshBinary') + " " + hostString + " \"" + mkdir + destFolder + " && exit\"");

                    # Sync file across
                    command = settings.get('scpBinary') + " -Cr " + localPath + " " + hostString + ":" + destPath;
                    os.system(command);
                elif (pathMap["type"] == 'local'):
                    # attempt to create directories in case they do not exist already
                    os.system(mkdir + destFolder);

                    # copy the file
                    os.system("cp " + localPath + " " + destPath);



class devLinkCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        workingPath = self.view.file_name()
        zfIndex = workingPath.find("ZF")
        if (zfIndex == -1):
            zfIndex = workingPath.find("legacy");
        branchStart = workingPath.rfind("/", 0, zfIndex-1)
        workingPath = workingPath[branchStart:zfIndex]
        workingPath = workingPath.strip("/")

        self.view.window().run_command("exec_link", {"branchName":workingPath})

class execLinkCommand(sublime_plugin.WindowCommand):
    def run(self, branchName):
        self.window.show_input_panel("Branch to activate:", branchName, self.on_done, None, None)
        pass

    def on_done(self, text):
        subprocess.call("sh /home/user/workspace/devLinkScript " + text, shell=True)
