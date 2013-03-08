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
                if (pathMap["type"] == 'remote'):
                    # then replace the src path with dest path
                    remotePath = localPath.replace(pathMap["source"], pathMap["destination"]);
                    hostString = pathMap["username"] + "@" + pathMap["serverAddress"];

                    # attempt to create directories in case they do not exist already
                    lastFolderIndex = rfind("/", remotePath);
                    remoteFolder = remotePath[0:lastFolderIndex];
                    os.system(settings.get('sshBinary') + " " + hostString + "\"mkdir -p " + remoteFolder + " && exit\"");

                    # Sync file across
                    command = settings.get('scpBinary') + " -Cr " + localPath + " " + hostString + ":" + remotePath;
                    os.system(command);


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
