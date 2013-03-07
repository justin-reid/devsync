import sublime, sublime_plugin, subprocess, re, os

class DevSyncCommand(sublime_plugin.EventListener):
	def on_post_save(self, view):
		path = view.file_name()
		path = path.replace('/home/username/workspace/project/', '/data/');
		if re.match('\/data', path):
			os.system("scp " + view.file_name() + " user@dev-vm.host.com:" + path)
			#subprocess.call("/data/sync.sh")


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
