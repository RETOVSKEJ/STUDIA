from tkinter import *
import time
from enum import Enum

class WindaState(Enum):
    IDLE = 0
    DOWN = 1
    UP = 2
    OTWARTA_PROSZE_CZEKAC = 3

windaStateStrings = {state.value: state.name for state in WindaState}

WIDTH = 640
HEIGHT = 640
ILOSC_PIETER = 5
BREAKPOINTS = [x for x in range(int(HEIGHT/ILOSC_PIETER),HEIGHT+1,int(HEIGHT/ILOSC_PIETER))]
BREAKPOINTS = BREAKPOINTS[::-1]  # reverse
WINDA_HEIGHT = BREAKPOINTS[-1]


class App():
    def __init__(self):
        self.root = Tk()
        self.root.config(bg='#292a2c', pady=3)

        self.REQUESTS = []
        self._currentSTATE = WindaState.IDLE
        self._currentPietro = 1
        self._nextPietro = 1
        self.currentPietroLabel = Label(self.root, bg='#292a2c', pady=2, fg='#eee', font=("Arial 10 bold"), text=f"Obecne Piętro: {self._currentPietro}")
        self.nextPietroLabel = Label(self.root, bg='#292a2c', pady=2, fg='#eee', font=("Arial 10 bold"), text=f"Następne Pietro: {self._nextPietro}")
        self.currentStateLabel = Label(self.root, bg='#292a2c', pady=2, fg='#eee', font=("Arial 10 bold"), text=f"Stan windy: {windaStateStrings[self._currentSTATE.value]}")
        self.currentPietroLabel.pack()
        self.nextPietroLabel.pack()
        self.currentStateLabel.pack()
 
        self.canvas = Canvas(self.root, width=WIDTH-150, height=HEIGHT)
        self.canvas.pack(side='left')

        self.createLines()

        #Create elevator
        self.windaPath = self.canvas.create_rectangle(WIDTH-250, 0, WIDTH-125, HEIGHT, fill='#ccc')
        self.winda = self.canvas.create_rectangle(WIDTH-250, BREAKPOINTS[self.currentPietro], WIDTH-125, BREAKPOINTS[self.currentPietro]-WINDA_HEIGHT, fill='green')
        self.createButtons()
        self.canvas.create_line(0, 3, WIDTH, 3, width=3, fill='blue')

    

    @property
    def currentPietro(self):
        return self._currentPietro

    @currentPietro.setter
    def currentPietro(self, value):
        self._currentPietro = value
        self.currentPietroLabel.config(text=f"Obecne Piętro: {self.currentPietro}")

    @property
    def nextPietro(self):
        return self._nextPietro

    @nextPietro.setter
    def nextPietro(self, value):
        self._nextPietro = value
        self.nextPietroLabel.config(text=f"Następne Piętro: {self.nextPietro}")

    @property
    def currentState(self):
        return self._currentSTATE

    @currentState.setter
    def currentState(self, value):
        self._currentSTATE = value
        self.currentStateLabel.config(text=f"Stan windy: {windaStateStrings[self.currentState.value]}")
        if(self.currentState == WindaState.IDLE):
            self.canvas.itemconfigure(self.winda, fill='green')
        elif(self.currentState == WindaState.OTWARTA_PROSZE_CZEKAC):
            self.canvas.itemconfigure(self.winda, fill='red')
        else:
            self.canvas.itemconfigure(self.winda, fill='gray')


    def createLines(self):
        for pietro, yPietro in enumerate(BREAKPOINTS):
            self.canvas.create_text(25, yPietro-WINDA_HEIGHT/2, text=pietro, fill="red", font=('Helvetica 18 bold'))
            self.canvas.create_line(0, yPietro, WIDTH-200, yPietro, width=2)



            # place(x=WIDTH-50, y=BREAKPOINTS[self.currentPietro]-30-pietro*22)
    def createButtons(self):
        self.buttonsList = []
        self.upButtonsList = []
        self.downButtonsList = []

        self.rightFrame = Frame(self.root).pack(side='top', anchor='n')
        self.requestsHelperButton = Button(self.rightFrame, text='REQUESTS', fg='#eee', bg='purple', command=self.printRequests).pack(side='top')

        for pietro, yPietro in enumerate(BREAKPOINTS):
            self.pietroButton = Button(self.rightFrame, text=pietro, bg='lightblue', padx=8, pady=5)
            self.pietroButton.pack(side='top')
            self.upButton = Button(self.canvas, text="UP", bg='lightblue', padx=8, pady=5, relief='groove')
            self.upButton.place(x=WIDTH-312, y=yPietro-100)
            self.downButton = Button(self.canvas, text="DOWN",  bg='lightblue', padx=8, pady=5, relief='groove')
            self.downButton.place(x=WIDTH-325, y=yPietro-60)

            self.buttonsList.append(self.pietroButton)
            self.upButtonsList.append(self.upButton)
            self.downButtonsList.append(self.downButton)

            self.pietroButton.config(command=lambda p=pietro: self.request(p, self.buttonsList[p], 'FLOOR'))
            self.upButton.config(command=lambda p=pietro: self.request(p, self.upButtonsList[p], 'UP'))
            self.downButton.config(command=lambda p=pietro: self.request(p, self.downButtonsList[p], 'DOWN'))

    def printRequests(self):
        print(self.REQUESTS)

    def request(self, pietro, button, type):
        button.config(bg='red')
        if(pietro not in self.REQUESTS):
            self.REQUESTS.append((pietro, type))


    def moveObj(self):
        moveY = (self.nextPietro - self.currentPietro) * -WINDA_HEIGHT    # minus bo breakpointy sa odwrotnie  

        if(self.nextPietro < self.currentPietro):
            self.currentState = WindaState.DOWN
        elif(self.nextPietro > self.currentPietro):
            self.currentState = WindaState.UP
        else: 
            self.currentState = WindaState.IDLE


        for _ in range(abs(moveY)):
            self.canvas.move(self.winda, 0, moveY*(1/abs(moveY)))
            coords = self.canvas.coords(self.winda)
            # print(coords) 
            time.sleep(0.004)
            self.root.update()

        self.currentPietro = self.nextPietro
        self.currentState = WindaState.OTWARTA_PROSZE_CZEKAC
        self.root.after(700, lambda: setattr(self, 'currentState', WindaState.IDLE))


    def checkRequests(self):
        target = self.currentPietro  # The number you want to find the closest value to
        closestIndex = 0
        best_difference = ILOSC_PIETER

        if len(self.REQUESTS) > 0:
            for index, (pietro, type) in enumerate(self.REQUESTS):  # ZATRZYMAJ SIĘ PO DRODZE JESLI KTOS CHCE WYSIASC WCZESNIEJ
                difference = abs(target - pietro)
                
                if difference < best_difference:
                    best_difference = difference
                    closestIndex = index

        
            if(self.currentState != WindaState.OTWARTA_PROSZE_CZEKAC):
                self.nextPietro = self.REQUESTS[closestIndex][0]
                self.moveObj()
                self.REQUESTS.pop(closestIndex)
                self.clearButtons(self.nextPietro)
            

        self.root.update()

    def clearButtons(self, index):
        self.buttonsList[index].config(bg='lightblue')
        self.upButtonsList[index].config(bg='lightblue')
        self.downButtonsList[index].config(bg='lightblue')

    def mainLoop(self):
        self.root.title('Windy - Michał 16785')
        self.root.geometry('600x720')
        self.root.update()

        while True:
            self.checkRequests()
            time.sleep(0.1)

            
myApp = App()
myApp.mainLoop()
