from tkinter import *
import customtkinter
import statistics

def LoadPassList():
    try:
        with open("100k-most-used-passwords-NCSC.txt", "r", encoding="utf-8") as commonListFile:
            commonList = [line.strip().lower() for line in commonListFile if line.strip()]
        commonListSorted = sorted(commonList, key = len, reverse = True)
        commonListDefault = set(commonListSorted)

        return commonListDefault, commonListSorted
    except FileNotFoundError:
        print("100k-most-used-passwords-NCSC.txt not found.") 
        return set(), []

commonListDefault, commonListSorted = LoadPassList()

def ScoreLen(pwd):
    #35%
    length = len(pwd)
    targetLength = 16
    if(length > targetLength):
        return 35
    else:
        return 35 * ((length / targetLength) ** 2)

def ScoreVar(pwd):
    #20%
    if len(pwd) < 2:
        return 0
    
    pwdInAscii = [ord(c) for c in pwd]
    pwdSTD = statistics.stdev(pwdInAscii)
    maxSTD = 46.5 #ascii 33 until 126
    return 20 * pwdSTD / maxSTD

def ScorePattern(pwd):
    #20%
    penalty = 0
    length = len(pwd)
    halfLength = length // 2
    for chunkSize in range(halfLength, 2, -1):
        for i in range(0, length - chunkSize - 1):
            high = i + chunkSize
            high2 = high + chunkSize
            chunk1 = pwd[i:high]
            chunk2 = pwd[high:high2]

            if chunk1 == chunk2:
                penalty = penalty + chunkSize / length
    return max(20 - penalty, 0)


def ScoreCommon(pwd):
    #25%
    pwdLowered = pwd.lower()

    penalty = 0
    numPenalties = 0
    if pwdLowered in commonListDefault:
        return 0
    else:
        for currCommon in commonListSorted:
            if len(currCommon) > len(pwdLowered):
                continue
            if currCommon in pwdLowered:
                penalty += (len(currCommon) / len(pwd)) / (numPenalties + 1)
                numPenalties += 1

        return max(25 - penalty, 0)


def ScorePass(pwd):
    score = ScoreLen(pwd) + ScoreVar(pwd) + ScorePattern(pwd) + ScoreCommon(pwd)

    return score

def ButtonPress():
    pwd = passEntry.get()
    if not pwd:
        resultLabel.configure(text="No password entered")
        return

    score = ScorePass(pwd)
    resultLabel.configure(text=f"{score:.4f}")

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

window = customtkinter.CTk()
window.title("Colloportus")
window.geometry("800x450")

mainLabel = customtkinter.CTkLabel(
    master=window,
    text="Colloportus",
    font=('Monocraft',40))
mainLabel.pack(pady = 20)

passEntry = customtkinter.CTkEntry(
    master = window,
    placeholder_text="Enter here",
    height = 50,
    width = 300
)
passEntry.pack(pady = 35)

scoreButton = customtkinter.CTkButton(master=window, text="Score", command=ButtonPress)
scoreButton.place(relx=0.5, rely=0.5, anchor=customtkinter.CENTER)

resultLabel = customtkinter.CTkLabel(
        window,
        text = "",
        font = ("Monocraft", 16)
    )
resultLabel.pack(pady=60)

window.mainloop()
