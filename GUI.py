from re import A, I
import turtle
from sly import Lexer
from sly import Parser

import turtle
import ctypes
import os
import tkinter
from tkinter import *
from tkinter import filedialog,Text
from turtle import title

root = Tk()
root.attributes("-fullscreen", True)

# Rearraning the title and creating app list

root.title("tirtil Draws Dick!")
apps= []

# Rearranging the icon
root.iconbitmap('C:\Automata.ico')

# Creating the canvas of turtle
canvas= Canvas(root, width=1119, height= 839)
tirtil = turtle.RawTurtle(canvas)


# Defining some actions
def openFile():

    filename= filedialog.askopenfilename(initialdir="/", title="Select File",
                        filetypes= (("Text Files", "*.txt"),("all files", "*.txt")))

    if len(apps) == 0:
            apps.append(filename)
            print(filename)
    else :
        apps.clear()
        apps.append(filename)
        print(filename)
    global app
    for app in apps:
        global kLabel
        kLabel= Label(root, text=app, bg="white")
        kLabel.grid(row= 33,column= 0)
    
    selectingButton['state'] = DISABLED
    deletingButton['state'] = NORMAL
    readingButton['state'] = NORMAL

def deselectFile():
    kLabel.destroy()
    textField.delete('1.0', END)
    selectingButton['state'] = NORMAL
    deletingButton['state'] = DISABLED
    readingButton['state'] = DISABLED

def runApps():
    for app in apps:
        os.startfile(app)

def openText():
    text_file= open(app, 'r')
    burhan= text_file.read()
    textField.insert(END, burhan)
    text_file.close()


def cembur(texttouse, tirtil):

    #Tokenların oluşturulduğu class

    class basicLexer(Lexer):
        tokens = { F, R, L, COLOR, PEN , NUMBER}
        ignore = '\t'
        
        literals = { '[' , ']' , ' ' }
        
        F = r'F'
        R = r'R'
        L = r'L'
        COLOR = r'COLOR'
        PEN = r'PEN'
        harf = r'M',r'Y',r'K',r'S'
        
        
        #Tam sayı değerlerini atama
        
        @_(r'\d+')
        def NUMBER(self,t):
            t.value=int(t.value)
            return t
        
        #Yeni satır ekleme

        @_(r'\n+')
        def newline(self,t ):
            self.lineno = t.value.count('\n')
            
    #Parse ağacının oluşturulduğu class
        
    class basicParser(Parser):
        tokens = basicLexer.tokens
    
        def __init__(self):
            self.env = { }
            
        @_('')
        def statement(self, p):
            pass
        
        @_('feature')
        def statement(self, p):
            return (p.feature)
        
        @_('move')
        def statement(self, p):
            return (p.move)
        
        #Gramer tanımları
        
        @_('move feature')
        def Dstatement(self, p):
            return (p.move, p.feature)
        
        @_('Dstatement')
        def statement(self, p):
            return (p.Dstatement)
        
        @_('move move')
        def Dstatement(self, p):
            return (p.move0, p.move1)
            
        @_('loop "[" Dstatement "]"')
        def statement(self, p):
            return ('g1', p.loop, p.Dstatement)
        
        #Loop komutu
        
        @_('L expr')
        def loop(self, p):
            return ('loop', p.L ,p.expr)
        
        #Forward komutu
        
        @_('F expr')
        def move(self, p):
            return ('forward',p.F ,p.expr)
        
        #Rotate komutu
        
        @_('R expr')
        def move(self, p):
            return ('rotate',p.R ,p.expr)

        #Renk değiştirme Komutu

        @_('COLOR expr')
        def feature(self, p):
            return ('color', p.COLOR, p.expr)

        #Kalem kalınlığı komutu
        
        @_('PEN expr')
        def feature(self, p):
            return ('pensize', p.PEN, p.expr)
        
        @_('NUMBER')
        def expr(self, p):
            return ('num', p.NUMBER)
        
        
    #tirtil fonksiyonları

    class tirtilFun:
        def LP(ib, integer1, integer2 , a , b):
            for i in range(ib[a][b]):
                tirtil.forward(integer1)
                tirtil.left(integer2)
                
        def kalemBoyu(a):
            if a == 1:
                tirtil.pensize(1)
            elif a == 2:
                tirtil.pensize(5)
            elif a == 3:
                tirtil.pensize(10)
                
        def kalemRengi(renk):
            if renk == 'K':
                tirtil.color('red')
            elif renk == 'M':
                tirtil.color('blue')
            elif renk == 'Y':
                tirtil.color('green')
            elif renk == 'S':
                tirtil.color('black')

    #Tokenlara ve parse ağacına göre çıkan komutları çalıştıran class
        
    class basicExecute:
        

        def __init__(self, tree, env):
            self.env = env
            result = self.walkTree(tree)
            if result is not None and isinstance(result, int):
                print(result)
            if isinstance(result, str) and result[0] == '"':
                print(result)
                
        #Ağaçtaki nodeları çıkan komuta göre birleştiren fonksiyon 
                
        def walkTree(self, node):
            
            if node[0] is None:
                return None
            
            if node[0] =='forward':
                tirtil.forward(node[2][1])
                
            if node[0] =='rotate':
                tirtil.left(node[2][1])
                
            if node[0] =='g1':
                tirtil.speed(1)
                tirtil.color("red")
                tirtil.pensize(20)
                tirtilFun.LP(node[2][1], 60, 45,2,1)
                
            if node[0] == 'pensize':
                tirtilFun.kalemBoyu(node[2][1])
                
            if node[0] == 'color':
                tirtilFun.kalemRengi(node[2][1])
                
        
    #Main fonksiyon


    if __name__ == '__main__': 
        lexer = basicLexer()
        parser = basicParser()
        env = {}
        text = texttouse
        tree = parser.parse(lexer.tokenize(text))
        print(tree)
        basicExecute(tree, env)

cembur('F100', tirtil)


# Creating Entry(text) Widget
textField = Text(root, width=50,height= 22, borderwidth=5, bg="black", fg="white")
debugField = Text(root, width=50,height= 22, borderwidth=5, bg="white", fg="black")

# Creating some Button Widgets and adjusting some settings
selectingButton = Button(root, text="Select File", padx=50, pady=2, command=lambda: [openFile(), openText()] , fg="blue", bg="red")
readingButton = Button(root, text="Read the selected TXT file", state=DISABLED, padx=9, pady=2, command=runApps, fg="blue", bg="red" )
deletingButton = Button(root, text="Deselect", padx=9, pady=2, state=DISABLED, command=deselectFile,fg="blue", bg="red" )
quit_Button= Button(root, text=' X ', command=root.quit)

# Putting them onto the screen
selectingButton.grid(row= 1,column= 0, sticky= S)
readingButton.grid(row= 2, column= 0, sticky= N)
deletingButton.grid(row= 3, column= 0, sticky= N)
canvas.grid(row= 0,column= 1, rowspan= 32)
textField.grid(row= 4,column= 0, rowspan= 20 )
quit_Button.grid(row=0, column=0, sticky=NW, padx=4, pady=4 )
debugField.grid(row= 25,column= 0, rowspan= 7 )

# Running the program
root.mainloop()
