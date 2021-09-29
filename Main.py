import sys, random
from PyQt5 import QtCore, QtWidgets, uic

score = 0
values = {
                "0": 0,
                "31": 1,
                "32": 2,
                "41": 3,
                "42": 4,
                "43": 5,
                "51": 6,
                "52": 7,
                "53": 8,
                "54": 9,
                "61": 10,
                "62": 11,
                "63": 12,
                "64": 13,
                "65": 14,
                "11": 15,
                "22": 16,
                "33": 17,
                "44": 18,
                "55": 19,
                "66": 20,
                "21": 21,
                }

class Maexle:    
    
    def __init__(self):
        pass
    
    @staticmethod
    def getScore():
        global score
        return score;
    
    @staticmethod
    def setScore(value):
        global score
        score = value;
    
    @staticmethod
    def getValueForRoll(roll):
        roll = str(roll)        
        result = values.get(roll);
        result = str(result);
        if (result == "None"):
            result = 0;
        result = int(result);
        return result;
    
    @staticmethod
    def getValueToRoll(value):
        return list(values)[value]
    
    @staticmethod
    def sortRoll(r1, r2):
        output = ""
        #orders the rolls and write the result in the output variable
        if (r1 >= r2):
            output = str(r1) + str(r2)
        elif (r2 >= r1):
            output = str(r2) + str(r1) 
        return output
    

class MainWindow(QtWidgets.QDialog, Maexle):

    switch_window = QtCore.pyqtSignal()
    playersRoll = 0

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        uic.loadUi("playerMove.ui", self) # Load the .ui file 
        self.setWindowTitle('Player')   
        self.currentValue.setText(str(Maexle.getValueToRoll(Maexle.getScore())))
        self.buttonCommit.clicked.connect(self.switch)
        self.buttonRoll.clicked.connect(self.rollDices)
        
    def rollDices(self):
        #roll two dices
        r1 = random.randint(1, 6)
        self.leftDice.setText(str(r1))
        r2 = random.randint(1, 6)
        self.rightDice.setText(str(r2))
        self.playersRoll = Maexle.sortRoll(r1, r2)
        self.result.setText(self.playersRoll)
        
    def switch(self):  
        value1 = Maexle.getValueForRoll(self.inputText.toPlainText());
        value2 = Maexle.getValueForRoll(self.currentValue.toPlainText());
        if (int(value1) > int(value2)):
            Maexle.setScore(value1)
            if(self.computerGuess(value1)):
                self.switch_window.emit()
            else:
                pass
        else:
            print("Dein Wert ist zu niedrig!");
        
    def computerGuess(self, inputValue):
        roll = random.randint(2, 20) #TODO: Maybe flatten the curve so that the game takes somewhat longer?
        if (inputValue > roll):
            print("Der Computer glaubt dir nicht")
            if(Maexle.getValueForRoll(int(self.playersRoll)) == inputValue):
                print("Du gewinnst!")
            else:
                print("Du hast verloren!")
        else:
            print("Der Computer glaubt dir")
            return True


class WindowTwo(QtWidgets.QDialog):
    
    switch_window = QtCore.pyqtSignal()
    computerRoll = "";
    newValue = "";

    def __init__(self):
        QtWidgets.QDialog.__init__(self)
        uic.loadUi('computerMove.ui', self) # Load the .ui file
        self.setWindowTitle('Computer')
        self.computerRoll();
        self.buttonBelieve.clicked.connect(self.switch)
        self.buttonLie.clicked.connect(self.gameOver)
        
    def switch(self):
        self.switch_window.emit()
        
    def gameOver(self): #TODO: Needs its own Pop-Up
        if(Maexle.getValueForRoll(self.computerRoll) == self.newValue):
            print("Der Computer gewinnt")
        else:
            print("Der Spieler gewinnt! Der Computer hatte eine " + self.computerRoll)
        
    def computerRoll(self):
        #roll two random numbers in the space from 1 to 6 and then sort them
        r1 = random.randint(1, 6)
        r2 = random.randint(1, 6)        
        self.computerRoll = Maexle.sortRoll(r1, r2)
        computerRollValue = Maexle.getValueForRoll(self.computerRoll);
        if(computerRollValue > Maexle.getScore()):
            self.computerResult.setText(self.computerRoll);
            self.newValue = computerRollValue
        else:
            #use a degressive function to pick a random number from the left over number/value space 
            numSpace = 21 - Maexle.getScore()
            x = random.randint(0, 5) 
            self.newValue = round(numSpace*(1-0.9*0.8**x)) + Maexle.getScore()
            if (self.newValue >= 21):
                self.newValue = 21   
            self.computerResult.setText(str(Maexle.getValueToRoll(self.newValue)))
            
        Maexle.setScore(self.newValue)
             
        

class Login(QtWidgets.QWidget):

    switch_window = QtCore.pyqtSignal()

    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        self.setWindowTitle('Login')

        layout = QtWidgets.QGridLayout()

        self.button = QtWidgets.QPushButton('Login')
        self.button.clicked.connect(self.login)

        layout.addWidget(self.button)

        self.setLayout(layout)

    def login(self):
        self.switch_window.emit()


class Controller:

    def __init__(self):
        pass

    def show_login(self):
         self.login = Login()
         self.login.switch_window.connect(self.show_main)
         self.login.show()

    def show_main(self):
        self.window = MainWindow()
        self.window.switch_window.connect(self.show_window_two)
        #self.login.close()
        try:
            self.window_two.close()
        except:
            print("Window two wasnt' loaded!")
        self.window.show()

    def show_window_two(self):
        self.window_two = WindowTwo()
        self.window_two.switch_window.connect(self.show_main)
        self.window.close()
        self.window_two.show()


def main():
    app = QtWidgets.QApplication(sys.argv)
    controller = Controller()
    controller.show_main()
    #controller.show_login()
    sys.exit(app.exec_())
    #TODO: win / lose screen (with 'play again' option)


if __name__ == '__main__':
    main()
    
