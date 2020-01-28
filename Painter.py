from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMenuBar,QMenu, QAction, QPushButton, QColorDialog
from PyQt5.QtGui import  QCursor,QColor,QIcon,QImage, QPainter, QPen, QPixmap,QKeySequence
from PyQt5 import QtGui,QtCore
from PyQt5.QtCore import Qt, QPoint, QSize, QRect
import random
import sys

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Painter")
        self.setWindowIcon(QIcon("icons/Painter.png"))
        self.setGeometry(100,100,800,500)
        
        
        self.image = QImage(QSize(1800,1500),QImage.Format_RGB32)
        self.image.fill(Qt.black)
        
        #brush properties
        self.drawing=False
        self.brushSize = 2
        self.penColor = "white"
        self.brushColor = QColor(str(self.penColor))
        self.lastPoint = QPoint()
               
        
        #Main Menu bar 
        mainMenu = self.menuBar()
        fileMenu = mainMenu.addMenu("File")
        brushSize = mainMenu.addMenu("Pen Size")
        
        #brush color  
        color = QAction("Pen Color",self)  
        color.triggered.connect(self.penColorPicker)
        mainMenu.addAction(color)
       
        #backgroundColor = mainMenu.addMenu("Background Color")
        backgroundColor = QAction("Change Background",self)
        backgroundColor.triggered.connect(self.BackgroundColorPicker)
        mainMenu.addAction(backgroundColor)
        
        #Items of the file menu 
        #Save the Image
        saveAction = QAction(QIcon("icons/save.png"),"Save",self)
        saveAction.setShortcut("Ctrl+S")
        fileMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)
        
        #Clear the image
        clearAction = QAction(QIcon("icons/clear.png"),"Clear",self)
        clearAction.setShortcut("Ctrl+C")
        fileMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)
        #exit the application
        exitAction = QAction(QIcon("icons/exit.png"),"Exit",self)
        exitAction.setShortcut("Alt+f4")
        fileMenu.addAction(exitAction)
        exitAction.triggered.connect(self.exit)
              
        #Items of the brush size menu 
        
        #increase brush size
        self.increaseBrushSizeAction = QAction("increase",self)
        self.increaseBrushSizeAction.triggered.connect(self.increaseBrushSize)
        self.increaseBrushSizeAction.setShortcut(QKeySequence.ZoomIn)
        brushSize.addAction(self.increaseBrushSizeAction)
        
        #decrease brush size
        self.decreaseBrushSizeAction = QAction("decrease",self)
        self.decreaseBrushSizeAction.triggered.connect(self.decreaseBrushSize)
        self.decreaseBrushSizeAction.setShortcut(QKeySequence.ZoomOut)
        brushSize.addAction(self.decreaseBrushSizeAction)
        
        #Reset brush size
        resetBrushSizeAction = QAction("reset",self)
        resetBrushSizeAction.triggered.connect(self.resetBrushSize)
        brushSize.addAction(resetBrushSizeAction)
    

    #Pen color picker
    def penColorPicker(self): 
        color =QColorDialog.getColor()
        self.penColor = color.name()
    
    #Back color picker
    #TODO
    def BackgroundColorPicker(self): 
        colors = [Qt.black,Qt.white,Qt.red,Qt.yellow,Qt.cyan,Qt.gray,Qt.darkBlue,Qt.darkCyan,Qt.darkGray,Qt.darkGreen,Qt.darkMagenta,Qt.darkRed,Qt.darkYellow,Qt.magenta,Qt.lightGray,Qt.color0,Qt.color1,Qt.transparent]
        i = random.randint(0,len(colors)-1)
        self.image.fill(colors[i])
        self.update()
        
    #Mouse Press Event
    def mousePressEvent(self, event):
        if event.type() == QtCore.QEvent.MouseButtonPress:
            if event.button() == QtCore.Qt.LeftButton:
                self.drawing = True
                self.lastPoint = event.pos()        

    #Mouse Move Event
    def mouseMoveEvent(self, event):
        
        if(event.buttons() & Qt.LeftButton) & self.drawing:
            self.brushColor = QColor(str(self.penColor))
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update() 
    
    #Mouse Release Event
    def mouseReleaseEvent(self,event ):
        if event.button == Qt.LeftButton:
            self.drawing = False
            
    # override paint event
    def paintEvent(self,event):
       
        rect = QRect(self.rect())
        #self.image.fill(QColor(str(self.backgroundColor)))
        #self.image.setPixelColor(100,200,QColor('white'))
       
        canPainter  = QPainter(self)
        canPainter.drawImage(self.rect(),self.image ,rect)
        
                 

    #Save Action 
    def save(self):
        saveFileName = "myPaint"
        filePath, _ = QFileDialog.getSaveFileName(self,"Save Image",saveFileName,"PNG(*.png);;JPEG(*.jpg *,jpeg);;  ALL Files (*.*)")
        if filePath==" ":
            return 
        else:
            self.image.save(filePath)
    
    #Clear Action
    def clear(self):
        self.image.fill(Qt.black)
        self.update()
        
    #Exit Action
    def exit(self):
        exit()
        
    #increase the size of the brush
    def increaseBrushSize(self):
        if self.brushSize < 300:
            self.brushSize *= 2
           
    #decrease the size of the brush
    def decreaseBrushSize(self):
        if self.brushSize > .5 :
            self.brushSize /= 2;

        
    
    #Reset Brush size
    def resetBrushSize(self):
        self.brushSize = 2
    

def main():
    app =QApplication(sys.argv)
    window = Window()
    window.show()    
    app.exec_()
    
   

if __name__ == "__main__":
    main()