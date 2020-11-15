import os
import distro
import wmctrl
import platform
import re
import subprocess
import json
import time


def termRun(command, arguments):
    output = subprocess.run([command, arguments], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return output.stdout

def getOS(architecture=False, removeLinux=False):
    os = distro.linux_distribution()[0]
    if removeLinux:
        os = re.sub('linux', '', os, flags=re.IGNORECASE)
    os = os.rstrip()
    if architecture:
        os += ' ' + platform.machine()
    os = os.lower()
    return os

def getWM():
    try:
        return wmctrl.os.environ.get('DESKTOP_SESSION').split("/")[-1].lower()
    except:
        pass
    try:
        return wmctrl.os.environ.get('XDG_SESSION_DESKTOP')
    except:
        return None

def getKernel(fullName=True):
    kernel = platform.release()
    if not fullName:
        kernel = kernel.split('-')[0]
    return kernel

def getPackages(displayPackageManager=False):
    try:
        packages = termRun('pacman', '-Qq')
        string = str(len(packages.split('\n')))
        if displayPackageManager:
            string += ' (pacman)'
        return string
    except:
        return None

def colorline(line, color1, color2):
    line = line.replace("[",f"\u001b[1m{color2}[\u001b[0m").replace("]",f"\u001b[1m{color2}]\u001b[0m")
    line = line.replace("╔",f"{color1}╔").replace("╚",f"{color1}╚").replace("═",f"{color1}═").replace("║",f"{color1}║").replace("╗",f"{color1}╗").replace("╝",f"{color1}╝")
    line = line.replace(">","\u001b[0m>")
    line = line.replace("os",f"\u001b[1m{color2}os\u001b[0m")
    line = line.replace("wm",f"\u001b[1m{color2}wm\u001b[0m")
    line = line.replace("pm",f"\u001b[1m{color2}pm\u001b[0m")
    return line


def checkColors(num: int):
    if num < 7:
        return True
    if num > 7 :
        return False


def transColor(num : int):
    if num == 0:
        return '\033[30m'
    elif num == 1:
        return '\033[31m'
    elif num == 2:
        return '\033[32m'
    elif num == 3:
        return '\033[33m'
    elif num == 4:
        return '\033[34m'
    elif num == 5:
        return '\033[35m'
    elif num == 6:
        return '\033[36m'
    elif num == 7:
        return '\033[37m'
    else:
        return ''




def main(title:str, color1:str, color2:str):
    linuxos = getOS(removeLinux=True)
    wm = getWM()
    kernel = getKernel(fullName=False)
    pkgs = getPackages(displayPackageManager=True)



    start = f"""
  ╔═[{title}]-[x]╗"""

    box = f"""║ > os: {linuxos} {kernel}
║ > wm: {wm}
║ > pm: {pkgs}"""

    end = """  ╚══════════════════════════╝
    """

    os.system("clear")

    linebox = box.splitlines()

    newstart = start
    newnum = 32 - len(start)
    newstart = newstart.replace("-","═"*newnum)

    print(colorline(newstart, color1, color2))
    for line in linebox:
        newline = line
        if len(line) == 27:
            newline = line + "║"

        elif len(line) >= 28: #* If Higher
            num = len(line) - 26
            newline = line[:-num] + f">{color1}║"

        elif len(line) < 27: #* If Lower
            num = 27 - len(line)
            newline = line + " "*num + "║"


        coloredline = colorline(newline, color1, color2)
        print("  " + coloredline) #!Debug Only:  + f"    [{str(len(line))} - {str(len(newline))}]"

        # print(line + "  -  " + str(len(line)))

    newend = colorline(end, color1, color2)
    print(newend + "\u001b[0m")







if __name__ == '__main__':
    default = None
    try:
        with open('./config.json') as f:
            data = json.load(f)
    except:
        input("Missing Config File")
        exit()

    # Check the data
    
    color1check = checkColors(data['color1'])
    color2check = checkColors(data['color2'])

    if color1check == True:
        color1 = transColor(data['color1'])
    else:
        color1 = ""

    if color2check == True:
        color2 = transColor(data['color2'])
    else:
        color2 = ""

    if color1check == True and color2check == True and data['title'] != "":
        main(data['title'], color1, color2)
    else:
        print(" -> Using Default Config.")
        time.sleep(1)
        os.system("clear")
        main("boxfetch.py","\033[31m","\033[33m")

