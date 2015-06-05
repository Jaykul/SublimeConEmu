import sublime, sublime_plugin
import winreg, subprocess
import re
from os import path

CONEMU  = "C:\\Program Files\\ConEmu\\ConEmu64.exe"
CONEMUC = "C:\\Program Files\\ConEmu\\ConEmu\\ConEmuC64.exe"

try:  # can we find ConEmu from App Paths?
   apps = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\App Paths")
   subkeys, nill, nill = winreg.QueryInfoKey(apps)
   for k in range(subkeys):
      app = winreg.EnumKey(apps, k)
      if app.startswith("ConEmu"):
         cemu = winreg.QueryValue(apps, app)
         if path.exists(cemu):
            CONEMU = cemu

         dirName, fileName = path.split(cemu)
         filePath = path.join(dirName,"ConEmu",fileName.replace('ConEmu','ConEmuC'))
         if path.exists(filePath):
            CONEMUC = filePath
            break
finally:
   winreg.CloseKey(apps)

# TODO: bundle Expand-Alias with functions to save it to disk and/or send it to sublime
# TODO: cmder style bundle including ConEmu, Sublime, PSReadLine and these macros

si = subprocess.STARTUPINFO() 
si.dwFlags = subprocess.STARTF_USESHOWWINDOW
si.wShowWindow = subprocess.SW_HIDE

### For best results, we use PSReadLine and rely on it's hotkeys:
### We need KillLine and Yank set so we can copy/paste any existing command
#   Set-PSReadlineKeyHandler Ctrl+k KillLine
#   Set-PSReadlineKeyHandler Ctrl+i Yank


# { "keys": ["f5"], "command": "conemu_script" }
class ConemuScriptCommand(sublime_plugin.TextCommand):
   def run(self, edit):
      # duplicate ISE behavior:          
      if self.view.file_name():
         if self.view.is_dirty():
            self.view.run_command("save")

         script = self.view.file_name()
      else:
         script = self.view.substr(sublime.Region(0, self.view.size()))

      script = re.sub(r'\\', r'\\\\', script)

      # Use PSReadline KillLine hotkey
      subprocess.call([CONEMUC, "-GUIMACRO:0", "KEYS", "Home", "^k"], startupinfo=si)
      subprocess.call([CONEMUC, "-GUIMACRO:0", "PASTE", "2", script + "\\n"], startupinfo=si)
      # Use PSReadline Yank hotkey
      subprocess.call([CONEMUC, "-GUIMACRO:0", "KEYS", "End", "^i"], startupinfo=si)
      subprocess.call([CONEMU, "-SHOWHIDE"], startupinfo=si)

# { "keys": ["f8"], "command": "conemu_selection" }
class ConemuSelectionCommand(sublime_plugin.TextCommand):
   def run(self, edit):
      script = []
      for region in self.view.sel():
         if region.empty():
            ## If we wanted to duplicate ISE's bad behavior, we could:
            # view.run_command("expand_selection", args={"to":"line"})
            ## Instead, we'll just get the line contents without selected them:
            script += [self.view.substr(self.view.line(region))]
         else:
            script += [self.view.substr(region)]

      script = "\n".join(script) + "\n"
      script = re.sub(r'\\', r'\\\\', script)

      # Use PSReadline KillLine hotkey
      subprocess.call([CONEMUC, "-GUIMACRO:0", "KEYS", "Home", "^k"], startupinfo=si)
      subprocess.call([CONEMUC, "-GUIMACRO:0", "PASTE", "2", script], startupinfo=si)
      # Use PSReadline Yank hotkey
      subprocess.call([CONEMUC, "-GUIMACRO:0", "KEYS", "End", "^i"], startupinfo=si)
      subprocess.call([CONEMU, "-SHOWHIDE"], startupinfo=si)

