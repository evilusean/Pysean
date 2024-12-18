# Why Reaper?-2024-12-15
[Video](https://www.youtube.com/watch?v=PJrN23efnbw&ab_channel=REAPERMania)
- **Go to Preferences > General > Select "Export Configuration”**. A checklist will appear. If you check all items, REAPER will export everything, giving you an exact replica of your current REAPER when you import this file into another instance. - for future sean, save a template somewhere and back it up, so I don't have to sink days into redoing the settings/configs again
##### What Reaper Does :
Free. Open Source. Based. >150MB DL. Works on Linux.
'sudo pacman -S reaper' That's it, no VM's, no docker containers, installed.
- CustomizeASean = Everything in Reaper can be customized : Themes(Options -> Theme adjuster for custom colours), Preferences, Menus, Mouse Modifiers(hot keys), toolbars, Actions(Macros), custom hotkeys/shortcuts, 
- Track lanes + comping = choose best parts to combine into a single file
- FX chains = a group of FX/settings that can be saved and reused later for other projects
- FX can be grouped in a container to be treated like one FX
- Only one track type 
- mouse placement for fades/trimming/volume/movement - intuitive instead of a modifier
- Pre Fader Envelopes - wave form editing
- you can copy multiple audio inputs between projects easily
- Track Folders = similar to a bus, route tracks from children to parent tracks, allows you to change multiple tracks as a single unit, hold 'SHIFT' to change just one - can 'hide/show' with arrow on top left
- Regions function = allows you to arrange songs/mixes
- Automation = copy faders and use them elsewhere in the song
- Gate/EQ/Compression/Reverb/Delay + Sequencer 'MegaBaby' allows you to play a keyboard with a step sequencer, click boxes to create [Arpeggios](https://en.wikipedia.org/wiki/Arpeggio)
- Screen Sense = allows you to switch views with a hotkey
- Subprojects = I heard you like projects
- Render Qeue = Add to qeue, render later
# First Settings to Adjust in Reaper I-2024-12-15
[Video](https://www.youtube.com/watch?v=mL1aUJuODt8&list=PLM0xHqxaiT68QXHwmlkQgbJc7OpWaNTS-&ab_channel=REAPERMania)
- After first install, change some settings, most of the defaults 
- 'View' in top dropdown to hide menus/objects - most have their own hotkeys
- 'Float' Mixer = right click -> 'Dock Mixer in Docker' -> unselect to float
- Create a track = 'double click' on the track control panel
- tracks by default have very little detail press 'O' (recored mode) to bring up the menu, You can change the input type from 'mono'/'stereo'/'MIDI' from the 'Triangle' dropdown on this menu
- To change the Default appearance of tracks = 'View' -> 'ScreenSets/Layouts' 'Layouts' Tab -> 'Track Panel' -> Change Size % and Layout (A vs B vs C) 'B' shows everything for tracks
- Project Sample Rate/BPM = By Default turned off - 'File' -> 'Project Settings' -> 'Project Sample Rate' (Hz) - All samples you import will stretch or shrink to match this tempo
-  'File' -> 'Project Settings' -> 'Media' Tab = Let's you change what filetype audio format is saved as 'Wav - 24bit' is default
- Reaper 7 has a new feature that every audio file/track you create will be saved in a relative file/subfolder of that project you saved = click 2 boxes when saving 'Create subdirectory for project' and 'Copy all media into project directory' - better for backups
# First Settings to Adjust in Reaper II-2024-12-15
[Video](https://www.youtube.com/watch?v=3WEsAiop89w&list=PLM0xHqxaiT68QXHwmlkQgbJc7OpWaNTS-&index=2&ab_channel=REAPERMania)
- 'CTRL' + 'P' = Hotkey to open 'Preferences'
- New Project Template = 'Project' Tab -> 'Project Settings' -> Template File
- Backups = Will save last 50 saves by default, can add source control to projects
- Track/Send Defaults = Raise/Lower volume on tracks default - Start in Record Mode(good for midi) - Record Configs - Arm on Select(Record)
# First Settings to Adjust in Reaper III-2024-12-15
[Video](https://www.youtube.com/watch?v=azIbd6Jnz8w&list=PLM0xHqxaiT68QXHwmlkQgbJc7OpWaNTS-&index=3&ab_channel=REAPERMania)
- Item Fade Defaults = 'Fade in/Fade Out Sizes' 'CrossFade Size' Defaults 10 ms - 'Fade Shapes' - auto crossfade button
- Item Loop Defaults = Will loop items by default when you drag them out
# First Settings to Adjust in Reaper IV-2024-12-16
[Video](https://www.youtube.com/watch?v=Mm-BuE2muOU&list=PLM0xHqxaiT68QXHwmlkQgbJc7OpWaNTS-&index=4&ab_channel=REAPERMania)
- 'Action' Dropdown = 'Show Action List' HOTKEY '?' = Will show all actions/hotkeys you can take in reaper - can change actions and modifier keys - lots of customizeASean - I wonder if there is a VIM setup for Reaper? instead of 'w' press 'gg' - future sean can spend hours messing around with this, 
- https://stash.reaper.fm/tag/Key-Maps 
# Best Settings for REAPER7(2024)-2024-12-17
[Video](https://www.youtube.com/watch?v=1WhAblK8z2U&ab_channel=Reapertips%7CAlejandro)
[PDF Tip-80 pagess](https://www.reapertips.com/resources/the-perfect-setup)
'Ctrl' + 'P' = Preferences
- Remove Auto Fades = Preferences -> Project -> Item Fade Defaults -> Uncheck 'Imported Media items' 'Recorded Media Items' 'Split Media Items'
 - 'SWS: Set item fades to default length' = '?' -> set a keybind(future sean problem)
 - Use Middle Mouse for Hand Scroll to navigate(like blender) =  Preferences -> Mouse Modifiers -> Arrange View(found in top dropdown 'Context:') -> 'Middle Click' (found beside the context dropdown) -> Default Action -> Hand Scroll
 - Change Mouse Scroll Wheel to scroll up/down from zoom in/out =  '?' -> Search 'View: scroll vertically (MIDI CC relative/mousewheel)' -> 'Add' -> 'Special Key' -> *scroll on mouse wheel*
 - Zoom in/out with old keybinding replaced by above = '?' -> 'View: Zoom horizontally (MIDI CC relative/mousewheel)' -> 'Special Key' -> 'Ctrl' + 'Alt' + *scroll on mouse wheel* (old shortcut replaced)
 - Zoom Center (will zoom on mouse cursor instead of tab-more intuitive) = 'Preferences' -> 'Zoom/Scroll/Offset' -> 'Horizontal Zoom Center' -> 'Mouse Cursor' 
   Also do Vertical  = 'Vertical Zoom Center' -> 'Track Under Mouse'
 - Initial fade on play press = 'Preferences' -> 'Playback' -> deselect 'Tiny fade on playback start'
 - Disable Item Loops (will automatically create an item loop instead of extending) = Right click the track item -> 'Item Settings' -> Uncheck 'Loop item source' = Globally = 'Preferences' -> 'Item Loop Defaults' -> Uncheck all
 - to fix infinite extension of items(items will snap to end)  = 'Preferences' -> 'Mouse Modifiers' -> 'Media Item Edge (in Context: dropdown)' -> Check 'Minit edits to source media content for unlooped media items'
 - Keep Playing forever (metronome) = 'Preferences' -> 'Playback' -> Uncheck 'Stop/Repeat playback at end of project'
 - Insert Midi Notes in one click(default is click and drag) = 'Preferences' -> 'Mouse Modifiers' -> 'MIDI Piano Roll (in Context: dropdown)' -> 'Left Click(next to Context:)' -> 'Default Action' -> 'Insert Note' = After above change to 'Unselect Notes' = Simply 'Shift' + 'Click' anywhere = You can change pitch/velocity afterwards instead of clicking and dragging
 - Collapse Folder Options = 'Preferences' -> 'Track Control Panel' -> 'Folder Collapse Buttons Cycles Tracks Heights' -> 'Normal, small, hidden'
# Best MIDI settings for REAPER-2024-12-18
[Video](https://www.youtube.com/watch?v=bc58K9a_kW4&ab_channel=Reapertips%7CAlejandro)
[Article](https://seventhsam.com/guides/blog/6791049/how-to-set-up-reaper-s-midi-editor-for-better-workflow)
'Ctrl' + 'Left Click' on Tracks = Open MIDI editor
##### Midi Editor :
- 'Options' -> 'Settings' -> Midi Editor 
- Remove Floating Windows when Opening new Midi Editor = 'one midi editor per : project'
- Enable 'Active MIDI item follows selection change in arrange view'
- Allow you to switch MIDI editors by clicking on them = Check 'Selection is linked to visibility' + 'Selection is linked to editability'
- Uncheck 'Close editor when the active item is deleted in the arrange view'
- Opacity set to '3'
##### Midi Dock :
- how to dock the editor in bottom section of midi editor
- When you open MIDI editor ('Ctrl' + 'Left Click' on Tracks = Open MIDI editor) - in the toolbar click 'DOCK' button - it will dock it on bottom of screen, click on tracks to change the midi editor
- Each midi editor will be attached to a different instrument (Guitars/Drums/Bass)
##### Edit Multiple MIDI tracks at once
- Select First(Main edit) and second tracks to edit
- then right click MIDI keyboard -> CC events in multiple media items -> Draw and edit on all tracks
- Add a custom action to toolbar = 'Right Click' Tool bar -> 'Customize Tool Bar' ->'Add' -> "Options: Avoid automatically setting IDI items from other tracks editable" = will allow you to enable/disable single track edit mode from toolbar
- Color Notes by Track = 'Right Click' Midi Keyboard -> 'Color notes by track' 