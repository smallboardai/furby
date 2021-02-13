Furby Setup From Scratch

######## Software Setup ############
sudo apt update
sudo apt upgrade
#go do something else for a while

pip3 install pyaudio
sudo apt install portaudio19-dev
sudo apt install flite

cd /home/pi
mkdir responsedata

copy runfurby.py, startfurbymotor.py, stopfurbymotor.py to
/home/pi

copy text files or wav or mp3 files to /home/pi/responsedata

Say or Play are selected by editing runfurby.py
Default Play random wav or mp3 files

######## END Software Setup ############

######### Auto Start ##########
to auto-start or stop at boot

1. boot to gui desktop
2. open file manager (pcmanfm)
3. menu view, showhidden
4. navigate to /home/pi
5. rt-click .bashrc select text editor
6. add at bottom: python3 /home/pi/runfurby.py
7. save, exit, reboot.
8. re-edit to stop (gui mode only, file is locked in console mode)
#########END Auto Start ##########

########### READ ME ###########
To run adhoc,open terminal then
python3 /home/pi/runfurby.py

to change back and forth from booting desktop or console:
in console or terminal: sudo raspi-config then System Options, then Boot/Autologin
select one that auto logs in as pi, desktop or console B2 or B4

In console mode, will auto-run with "black screen" and text
In gui desktop mode, will run hidden in background 
and every time a terminal window is opened.
..stop with ctr-c.
###########end READ ME ###########
