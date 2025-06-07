from tkinter import messagebox 

""""
Class to create and store achievements
"""

class Achievement:
    __complete = False
    __name = ""
    __message = ""
    totalComplete = 0

    def __init__(self, name, message):
        self.__name = name
        self.__message = message

    def showAchievement(self):
        self.__complete = True
        messagebox.showinfo("Achievement Unlocked!", self.__name + "\n"  + self.__message)
        Achievement.totalComplete += 1

    def setMessage(self, message):
         self.__message = message

    def setComplete(self,complete):
         # if going from complete to incomplete: decrease totalComplete
         # if going from incomplete to complete: incrememnt totalComplete
        if (self.__complete == True and complete == False):
            Achievement.totalComplete -=1
        elif (self.__complete == False and complete == True):
            Achievement.totalComplete += 1
        self.__complete = complete

    def setName(self,name):
        self.__name = name

    def getMessage(self):
        return self.__message
    
    def isComplete(self):
        return self.__complete
    
    def getName(self):
        return self.__name
    
    def getTotalComplete():
        return Achievement.totalComplete
    


