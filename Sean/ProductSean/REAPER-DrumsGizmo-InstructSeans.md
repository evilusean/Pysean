This actually took almost a day to figure out how to get drums in REAPER for Linux - leaving some instrumentASean instructSeans for future sean - 
DrumGizmo (works on linux, can be downloaded through AUR) : 
 https://archlinux.org/packages/extra/x86_64/drumgizmo/
 https://drumgizmo.org/wiki/doku.php?id=getting_drumgizmo
 sudo pacman -S drumgizmo #worked, it was only 2 megs, you need to download the drumkits seperately, future sean problem, at least I found something that will work

 sudo pacman -S drumsgizmo #install through AUR
 https://drumgizmo.org/wiki/doku.php?id=kits:drskit #download a drumkit
 Extract Drumkit
 Open Reaper -> Load DrumGizmo Plugin on a MIDI track -> After you load, it will open a popup that will allow you to locate the extracted folder -> look for 'DRSkit2_1.xml' and load that, 
   MidiMap should match and be the same name as the '.xml' file for drumkit, 

After adding the drumkit, and midimap, I noticed it's unlabeled, trying to fix, it works but everything is labeled generically as 'Out1-18', also only some of the outputs are working, missing a few
