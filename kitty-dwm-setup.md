# DWM-Style Kitty Setup (Fresh Mac)

This repo ships a ready-to-use kitty config for a DWM-style terminal workflow.
Use the steps below to install it on a fresh macOS machine.

## Files in this repo
- `kitty/kitty.conf`
- `kitty/sessions/workspaces.kitty-session`

## Install kitty and font
1) Install kitty (for example with Homebrew):
```
brew install --cask kitty
```
2) Install the font used by the config: Inconsolata LGC.

## Install the config
```
mkdir -p ~/.config/kitty/sessions
cp /path/to/tmux-dwm/kitty/kitty.conf ~/.config/kitty/kitty.conf
cp /path/to/tmux-dwm/kitty/sessions/workspaces.kitty-session ~/.config/kitty/sessions/workspaces.kitty-session
```

Reload kitty:
```
kitty @ load-config
```
Or quit and reopen kitty.

## macOS shortcuts to disable or remap
These system shortcuts conflict with the DWM-style keybindings.

### Spotlight hotkeys
Disable Cmd+Space and Cmd+Option+Space:
```
defaults write com.apple.symbolichotkeys AppleSymbolicHotKeys -dict-add 64 '{enabled = 0;}'
defaults write com.apple.symbolichotkeys AppleSymbolicHotKeys -dict-add 65 '{enabled = 0;}'
killall SystemUIServer
```

### Screenshot hotkeys
Disable Cmd+Shift+3/4/5/6 and Cmd+Ctrl+Shift+3/4:
```
defaults write com.apple.symbolichotkeys AppleSymbolicHotKeys -dict-add 28 '{enabled = 0;}'
defaults write com.apple.symbolichotkeys AppleSymbolicHotKeys -dict-add 29 '{enabled = 0;}'
defaults write com.apple.symbolichotkeys AppleSymbolicHotKeys -dict-add 30 '{enabled = 0;}'
defaults write com.apple.symbolichotkeys AppleSymbolicHotKeys -dict-add 31 '{enabled = 0;}'
defaults write com.apple.symbolichotkeys AppleSymbolicHotKeys -dict-add 184 '{enabled = 0;}'
defaults write com.apple.symbolichotkeys AppleSymbolicHotKeys -dict-add 190 '{enabled = 0;}'
killall SystemUIServer
```

### Log Out shortcut
Cmd+Shift+Q conflicts with kitty quit. Remap or disable:
- System Settings -> Keyboard -> Keyboard Shortcuts -> App Shortcuts.
- Add an "All Applications" shortcut for "Log Out <username>..." with a different chord.

### Hide kitty shortcut
Cmd+H conflicts with resize. Disable or remap:
```
defaults write net.kovidgoyal.kitty NSUserKeyEquivalents -dict-add "Hide kitty" "@~^$h"
defaults write net.kovidgoyal.kitty NSUserKeyEquivalents -dict-add "Hide Kitty" "@~^$h"
```

## Optional: fully disable Spotlight indexing
If you want Spotlight fully off (not just hotkeys):
```
sudo mdutil -a -i off
sudo mdutil -a -d
sudo launchctl disable system/com.apple.metadata.mds
sudo launchctl disable system/com.apple.metadata.mds_stores
sudo launchctl bootout system /System/Library/LaunchDaemons/com.apple.metadata.mds.plist
sudo launchctl bootout system /System/Library/LaunchDaemons/com.apple.metadata.mds_stores.plist
```

## What you get
- 9 workspace tabs on launch via `startup_session`
- DWM-like tall layout with 50/50 master/stack
- Cmd-based navigation, resizing, and window moves
- Hidden tab bar for a clean UI
