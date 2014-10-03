Sublime ConEmu
==============

Add some helper commands for using Sublime with ConEmu (and PowerShell).

In order to use the commands, you should to set hotkeys for them in your KeyBindings, so for instance, click `Preferences` and then `Key Bindings -- User` and paste this:

```
[
   { "keys": ["f5"], "command": "conemu_script" },
   { "keys": ["f8"], "command": "conemu_selection" },
]
```

This is primarily written for PowerShell, and for best results, we use PSReadLine and rely on it's hotkeys. We need KillLine and Yank set so we can copy/paste any existing command, so you need to run these commands in your PowerShell profile:

```posh
    Set-PSReadlineKeyHandler Ctrl+k KillLine
    Set-PSReadlineKeyHandler Ctrl+i Yank
```

### conemu_script (ConemuScriptCommand)

    Invokes the path to the active file in the active ConEmu window

### conemu_selection (ConemuSelectionCommand)

    Pastes the active line or selected text
