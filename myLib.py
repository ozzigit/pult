import sys
import os
#import pyautogui

defaultKeyBinds = {
    "KEY_STOP" : "xdotool key alt+F4",
    "KEY_EXIT" : "python3 /home/ozzi/myMenues/wizualmenu.py",
    "KEY_BACKSPACE" : "xdotool key 22",
    "KEY_UP" : "xdotool key Up",
    "KEY_LEFT" : "xdotool key Left",
    "KEY_RIGHT" : "xdotool key Right",
    "KEY_DOWN" : "xdotool key Down",
    "KEY_SELECT" : "xdotool key KP_Enter",
    "KEY_PAUSE" : " xdotool key space",
    "KEY_FORWARD" : "xdotool key 41",
    "KEY_BACK" : " xdotool key 27",
    "KEY_RED" : "/home/ozzi/altTab.sh \&",
    "KEY_GREEN" : "xdotool key control+alt+Left",
    "KEY_YELLOW" : "xdotool key control+alt+Right",
    "KEY_BLUE" : "xdotool key alt+F2",
    "KEY_5" : "xdotool click 1",
    "KEY_0" : "xdotool click 3",
    "KEY_1" : "xdotool mousemove_relative -- -100 0",
    "KEY_2" : "xdotool mousemove_relative -- 0 -10",
    "KEY_3" : "xdotool mousemove_relative -- 100 0",
    "KEY_4": "xdotool mousemove_relative -- -10 0",
    "KEY_6": "xdotool mousemove_relative -- 10 0",
    "KEY_7": "xdotool mousemove_relative -- 0 100",
    "KEY_8" : "xdotool mousemove_relative -- 0 10",
    "KEY_9" : "xdotool mousemove_relative -- 0 -100",
}

listOfOrderedRulesForDefaulMenu = ["Open Kodi",
                                   "Open evince",
                                   "Open gedit",
                                   "Open terminal",
                                   "Open torrent",
                                   "Левый рабочий стол",
                                   "Правый рабочий стол",
                                   "Resize window",
                                   "Close window",
                                   "Exit"]
svodPravil = {
    "kodi.bin": {
        "Kodi": {
            "KEY_BLUE": "xdotool key XF86HomePage",
        },
        "Default": {
            "KEY_BLUE": "xdotool key XF86HomePage",
        }
     },
    "transmission-gtk": {
        "Open a Torrent": {
            "KEY_LEFT": " xdotool key alt+Up",
            "KEY_RIGHT": " xdotool key KP_Enter",
        },
    },    
    "evince": {
        "Open Document": {
            "KEY_LEFT": " xdotool key alt+Up",
            "KEY_RIGHT": " xdotool key KP_Enter",

        },
        "evince": {
            "PultKey": "bash command for ecince window"
        },
        "Recent Documents": {
            "KEY_LEFT": "xdotool key alt+Up",
            "KEY_RIGHT": "xdotool key KP_Enter",

        },
        "Default": {
            "KEY_LEFT": "xdotool key Prior",
            "KEY_RIGHT": "xdotool key Next",
            "KEY_BACK": "xdotool key minus+shift+minus",
            "KEY_FORWARD": "xdotool key plus+shift+plus",
        },
    },
}
defaultCommands = {
    "Open Kodi": "kodi &",
    "Open torrent": "transmission-gtk &",
    "Resize window": "xdotool key alt+F11",
    "Close window": "xdotool key alt+F4",
}
listOfOrderedRulesForContextMenu = ["DefaultMenu",
                                    "Maximin/minim window",
                                    "Close window",
                                    "ConextMenu",
                                    "Exit"]
contextCommands = {
    "kodi.bin": {
        "Kodi": {
            "Close window" : "xdotool key alt+F4",
            "Resize window": "xdotool key backslash",
        },
        "Default": {
            "Close window": "xdotool key alt+F4",
        }
     },
    "transmission-gtk":{
        "Default": {
            "Close window": "xdotool key alt+F4",
            "Open File": "xdotool key control+32",
        },

    },
    "evince": {
        "Open Document": {
            "Close window": "xdotool key alt+F4",
            "Resize window" : "xdotool key F11",
        } ,

        "evince": {
            "Resize window": "xdotool key F11",
        },
        "Default": {
            "Open File": "xdotool key control+32",
            "Resize window": "xdotool key F11",
        }

    }
}
def getWindowRegonizeStatus(procname,windowname):
    if procname in contextCommands.keys():
        if windowname in contextCommands[procname]:
            return True
    return False

def getContextCommands(procname,windowname):
    if procname in contextCommands.keys() :
        listOfCommands = ["DefaultMenu"]
        if windowname in contextCommands[procname] :
            listOfCommands[len(listOfCommands):] = [i for i in listOfOrderedRulesForContextMenu if i in contextCommands[procname][windowname].keys()]
            #добавление правил кот нет в сортированном списке
            listOfCommands[len(listOfCommands):] = [i for i in contextCommands[procname][windowname].keys() if i not in listOfOrderedRulesForContextMenu]
            contextCommands[procname][windowname]["DefaultMenu"]="python3 /home/ozzi/myMenues/wizualDefaultMenu.py"
            contextCommands[procname][windowname]["Exit"]=""
        else:
            listOfCommands[len(listOfCommands):] = [i for i in listOfOrderedRulesForContextMenu if i in contextCommands[procname]["Default"].keys()]
            # добавление правил кот нет в сортированном списке
            listOfCommands[len(listOfCommands):] = [i for i in contextCommands[procname]["Default"].keys() if i not in listOfOrderedRulesForContextMenu]
            contextCommands[procname]["Default"]["DefaultMenu"]="python3 /home/ozzi/myMenues/wizualDefaultMenu.py"
            contextCommands[procname]["Default"]["Exit"]=""

        listOfCommands[len(listOfCommands):] = ["Exit"]
        return  listOfCommands
    else:
        return ""
def getDefaultCommands():
    listOfCommands = [i for i in listOfOrderedRulesForDefaulMenu if i  in defaultCommands.keys()]
    listOfCommands[len(listOfCommands):] = [i for i in defaultCommands.keys() if i not in listOfOrderedRulesForDefaulMenu]
    listOfCommands[len(listOfCommands):] = ["Exit"]
    defaultCommands["Exit"] = ""
    return listOfCommands

def getKeyBinds(procname,windowname):
    if windowname in svodPravil[procname] :
        for newKeys in svodPravil[procname][windowname].keys():
            defaultKeyBinds[newKeys] = svodPravil[procname][windowname][newKeys]
    else :
        if "Default" in  svodPravil[procname]:
            for newKeys in svodPravil[procname]["Default"].keys():
                defaultKeyBinds[newKeys] = svodPravil[procname]["Default"][newKeys]

def getListOfOprnWindows():
    slovarOpenWindows = {}
    command1 = "wmctrl -l -G -p"
    bashOutput1 = os.popen(command1, "r")
    while 1:
        line = bashOutput1.readline().replace('\n','')
        if not line:
            break
        nameOfWindow = ' '.join(line.split()[8:])
        if (nameOfWindow != "xfce4-panel") and (nameOfWindow != "Desktop"):
            slovarOpenWindows[nameOfWindow] = {}
            slovarOpenWindows[nameOfWindow]['ThelfName'] = nameOfWindow
            if int(line.split()[2]) != 0:
                slovarOpenWindows[nameOfWindow]['Pid'] = line.split()[2]
            else:
                bashPidFind = os.popen('ps -ax | grep -i ' + nameOfWindow, "r")
                while 1:
                    bashPidFindline = bashPidFind.readline().replace('\n','')
                    if not bashPidFindline:
                        break
                    if (bashPidFindline.split()[3] != '0:00'):
                        slovarOpenWindows[nameOfWindow]['Pid'] = str(bashPidFindline.split()[0])

            bashPs = os.popen('ps ' + str(slovarOpenWindows[nameOfWindow]['Pid']), "r")
            while 1:
                bashPsline = bashPs.readline().replace('\n','')
                if not bashPsline:
                    slovarOpenWindows[nameOfWindow]['nameOfProc'] = slovarOpenWindows[nameOfWindow].get('nameOfProc', "ungnown")
                    break
                slovarOpenWindows[nameOfWindow]['nameOfProc'] = bashPsline.split()[4]
            bashPs.close()

    bashOutput1.close()
    return slovarOpenWindows

def getNamePidOfActiweWindows() :
    activeWindowinfo = {}
    command2 = "xdotool getwindowfocus getwindowname"
    bashOutput2 = os.popen(command2, "r")
    while 1:
        line = bashOutput2.readline()
        if not line :
            break
        activeWindowinfo['Name'] = line.replace('\n','')
    bashOutput2.close()
    Pid = os.popen('xdotool getwindowpid $(xdotool getwindowfocus) 2>/dev/null',"r")
    while 1:
        pidline = Pid.readline().replace('\n','')
        if not pidline:
            activeWindowinfo['Pid'] = activeWindowinfo.get('Pid', "ungnown")
            break
        activeWindowinfo['Pid'] = pidline
    Pid.close()
    if activeWindowinfo['Pid'] == "ungnown" :
        bashPs = os.popen('ps -ax | grep -i '+activeWindowinfo['Name'],"r")
        while 1:
            line = bashPs.readline().replace('\n','')
            if not line:
                activeWindowinfo['Pid'] = activeWindowinfo.get('Pid', "ungnown")
                break
            if (line.split()[3] != '0:00'):
                activeWindowinfo['Pid'] = line.split()[0]
                activeWindowinfo['nameOfProc'] = line.split()[4]
        bashPs.close()
    else :
        bashPs = os.popen('ps ' + activeWindowinfo['Pid'], "r")
        while 1:
            line = bashPs.readline().replace('\n','')
            if not line:
                activeWindowinfo['nameOfProc'] = activeWindowinfo.get('nameOfProc', "ungnown")
                break
            activeWindowinfo['nameOfProc'] = line.split()[4]
        bashPs.close()
    if 'nameOfProc' in activeWindowinfo:
        activeWindowinfo['nameOfProc'] = activeWindowinfo['nameOfProc'][activeWindowinfo['nameOfProc'].rfind('/')+1:]
    return activeWindowinfo
