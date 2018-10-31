#!/usr/bin/python3
import tkinter as tk
from time import sleep
from datetime import datetime
import re
root = tk.Tk()
root.config(background="black")


root.attributes("-fullscreen", True)
root.bind('<Escape>',quit)

box = tk.Text(master=root, width=70, height=25, background = "black", foreground = "green", insertbackground = "green")

path = ""
#try to get the log
try:
    log = open("log.txt", 'a')
    log.write("\n //////////////////////////")
except:
    log = open("log.txt", "w")
    log.write("Log for text memorizer program \n //////////////////////////")

log.close()





filetext = ""

counter = 0
prevLength = 1000



txtLength = 10

def handleUni():
    typed = box.get("1.0", tk.END)
    wlist = typed.split()


    """
    for x in range(len(wlist)):
        if (wlist[x][0] == "#" and len(wlist[x]) >= 7 and wlist[x][6] == "#" ):
            unicode = wlist[x][1:6]
            wlist[x] = chr(int(unicode, 16))

            box.delete("1.0", tk.END)
            box.insert("1.0", " ".join(wlist))
    """

    if("#" in typed):
        index = typed.find("#")
        #print(index)
        #print(index + 5)
        #print(len(typed))
        if(len(typed) >= index + 6):

            if( typed[index + 5] == "#"):
                unicode = typed[index + 1:index + 5]
                s1 = typed[0:index]

                if(len(typed) <= index + 6):
                    s2 = ""
                else:
                    s2 = typed[index+6: len(typed)]

                symbol = chr(int(unicode, 16))

                typed = s1 + symbol + s2
                box.delete("1.0", tk.END)
                box.insert("1.0", typed[0: len(typed) - 1])


    box.after(10, func=handleUni)

getFile = ""

def checker():
    global counter
    typed = box.get("1.0", tk.END)

    typed = typed[0: len(typed) - 1]
    if len(typed) <= 0:
        return

    #print(typed)
    #print(filetext)
    start = counter
    end = len(typed) + start

    if (len(filetext) < end):
        end = len(filetext)

    if (typed == filetext[start:end]):
        #print("YES")
        counter = end
        box.delete("1.0", tk.END)
        box.insert("1.0", "That Was Correct!")
        root.update()

        log = open("log.txt", "a")
        log.write("\n "+ path + " | " + str(datetime.now()) + " | " + str(start) + "-" + str(end))
        log.close()
        sleep(1)

        box.delete("1.0", tk.END)

        if(end >= len(filetext)):
            counter = 0
            box.insert("1.0", "File Complete")
            getFile.config(text = "Start from beginning")
            log = open("log.txt", "a")
            log.write("\n "+ path + " | " + str(datetime.now()) + " | " + "COMPLETED")

        s = open("save.txt")

        lines = s.readlines()

        for i in range(len(lines)):
            if (path in lines[i]):
                line = lines[i].split()
                line[1] = str(counter)
                lines[i] = " ".join(line)

                s.close()
                s = open("save.txt", "w")
                for line in lines:
                    s.write(line)


            else:
                s.close()
                s = open("save.txt", 'a')
                s.write("\n" + path + " " + str(counter))
            s.close()


    else:

        #print("NO")
        box.delete("1.0", tk.END)
        box.insert("1.0", "That Was Not Correct.")
        root.update()
        sleep(1)

        box.delete("1.0", tk.END)

checkText = tk.Button(master=root, command=checker, text="Check", background = "black", foreground = "green", state="disabled")


fileSelector = tk.Entry(master=root, background = "black", foreground = "green", insertbackground = "green")
docSelector = tk.Entry(master=root, background = "black", foreground="green", insertbackground="green")

getFile = ""


def readFile():
    global filetext
    global counter
    global path
    path = fileSelector.get()
    path = path + docSelector.get()
    try:
        file = open(path)
    except:
        box.delete("1.0", tk.END)
        box.insert("1.0", "File not found")
        return

    try:
        s = open("save.txt")
        for line in s.readlines():
            if(path in line):
                x = line.split()
                counter = int(x[1])
        s.close()
    except:
        #print("No save file")
        s = open("save.txt", "w")
        s.write("Save file for memorizer program \n")
        s.close()


    filetext = file.read()
    getFile.config(text="Preview Section")
    checkText.config(state="disabled")
    box.delete("1.0", tk.END)

    start = counter
    end = counter + prevLength
    if (len(filetext) < (end)):
        end = len(filetext)
    box.insert("1.0", filetext[start:end])
    file.close()
getFile = tk.Button(master=root, command=readFile, text="Click to get file and preview", background = "black", foreground = "green")



begin = ""

def startMemo():
    box.delete("1.0", tk.END)
    box.focus_set()
    checkText.config(state="normal")
     #begin.config(text="Start next section")


def focusNext(widget):
    widget.tk_focusNext().focus_set()
    return 'break'

def focusPrev(widget):
    widget.tk_focusPrev().focus_set()
    return 'break'





box.bind('<Shift-Tab>', lambda e, box=box: focusPrev(box))



begin = tk.Button(master=root, command=startMemo, text="Start", background = "black", foreground = "green")



fileLabel = tk.Label(master=root, text = "Enter Directory Path", background = "black", foreground = "green")

docLabel = tk.Label(master=root, text = "Enter File Name" , background = "black", foreground = "green")


fileLabel.grid(row=0, column = 0, sticky=tk.N)
fileSelector.grid(row=0, column=0)


docLabel.grid(row=1, column=0, sticky=tk.N)
docSelector.grid(row=1, column=0)


getFile.grid(row=2, column=0, sticky=tk.N)


begin.grid(row=3, column=0)
checkText.grid(row=4, column=0)


box.grid(row=0, column=1, rowspan=5)

box.after(10, func=handleUni)

root.mainloop()