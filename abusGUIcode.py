
import sys
import pydicom
import PIL
import os
import vtk
import qimage2ndarray
import numpy as np
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets

from PyQt5.QtCore import Qt

from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog, QLabel
from PyQt5.QtGui import QIcon, QPixmap, QPainter, QBrush, QPen
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor


filename = []
pfiles = []
image = []
coronal=[]
transverse = []
colorFunc = vtk.vtkColorTransferFunction()
reader=vtk.vtkPNGReader()
shiftScale = vtk.vtkImageShiftScale()

class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1126, 828)
        
        # Initialize the widgets

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(20, 180, 150, 23))
        self.pushButton.setAutoDefault(False)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setStyleSheet(" border:2px solid rgb(0, 0, 0); ")
        self.myglwidget = QtWidgets.QOpenGLWidget(self.centralwidget)
        self.myglwidget.setGeometry(QtCore.QRect(790, 450, 311, 261))
        self.myglwidget.setMouseTracking(False)
        self.myglwidget.setTabletTracking(False)
        self.myglwidget.setObjectName("myglwidget")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(20, 230, 150, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_2.setStyleSheet(" border:2px solid rgb(0, 0, 0); ")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(500, 40, 531, 331))
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(20, 280, 150, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.pushButton_3.setStyleSheet(" border:2px solid rgb(0, 0, 0); ")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(20, 330 , 150, 23))
        self.pushButton_4.setObjectName("pushButton_3")
        self.pushButton_4.setStyleSheet(" border:2px solid rgb(0, 0, 0); ")
        self.bar = QtWidgets.QScrollBar(self.centralwidget)
        self.bar.setGeometry(QtCore.QRect(40, 730, 301, 22))
        self.bar.setMaximum(1000)
        self.bar.setOrientation(QtCore.Qt.Horizontal)
        self.bar.setInvertedAppearance(False)
        self.bar.setObjectName("bar")
        self.bar_2 = QtWidgets.QScrollBar(self.centralwidget)
        self.bar_2.setGeometry(QtCore.QRect(430, 730, 301, 22))
        self.bar_2.setMaximum(1000)
        self.bar_2.setOrientation(QtCore.Qt.Horizontal)
        self.bar_2.setObjectName("bar_2")
        self.bar_3 = QtWidgets.QScrollBar(self.centralwidget)
        self.bar_3.setGeometry(QtCore.QRect(800, 730, 301, 22))
        self.bar_3.setMaximum(1000)
        self.bar_3.setOrientation(QtCore.Qt.Horizontal)
        self.bar_3.setObjectName("bar_3")
        self.bar_4 = QtWidgets.QScrollBar(self.centralwidget)
        self.bar_4.setGeometry(QtCore.QRect(510, 380, 408, 22))
        self.bar_4.setRange(0,1000)
        self.bar_4.setOrientation(QtCore.Qt.Horizontal)
        self.bar_4.setObjectName("bar_4")
        self.bar_5 = QtWidgets.QScrollBar(self.centralwidget)
        self.bar_5.setGeometry(QtCore.QRect(450, 120, 22,270 ))
        self.bar_5.setRange(0,60)
        self.bar_5.setOrientation(QtCore.Qt.Vertical)
        self.bar_5.setObjectName("bar_5")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(510, 400, 408, 22))
        pixmap = QPixmap('rsz_slider.png')
        self.label.setPixmap(pixmap)
        self.label.show()
        self.labelbright = QtWidgets.QLabel(self.centralwidget)
        self.labelbright.setGeometry(QtCore.QRect(400, 45, 30, 418))
        pixmapbright = QPixmap('brightnessbar.png')
        self.labelbright.setPixmap(pixmapbright)
        self.label.show()
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(420, 450, 321, 261))
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(790, 450, 311, 261))
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(40, 450, 321, 261))
        self.label_text3 = QtWidgets.QLabel(self.centralwidget)
        self.label_text3.setGeometry(QtCore.QRect(100, 650, 321, 261))
        self.label_text3.setText('Transverse Plane')
        self.label_text1 = QtWidgets.QLabel(self.centralwidget)
        self.label_text1.setGeometry(QtCore.QRect(520, 650, 321, 261))
        self.label_text1.setText('Sagittal Plane')
        self.label_text2 = QtWidgets.QLabel(self.centralwidget)
        self.label_text2.setGeometry(QtCore.QRect(900, 650, 321, 261))
        self.label_text2.setText('Frontal Plane')
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1126, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)

        # connect the widgets with the functions

        self.bar.valueChanged.connect(self.update_tplane)
        self.bar_2.valueChanged.connect(self.update_splane)
        self.bar_3.valueChanged.connect(self.update_cplane)
        self.bar_4.valueChanged.connect(self.update_color)
        self.bar_5.valueChanged.connect(self.update_brightness)
        self.pushButton.clicked.connect(self.input)
        self.pushButton_3.clicked.connect(self.vis3Dmodel)
        self.pushButton_2.clicked.connect(self.saveFileDialog)
        self.pushButton_4.clicked.connect(self.threeplane)


        QtCore.QMetaObject.connectSlotsByName(MainWindow)


    def threeplane(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder = QFileDialog.getExistingDirectory(self.centralwidget,"Open a folder","",QFileDialog.ShowDirsOnly)
        for root, dirs, fils in os.walk(folder):
            for file in fils:
                if file.endswith(".png"):
                    pfiles.append(os.path.join(root, file))
        pfiles.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
        first_image = np.asarray_chkfinite(Image.open(pfiles[0]))
        print(first_image.shape)
        image=[]
        for n in range(0,len(pfiles)):
            img = np.asarray_chkfinite(Image.open(pfiles[n]))
            image.append(img)
        stack = []
        stack = np.zeros((len(pfiles),first_image.shape[0],first_image.shape[1]),np.uint8)
        for i in range(len(image)):
            stack[i,:,:]=image[i]
        for i in range(0,stack.shape[2]):
            new_img=stack[:,:,i]
            coronal.append(new_img)
        for i in range(0,stack.shape[1]):
            new_img=stack[:,i,:]
            transverse.append(new_img)

    def update_splane(self):
        fmax = len(pfiles)
        n = self.bar_2.value()
        fno = int((n-1)*(fmax-1)/999)  
        pixmap = QPixmap(pfiles[fno])
        self.label_1.setPixmap(pixmap)
        self.label_1.setScaledContents(True)

    def update_cplane(self):
        fmax = len(coronal)
        n = self.bar_3.value()
        fno = int((n-1)*(fmax-1)/999) 
        qimg = qimage2ndarray.array2qimage(coronal[fno])
        print("saved")
        pixmap = QPixmap(qimg)
        self.label_2.setPixmap(pixmap)
        self.label_2.setScaledContents(True)
       
    def update_tplane(self):

        fmax = len(transverse)
        n = self.bar.value()
        fno = int((n-1)*(fmax-1)/999) 
        qimg = qimage2ndarray.array2qimage(transverse[fno])
        print("saved")
        pixmap = QPixmap(qimg)
        self.label_3.setPixmap(pixmap)
        self.label_3.setScaledContents(True)

    def input(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        global filename
        filename = QFileDialog.getOpenFileName(self.centralwidget, ".dcm to .png", "", "dicom files (*.dcm)", options=options)[0]

    def vis3Dmodel(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        folder = QFileDialog.getExistingDirectory(self.centralwidget,"Open a folder","",QFileDialog.ShowDirsOnly)
        files=[]
        for root, dirs, fils in os.walk(folder):
            for file in fils:
                if file.endswith(".png"):
                    files.append(os.path.join(root, file))
        
        filePath = vtk.vtkStringArray()
        files.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
        #print(files)
        filePath.SetNumberOfValues(len(files))

        for i in range(0,len(files),1):
            filePath.SetValue(i,files[i])

        

        reader.SetFileNames(filePath)
        reader.SetDataSpacing(1,1,1)
        reader.Update()
        shiftScale.SetInputConnection(reader.GetOutputPort())
        self.brightcontra(0)
        shiftScale.SetOutputScalarTypeToUnsignedChar()
        self.colorfunction(1.0,0.0,0.0)

        opacity = vtk.vtkPiecewiseFunction()
        volumeProperty = vtk.vtkVolumeProperty()
        # set the color for volumes
        volumeProperty.SetColor(colorFunc)
        # To add black as background of Volume
        volumeProperty.SetScalarOpacity(opacity)
        volumeProperty.SetInterpolationTypeToLinear()
        volumeProperty.SetIndependentComponents(2)

        #Ray cast function know how to render the data
        volumeMapper = vtk.vtkOpenGLGPUVolumeRayCastMapper()
        volumeMapper.SetInputConnection(shiftScale.GetOutputPort())
        volumeMapper.SetBlendModeToMaximumIntensity()

        volume = vtk.vtkVolume()
        volume.SetMapper(volumeMapper)
        volume.SetProperty(volumeProperty)
 
        # Display the object in the frame
        self.vl = QtWidgets.QVBoxLayout()
        self.vtkWidget = QVTKRenderWindowInteractor(self.frame)
        self.vl.addWidget(self.vtkWidget)
 
        self.ren = vtk.vtkRenderer()
        self.vtkWidget.GetRenderWindow().AddRenderer(self.ren)
        self.iren = self.vtkWidget.GetRenderWindow().GetInteractor()

        
        self.ren.AddVolume(volume)
        self.frame.setLayout(self.vl)
        self.vtkdisplay()


    def brightcontra(self,bright = 0):
        shiftScale.SetShift(bright)

    def vtkdisplay(self):
        self.iren.Initialize()
        
    def colorfunction(self,r,g,b):
        colorFunc.AddRGBPoint(2, r, g, b)

    def update_brightness(self):
        n = self.bar_5.value()
    
        print(n)
        self.brightcontra(n)
        self.vtkdisplay()
    
    
    def update_color(self):
        n = self.bar_4.value()
        r = 1.0
        g = 1.0
        b = 1.0
        if n in range(0,100):
            r = 1.0
            g = n/100.0
            b = 0.0
        else :
            if n in range(101,200):
                r = (200.0 - n)/100.0
                g = 1
                b = 0.0
            else :
                if n in range(201,300):
                    r = 0.0
                    g = 1.0
                    b = (n - 200.0)/100.0
                else:
                    if n in range(301,400):
                        r = 0.0
                        g = (400.0-n)/100.0
                        b = 1.0
                    else :
                        r = (n - 400.0)/100.0
                        g = 0.0
                        b = 1.0
        red = r*255
        green = g*255
        blue = b*255
        self.bar_4.setToolTip("rgb :%d %d %d" %(red,green,blue) )
        self.colorfunction(r,g,b)
        self.vtkdisplay()
       
    

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        my_dirURL = QFileDialog.getExistingDirectory(self.centralwidget,"Open a folder","",QFileDialog.ShowDirsOnly)
        fileToPng = filename

        if my_dirURL:
            if fileToPng:
               # for f in filesToPng:
                    #create a directory here with the name same as x
                    print(fileToPng)
                    y = os.path.basename(fileToPng)
                    print(y)
                    x = os.path.splitext(y)[0]
                    print(x)
                    #global my_newdirURL
                    my_newdirURL = my_dirURL + "/" + x
                    os.mkdir(my_newdirURL)
                    #if '.dcm' in f:
                        #reads a dicom file
                    ds = pydicom.dcmread(fileToPng)
                        #gets the number of frames , width and height
                    (fr, w, h) = ds.pixel_array.shape

                        #gets the individual dicom frames and saves them in png (monochrome)
                    for i in range(0,fr):
                            frame = ds.pixel_array[i]
                        
                            img = PIL.Image.fromarray(frame)
                            z = i + 1
                            z   = str(z)
                            
                            img.save(my_newdirURL+"/"+ x + "frame_" + z + ".png")
            
    
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", ".dcm to .png"))
        self.pushButton_3.setText(_translate("MainWindow", "3D rendering"))
        self.pushButton_2.setText(_translate("MainWindow", "Save .png files"))
        self.pushButton_4.setText(_translate("MainWindow", "View in 3 Planes"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

