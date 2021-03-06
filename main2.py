# -*- coding: utf-8 -*-

import sys, random
import numpy as np
import sympy as sp
import random

from mpu import datastructures
from sympy import *
from PyQt5.QtWidgets import *#QMainWindow, QFrame, QDesktopWidget, QApplication, QWidget, QGraphicsScene, QGraphicsSceneMouseEvent
from PyQt5.QtCore import *#Qt, QBasicTimer, pyqtSignal, QPoint
from PyQt5.QtGui import *#QPainter, QColor, QPen, QPolygon

x0, x1, x2, x3, x4, x5, x6, x7, x8, x9, x10, x11, x12, x13, y0, y1, y2, y3, y4, y5, y6, y7, y8, y9, y10, y11, y12, y13 = sp.symbols('x0 x1 x2 x3 x4 x5 x6 x7 x8 x9 x10 x11 x12 x13 y0 y1 y2 y3 y4 y5 y6 y7 y8 y9 y10 y11 y12 y13')
la0, la1, la2, la3, la4, la5, la6, la7, la8, la9, la10, la11, la12, la13 = sp.symbols('la0 la1 la2 la3 la4 la5 la6 la7 la8 la9 la10 la11 la12 la13')
name = "x"
name_la = "la"
list_of_sym_coord = []
list_of_la = []
# todo найти и посмотреть transform для окна
# todo придумать что делать с совпадающими точками в MouseRelease


class GraphicsView(QGraphicsView) :
    def __init__(self,parent):
        QGraphicsView.__init__(self, parent)
        self.parent = parent
        self.setMouseTracking(True)

    def mouseMoveEvent(self, event):          #при нажатой левой кнопке мыши текущее положение курсора записывается вместо последней переменной списка Points
        # и перерисовывается текущая линия
        if self.parent.scene.drawing :
            if (self.parent.option == "line"):
                X = event.pos()  # позиция курсора
                Y = self.sceneRect()
                self.parent.Points = self.parent.Points[:-1]
                self.parent.Points.append([X.x() + Y.x(), X.y() + Y.y()])

                self.parent.repaintLine(len(self.parent.Points) - 1, len(self.parent.Points) - 2)#перерисовка
                self.drawing = False
                # Вызов перерисовки виджета
                self.parent.scene.update()




class GraphicScene(QGraphicsScene) :
    def __init__(self,parent):
        QGraphicsScene.__init__(self, parent)
        self.parent = parent
        self.path = QPainterPath()
        self.drawing = False


    def mousePressEvent(self, event): # при нажатии кнопки мыши создаются 2 точки в Points начало и конец линии. они инициализируются позицией курсора
        # создается новая линия
        if event.button() == Qt.LeftButton:
            if (self.parent.option == "line"):
                X = event.scenePos()
                self.parent.Points.append([X.x(),X.y()])#  точки новой линии
                self.parent.Points.append([X.x(), X.y()])
                self.X = X
                self.parent.paintLine(len(self.parent.Points) - 1, len(self.parent.Points) - 2)#новая линия
                self.drawing = True


                # Вызов перерисовки виджета
                self.update()


    def mouseMoveEvent(self, event):
        QGraphicsScene.mouseMoveEvent(self, event)

        if self.parent.drawing :
            if (self.parent.option == "line"):
                X = event.scenePos()
                self.parent.Points = self.parent.Points[:-1]
                self.parent.Points.append([X.x(), X.y()])

                self.parent.repaintLine(len(self.parent.Points) - 1, len(self.parent.Points) - 2)
                self.drawing = False
                # Вызов перерисовки виджета
                self.parent.update()
                self.update()






    def mouseReleaseEvent(self,event):# при отпускании мышки конечная точка текущей линии инициализируется позицией курсора, или же создается точка
        # зависит от опции
        if event.button() == Qt.LeftButton:
            if(self.parent.option == "line") :#если была нажата кнопка line. действия аналогичны mousemovevent
                X = event.scenePos()
                self.parent.Points = self.parent.Points[:-1]
                self.parent.Points.append([X.x(),X.y()])
                print(X.x())
                print(X.y())
                self.parent.repaintLine(len(self.parent.Points) - 1,len(self.parent.Points) - 2)
                self.drawing = False
                #  Добавили в список из перечня символьных величин
                list_of_sym_coord.append(globals()['x%s' % str(self.parent.glob_count)])
                list_of_sym_coord.append(globals()['y%s' % str(self.parent.glob_count)])
                self.parent.glob_count = self.parent.glob_count+1
                list_of_sym_coord.append(globals()['x%s' % str(self.parent.glob_count)])
                list_of_sym_coord.append(globals()['y%s' % str(self.parent.glob_count)])
                self.parent.glob_count = self.parent.glob_count+1
                print("Текущее состояние вектора символьных координат", list_of_sym_coord)
                #  Теперь надо создать уравнение без ограничения
                self.parent.pointsFlatten = datastructures.flatten(self.parent.Points)
                self.parent.function_no_restriction = list(map(lambda x, y: (0.5 * pow(x - y, 2)),
                                                                       list_of_sym_coord, self.parent.pointsFlatten))
                print("Текушее состоянии фукнции без ограничений", self.parent.function_no_restriction)
                #  Прибавляем глобальный счетчик для символьных значений
                self.update()

            elif self.parent.option == "point" :# если кнопка point. создается новая точка
                X = event.scenePos()
                self.parent.Points.append([X.x(), X.y()])
                #  Добавили в список из перечня символьных величин
                list_of_sym_coord.append(globals()['x%s' % str(self.parent.glob_count)])
                list_of_sym_coord.append(globals()['y%s' % str(self.parent.glob_count)])
                print("Текущее состояние вектора символьных координат", list_of_sym_coord)
                #  Теперь надо создать уравнение без ограничения
                self.parent.pointsFlatten = datastructures.flatten(self.parent.Points)
                self.parent.function_no_restriction = list(map(lambda x, y: (0.5 * pow(x - y, 2)),
                                                                       list_of_sym_coord, self.parent.pointsFlatten))
                print(self.parent.function_no_restriction)
                #  Прибавляем глобальный счетчик для символьных значений
                self.parent.glob_count = self.parent.glob_count+1
                self.parent.paintPoint(len(self.parent.Points) - 1)
                self.update()
                
            elif (self.parent.option == "delete") :# если кнопка delete
                X = event.scenePos()

                Tr = QTransform()
                flag = False
                for i in range (-5,5) :#находим объект сцены в радиусе 5 от позиции курсора
                    for j in range (-5,5) :

                        item = self.parent.scene.itemAt(X.x() + i,X.y() + j,Tr)#поиск элемента на сцене

                        if(item != None) :#если найден - прерываем цикл
                            flag = True

                        if(flag) :
                            break
                    if(flag) :
                        break

                if self.parent.lines.count(item)>0 :#если найденный объект - линия.
                    print("find item_line")
                    #idx = self.parent.lines.index(item)
                   # elem = self.parent.lines_idxs[idx]
                   # self.parent.lines_idxs.remove(elem)
                    line = item.line()
                    #if len(self.parent.Restriction) > 0:
                    for i in range(len(self.parent.pointsFlatten)):
                        if line.x1() == self.parent.pointsFlatten[i]:
                            ind_x1 = i
                        elif line.y1() == self.parent.pointsFlatten[i]:
                            ind_y1 = i
                        elif line.x2() == self.parent.pointsFlatten[i]:
                            ind_x2 = i
                        elif line.y2() == self.parent.pointsFlatten[i]:
                            ind_y2 = i
                    print("Before del:", self.parent.function_no_restriction)
                    x1_sym = list_of_sym_coord[ind_x1]
                    y1_sym = list_of_sym_coord[ind_y1]
                    x2_sym = list_of_sym_coord[ind_x2]
                    y2_sym = list_of_sym_coord[ind_y2]
                    i = 0
                    while True:
                        fl = 0
                        if y1_sym in self.parent.function_no_restriction[i].free_symbols:
                            self.parent.function_no_restriction.pop(i)
                            #print("After del:", self.parent.function_no_restriction)
                            ind_x2 -= 1
                            ind_y2 -= 1
                            fl = 1
                        elif x1_sym in self.parent.function_no_restriction[i].free_symbols:
                            self.parent.function_no_restriction.pop(i)
                            #print("After del:", self.parent.function_no_restriction)
                            ind_y1 -= 1
                            ind_x2 -= 1
                            ind_y2 -= 1
                            fl = 1
                        elif x2_sym in self.parent.function_no_restriction[i].free_symbols:
                            self.parent.function_no_restriction.pop(i)
                            #print("After del:", self.parent.function_no_restriction)
                            ind_y2 -= 1
                            fl = 1
                        elif y2_sym in self.parent.function_no_restriction[i].free_symbols:
                            self.parent.function_no_restriction.pop(i)
                            #print("After del:", self.parent.function_no_restriction)
                            fl = 1
                        i += 1
                        if fl == 1:
                            i = i - 1
                        if i >= len(self.parent.function_no_restriction):
                            break
                    list_of_sym_coord.remove(y1_sym)
                    list_of_sym_coord.remove(x1_sym)
                    list_of_sym_coord.remove(y2_sym)
                    list_of_sym_coord.remove(x2_sym)
                    print(self.parent.function_no_restriction)
                    print(list_of_sym_coord)

                        #i = 0
                        # while True:
                        #     flag = 0
                        #     for j in range(len(self.parent.Restriction[i])):
                        #         if self.parent.Restriction[i][j] != 0 and j == ind_x1:
                        #             flag = 1
                        #             print("remove ", self.parent.Restriction[i], " and ",
                        #                   self.parent.RestrictionRightVector[i])
                        #             self.parent.Restriction.pop(i)
                        #             self.parent.RestrictionRightVector.pop(i)
                        #             break
                        #
                        #         elif self.parent.Restriction[i][j] != 0 and j == ind_y1:
                        #             flag = 1
                        #             print("remove ", self.parent.Restriction[i], " and ",
                        #                   self.parent.RestrictionRightVector[i])
                        #             self.parent.Restriction.pop(i)
                        #             self.parent.RestrictionRightVector.pop(i)
                        #             break
                        #         elif self.parent.Restriction[i][j] != 0 and j == ind_x2:
                        #             flag = 1
                        #             print("remove ", self.parent.Restriction[i], " and ",
                        #                   self.parent.RestrictionRightVector[i])
                        #             self.parent.Restriction.pop(i)
                        #             self.parent.RestrictionRightVector.pop(i)
                        #             break
                        #         elif self.parent.Restriction[i][j] != 0 and j == ind_y2:
                        #             flag = 1
                        #             print("remove ", self.parent.Restriction[i], " and ",
                        #                   self.parent.RestrictionRightVector[i])
                        #             self.parent.Restriction.pop(i)
                        #             self.parent.RestrictionRightVector.pop(i)
                        #             break
                        #     if flag == 0:
                        #         self.parent.Restriction[i].pop(ind_y2)
                        #         self.parent.Restriction[i].pop(ind_x2)
                        #         self.parent.Restriction[i].pop(ind_y1)
                        #         self.parent.Restriction[i].pop(ind_x1)
                        #     if flag == 0:
                        #         i = i + 1
                        #     if (i != len(self.parent.Restriction) and flag == 1):
                        #         print("EDDD")
                        #         if self.parent.Restriction[i].count(1) == 1 and self.parent.Restriction[i].count(0) == len(self.parent.Restriction[i])-1:
                        #             print("remove ", self.parent.Restriction[i], " and ",
                        #                   self.parent.RestrictionRightVector[i])
                        #             print("remove ", self.parent.Restriction[i+1], " and ",
                        #                   self.parent.RestrictionRightVector[i+1])
                        #             self.parent.Restriction.pop(i)
                        #             self.parent.RestrictionRightVector.pop(i)
                        #             self.parent.Restriction.pop(i)
                        #             self.parent.RestrictionRightVector.pop(i)
                        #     print(self.parent.Restriction)
                        #     print(self.parent.RestrictionRightVector)
                        #     if i >= len(self.parent.Restriction):
                        #         break
                    self.parent.Points.remove([line.x1(),line.y1()])  # удаляем точки из общего массива
                    self.parent.Points.remove([line.x2(), line.y2()])
                    self.parent.scene.removeItem(item)# удаляем со сцены
                    self.parent.lines.remove(item)#удаляем из массива линий
                    self.parent.pointsFlatten = datastructures.flatten(self.parent.Points)

                elif self.parent.scPoints.count(item):#если точка
                    print("find item_point")
                    x1,y1,x2,y2 = item.rect().getRect()
                    #if len(self.parent.Restriction) > 0:
                    for i in range(len(self.parent.pointsFlatten)):
                        if x1 == self.parent.pointsFlatten[i]:
                            ind_x1 = i
                        elif y1 == self.parent.pointsFlatten[i]:
                            ind_y1 = i

                        #  Если в списке ограничений найден такой символ, то нужно определить в каком именно выражении
                        #  и удалить выражение/я
                    print("Find sym:", list_of_sym_coord[ind_y1], " in ",
                          sp.Add(*self.parent.function_no_restriction).free_symbols)
                    print("Before del:", self.parent.function_no_restriction)
                    x1_sym = list_of_sym_coord[ind_x1]
                    y1_sym = list_of_sym_coord[ind_y1]
                    i = 0
                    while True:
                        fl = 0
                        if y1_sym in self.parent.function_no_restriction[i].free_symbols:
                            self.parent.function_no_restriction.pop(i)
                            print("After del:", self.parent.function_no_restriction)
                            fl = 1
                        elif x1_sym in self.parent.function_no_restriction[i].free_symbols:
                            self.parent.function_no_restriction.pop(i)
                            print("After del:", self.parent.function_no_restriction)
                            ind_y1 -= 1
                            fl = 1
                        i += 1
                        if fl == 1:
                            i = i - 1
                        if i >= len(self.parent.function_no_restriction):
                            break


                    #  Следующий код подлежит доработке, так как предполагает, что на точку наложено ограничение.
                    #  Вдобавок не продумано удаление лямбды. Скорее заметка
                    #if lenlist_of_sym_coord
                    if list_of_sym_coord[ind_x1] in sp.Add(*self.parent.function_with_restriction).free_symbols:
                        #  Если в списке ограничений найден такой символ, то нужно определить в каком именно выражении
                        #  и удалить выражение/я
                        i = 0
                        while i < len(sp.Add(*self.parent.function_with_restriction).args):
                            fl = 0
                            if list_of_sym_coord[ind_x1] in sp.Add(*self.parent.function_with_restriction).args[i].free_symbols:
                                self.parent.function_with_restriction.pop(i)
                                fl = 1
                            i += 1
                            if fl == 1:
                                i = i-1
                        list_of_sym_coord.remove(ind_x1)

                        print(list_of_sym_coord)
                    list_of_sym_coord.remove(y1_sym)
                    list_of_sym_coord.remove(x1_sym)
                    print(list_of_sym_coord)
                        #  Старый код
                        # i = 0; df = 0
                        # while True:
                        #     flag = 0
                        #     for j in range(len(self.parent.Restriction[i])):
                        #         if self.parent.Restriction[i][j] != 0 and j == ind_x1:
                        #             flag = 1
                        #             print("remove ", self.parent.Restriction[i], " and ",
                        #                   self.parent.RestrictionRightVector[i])
                        #             self.parent.Restriction.pop(i)
                        #             self.parent.RestrictionRightVector.pop(i)
                        #             break
                        #
                        #         elif self.parent.Restriction[i][j] != 0 and j == ind_y1:
                        #             flag = 1
                        #             print("remove ", self.parent.Restriction[i], " and ",
                        #                   self.parent.RestrictionRightVector[i])
                        #             self.parent.Restriction.pop(i)
                        #             self.parent.RestrictionRightVector.pop(i)
                        #             break
                        #     if flag == 0:
                        #         self.parent.Restriction[i].pop(ind_y1)
                        #         self.parent.Restriction[i].pop(ind_x1)
                        #     if flag == 0:
                        #         i = i+1
                        #     #print(self.parent.Restriction)
                        #     #print(self.parent.RestrictionRightVector)
                        #     if (i != len(self.parent.Restriction) and flag == 1):
                        #         print("EDDD")
                        #         if self.parent.Restriction[i].count(1) == 1 and self.parent.Restriction[i].count(0) == len(self.parent.Restriction[i])-1:
                        #             print("remove ", self.parent.Restriction[i], " and ",
                        #                   self.parent.RestrictionRightVector[i])
                        #             print("remove ", self.parent.Restriction[i+1], " and ",
                        #                   self.parent.RestrictionRightVector[i+1])
                        #             df = 1
                        #             self.parent.Restriction.pop(i)
                        #             self.parent.RestrictionRightVector.pop(i)
                        #             self.parent.Restriction.pop(i)
                        #             self.parent.RestrictionRightVector.pop(i)
                        #         else:
                        #             df = 0
                        #     if i >= len(self.parent.Restriction):
                        #         break
                        # print(self.parent.Restriction)
                        # print(self.parent.RestrictionRightVector)
                    self.parent.Points.remove([x1,y1])
                    self.parent.scene.removeItem(item)
                    self.parent.scPoints.remove(item)
                    self.parent.pointsFlatten = datastructures.flatten(self.parent.Points)
                self.update()

            elif(self.parent.option == "coords")  :# если кнопка задания координат
                X = event.scenePos()

                Tr = QTransform()
                flag = False


                self.parent.showDialogEnterPoint()  # задание х
                x = self.parent.d
                '''''
                for i in range(len(self.pointsFlatten)):
                    for j in range(len(self.pointsFlatten)):
                        if self.Restriction[i][j] == 1 and j == incr*2 and self.RestrictionRightVector[j] != 0:  # Для х координаты, которая меняется
                            self.RestrictionRightVector[j] = x
                '''''
                self.parent.showDialogEnterPoint()  # задание y
                y = self.parent.d

                self.parent.repaintByPoint(X.x(), X.y(),x,y)

            elif self.parent.option == "twoPointRestriction":
                coord = event.scenePos()
                transform = QTransform()
                flag = False
                cur_value = []  # текущая выбранная точка, ее координаты по х и у
                for i in range(-5, 5):  # находим объект сцены в радиусе 5 от позиции курсора
                    for j in range(-5, 5):
                        item = self.parent.scene.itemAt(coord.x() + i, coord.y() + j,
                                                        transform)  # поиск элемента на сцене
                        if item is not None:  # если найден - прерываем цикл
                            if self.parent.lines.count(item) > 0:  # говнокод, чтобы находил точки из линии выбранную
                                for k in range(-5, 5):
                                    for m in range(-5, 5):
                                        if item.line().x1() == coord.x() + k and item.line().y1() == coord.y() + m:
                                            cur_value.append(coord.x() + k)
                                            cur_value.append(coord.y() + m)
                                        elif item.line().x2() == coord.x() + k and item.line().y2() == coord.y() + m:
                                            cur_value.append(coord.x() + k)
                                            cur_value.append(coord.y() + m)
                            else:
                                x1, y1, x2, y2 = item.rect().getRect()
                                for k in range(-5, 5):
                                    for m in range(-5, 5):
                                        if x1 == coord.x() + k and \
                                                y1 == coord.y() + m:
                                            cur_value.append(coord.x() + k)
                                            cur_value.append(coord.y() + m)
                                        elif x2 == coord.x() + k and \
                                                y2 == coord.y() + m:
                                            cur_value.append(coord.x() + k)
                                            cur_value.append(coord.y() + m)
                            flag = True
                        if flag:
                            break
                    if flag:
                        break
                if self.parent.Points.count(cur_value):
                    if len(self.parent.chsTwoPoint) < 3:
                        #print("find item")
                        self.parent.chsTwoPoint.extend(cur_value)
                        print("ChsTwoP", self.parent.chsTwoPoint)
                    else:
                        print("Too much points")
                self.update()

            elif(self.parent.option == "choose") :
                X = event.scenePos()

                Tr = QTransform()
                flag = False
                for i in range(-5, 5):
                    for j in range(-5, 5):

                        item = self.parent.scene.itemAt(X.x() + i, X.y() + j,  QTransform())

                        if (item != None):
                            flag = True

                        if (flag):
                            break
                    if (flag):
                        break

                if self.parent.lines.count(item) > 0:#аналогично уладению и созданию. сначала удаляем, потом создаем новую
                    print("find item")
                    idx = self.parent.lines.index(item)
                    #elem = self.parent.lines_idxs[idx]
                   # self.parent.lines_idxs.remove(elem)
                    line = item.line()

                    self.parent.chooseElems.append([line.x1(), line.y1()])
                    self.parent.chooseElems.append([line.x2(), line.y2()])

                    self.update()

                if (self.parent.scPoints.count(item)):
                    print("find item")
                    idx = self.parent.scPoints.index(item)
                  #  elem = self.parent.scPoints_idxs[idx]
                    x1, y1, x2, y2 = item.rect().getRect()
                    self.parent.chooseElems.append([x1,y1])

                    self.update()














class subRect(QWidget):
    text_value = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 300, 50)
        self.setWindowTitle('Выберите опцию')

        self.button1Opt = QPushButton('rect 2 points diagonal')
        self.button2Opt = QPushButton('rect 1 point, angle and lengths')

        self.layout = QGridLayout()
        self.layout.addWidget(self.button1Opt, 1, 1)
        self.layout.addWidget(self.button2Opt, 2, 1)

        self.button1Opt.clicked.connect(lambda: self.bEvent(('rect 2 points diagonal')))
        self.button2Opt.clicked.connect(lambda: self.bEvent(('rect 1 point, angle and lengths')))
        self.setLayout(self.layout)




    def bEvent(self,opt):
        self.text_value.emit(opt)
        self.hide()







class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.Points = []
        self.oldPoints = []
        self.function_no_restriction = []
        self.function_with_restriction = []
        self.Restriction = []
        self.RestrictionRightVector = []
        self.setUi()
        self.glob_count = 0
        self.counter_la = 0

       # QtWidgets.QMainWindow.__init__(self, parent=parent)
       # self.setupUi(self)
        #scene = QtWidgets.QGraphicsScene()
       # self.graphicsView.setScene(scene)
    def setUi(self):
        self.rectWin = None
        self.option = ""#при нажатии кнопки меню выбирается опция для обработки нажатия мыши
        self.lines=[]# список линий
       # self.lines_idxs = []
        self.chooseElems=[]
        self.chsTwoPoint = []  # для записи двух точек
        self.pointsFlatten = []  # для невложенного списка точек
        self.d = 0.0# для диалога ввода double
        self.incr = -1#  для диалога ввода int
        self.scPoints=[]# список точек
       # self.scPoints_idxs = []
        self.win = QWidget()
        self.center()
        self.scene = GraphicScene(self)#сцена
        self.scene.setSceneRect(75, 11, 501, 441)#отступы. переделаю
        self.buttonLine = QPushButton(self)
        self.buttonLine.setIcon(QIcon("line.png"))
        self.buttonLine.setIconSize(QSize(25, 25))
        self.buttonLine.setToolTip("Редактор линий")
        self.buttonPoint = QPushButton(self)
        self.buttonPoint.setIcon(QIcon("point.png"))
        self.buttonPoint.setIconSize(QSize(25, 25))
        self.buttonPoint.setToolTip("Редактор точек")
        self.buttonOk = QPushButton("OK")
        self.buttonOk.setToolTip("Окончить редактирование обЪекта")
        self.buttonDel = QPushButton("Delete")
        self.buttonDel.setToolTip("Выберите обЪект для удаления")
        self.buttonCoord = QPushButton("Choose Coords")
        self.buttonCoord.setToolTip("Задайте координаты")
        self.buttonChoose = QPushButton("Choose")
        self.buttonChoose.setToolTip("Выберите элемент")
        self.buttonTwoPoints = QPushButton("Ограничение по совпадению точек")
        self.buttonTwoPoints.setToolTip("Выберите 2 точки")
       # self.button2 = QPushButton(self)
        #self.button2.setIcon(QIcon("rect.png"))
       # self.button2.setIconSize(QSize(25, 25))
      #  self.button2.setToolTip("Редактор прямоугольников")
        self.view = GraphicsView(self)
       # self.view.setRubberBandSelectionMode(0)
        self.view.setSceneRect(75, 11, 501, 441)
        #self.view.setInteractive(True)
        self.view.setDragMode(1) #1-можно перетаскивать полотно 2 задало бы возможность выделения области
     #   self.scene.addItem(self.button)
        #self.scene.addWidget(self.win)
        self.view.setScene(self.scene)
        self.layout = QGridLayout()
        self.buttonsBox = QVBoxLayout()
        self.buttonRightBox = QVBoxLayout()
        self.buttonsBox.addWidget(self.buttonLine)
        self.buttonsBox.addWidget(self.buttonDel)
        self.buttonsBox.addWidget(self.buttonPoint)
        self.buttonsBox.addWidget(self.buttonOk)
        self.buttonsBox.addWidget(self.buttonCoord)
        self.buttonsBox.addWidget(self.buttonChoose)
        self.buttonRightBox.addWidget(self.buttonTwoPoints)
        self.layout.addLayout(self.buttonsBox, 1, 1)
        self.layout.addWidget(self.view, 1, 3)
        self.layout.addLayout(self.buttonRightBox, 1, 5)
        self.buttonTwoPoints.clicked.connect(lambda: self.activateFigures("twoPointRestriction"))
        self.buttonLine.clicked.connect(lambda : self.activateFigures("line"))
        self.buttonPoint.clicked.connect(lambda: self.activateFigures("point"))
        self.buttonDel.clicked.connect(lambda: self.activateFigures("delete"))
        self.buttonCoord.clicked.connect(lambda: self.activateFigures("coords"))
        self.buttonChoose.clicked.connect(lambda: self.activateFigures("choose"))
       # self.button2.clicked.connect(self.dialogOpen)
        self.buttonOk.clicked.connect(self.desactivate)
        self.win.setLayout(self.layout)
        self.eName = subRect()
        self.eName.text_value.connect(self.signalHandler)
        self.win.show()

    def showDialogEnterPoint(self):

        d, ok = QInputDialog.getDouble(self, 'Input Dialog',
                                        'Enter Coord:')

        if ok:
            self.d = d


    def showDialogEnterNum(self):

        i, ok = QInputDialog.getInt(self, 'Input Dialog',
                                        'Enter Number of Line Point:')

        if ok:
            self.incr = i



    def dialogOpen(self):
        self.eName.show()

    def signalHandler(self, text):
        self.activateFigures(text)

    def center(self):
        qr = self.win.frameGeometry() #Мы получаем прямоугольник, определяющий геометрию главного окна
        cp = QDesktopWidget().availableGeometry().center() #Мы получаем разрешение экрана нашего монитора. И с этим разрешением, мы получаем центральную точку.
        qr.moveCenter(cp)
        self.win.move(qr.topLeft())

    def activateFigures(self,opt):
        self.pointsFlatten = datastructures.flatten(self.Points)
        self.option = opt
        print(self.option)
        if(opt =="coords"):
            self.showDialogEnterNum()

            if (self.incr >= 0 and self.incr <= len(self.Points)):
                X = self.Points[self.incr]
                item = self.scene.itemAt(X[0], X[1], QTransform())
                self.repaintByPoint(item)
                self.incr = -1

    def appendTwoPointsRestriction(self):  # Ограничение совпадение двух точек

        self.oldPoints = self.Points.copy()
        ind_point = []
        for i in range(len(self.chsTwoPoint)):
            ind_point.append(self.pointsFlatten.index(self.chsTwoPoint[i]))
        self.chsTwoPoint.clear()
        list_of_la.append(globals()['la%s' % str(self.counter_la)])
        self.function_with_restriction.append(sp.Mul(list_of_la[self.counter_la],
                                                     list_of_sym_coord[ind_point[2]] - list_of_sym_coord[ind_point[0]]))
        self.counter_la += 1
        list_of_la.append(globals()['la%s' % str(self.counter_la)])  # Добавили новую лямбду в массив всех текущих лябмд
        self.function_with_restriction.append(sp.Mul(list_of_la[self.counter_la],
                                                     list_of_sym_coord[ind_point[3]] - list_of_sym_coord[ind_point[1]]))
        self.counter_la += 1
        list_of_la.append(globals()['la%s' % str(self.counter_la)])
        self.function_with_restriction.append(sp.Mul(list_of_la[self.counter_la],
                                                     list_of_sym_coord[ind_point[2]] - self.pointsFlatten[ind_point[2]]))
        self.counter_la += 1
        list_of_la.append(globals()['la%s' % str(self.counter_la)])
        self.function_with_restriction.append(sp.Mul(list_of_la[self.counter_la],
                                                     list_of_sym_coord[ind_point[3]] - self.pointsFlatten[ind_point[3]]))
        self.counter_la += 1
        #self.function_with_restriction = sp.Add(*self.function_with_restriction)
        #print("hh", self.function_with_restriction)
        #print("jjj", self.function_no_restriction)
        self.Restriction = sp.Add(sp.Add(*self.function_with_restriction), sp.Add(*self.function_no_restriction))  # Сложили две части уравнений
        print("Current function: ", self.Restriction)
        list_of_sym = list_of_sym_coord + list_of_la
        print("List of sym = ", list_of_sym)
        list_diff = list(sp.diff(self.Restriction, x) for x in list_of_sym)  # Находим производные для функции
        # по всем символьным переменным
        print(list_diff)
        cur_point = sp.solve(list_diff, list(list_of_sym))  # Здесь решили уравнение и получили новое значение в виде словаря,
        print(cur_point)
        # надо откинуть лямбды

        cur_point_without_lambda = []
        i = 0
        while i < len(list_of_sym_coord):
            cur_two_coord = []
            cur_two_coord.append(cur_point.get(list_of_sym[i]))
            cur_two_coord.append(cur_point.get(list_of_sym[i+1]))
            cur_point_without_lambda.append(cur_two_coord)
            i += 2
        for i in range(len(cur_point_without_lambda)):
            #self.Points[i] = cur_point_without_lambda[i]
            self.repaintByPoint(self.Points[i][0],self.Points[i][1],cur_point_without_lambda[i][0],cur_point_without_lambda[i][1])
        print("New points: ", self.Points)
        # Старый код
        # #print("PointsFlatten: \n", self.pointsFlatten)
        # cur_restriction1 = []
        # for i in range(len(self.pointsFlatten)):
        #     cur_restriction1.append(0)
        # cur_restriction1[ind_point[0]] = -1
        # cur_restriction1[ind_point[2]] = 1
        # self.Restriction.append(cur_restriction1)
        # self.RestrictionRightVector.append(0)
        # cur_restriction2 = []
        # for i in range(len(self.pointsFlatten)):
        #     cur_restriction2.append(0)
        # cur_restriction2[ind_point[1]] = -1
        # cur_restriction2[ind_point[3]] = 1
        # #print(cur_restriction2)
        # self.Restriction.append(cur_restriction2)
        # self.RestrictionRightVector.append(0)
        # cur_restriction3 = []
        # for i in range(len(self.pointsFlatten)):
        #     cur_restriction3.append(0)
        # cur_restriction3[ind_point[2]] = 1  # уравнение для сохранения значений x1
        # self.Restriction.append(cur_restriction3)
        # self.RestrictionRightVector.append(self.pointsFlatten[ind_point[2]])
        # cur_restriction4 = []
        # for i in range(len(self.pointsFlatten)):
        #     cur_restriction4.append(0)
        # cur_restriction4[ind_point[3]] = 1  # уравнение для сохранения значений y1
        # self.Restriction.append(cur_restriction4)
        # self.RestrictionRightVector.append(self.pointsFlatten[ind_point[3]])
        # #print(ind_point)
        # print("Restrictions: \n", np.array(self.Restriction))
        # print("Right vector of restriction", self.RestrictionRightVector)




    def desactivate(self):
        print("elems : ")
        if self.option == "choose":
            print(len(self.chooseElems))
            for i in range(len(self.chooseElems)):
                print("elem : ")
                print(self.chooseElems[i])
            self.chooseElems = []
        elif self.option == "twoPointRestriction":
            self.appendTwoPointsRestriction()


    def repaintByPoint(self,item):# меняет координаты точки с номером self.incr и перерисовывает соответствующий ей объект( динию или точку сцены)
        if self.lines.count(item) > 0:  # аналогично уладению и созданию. сначала удаляем, потом создаем новую
            print("find item")
            idx = self.lines.index(item)

            line = item.line()

            self.showDialogEnterNum()  # выбор номера точки
            incr = self.incr
            self.incr = -1
            self.showDialogEnterPoint()  # задание х
            x = self.d
            '''''
            for i in range(len(self.pointsFlatten)):
                for j in range(len(self.pointsFlatten)):
                    if self.Restriction[i][j] == 1 and j == incr*2 and self.RestrictionRightVector[j] != 0:  # Для х координаты, которая меняется
                        self.RestrictionRightVector[j] = x
            '''''
            self.showDialogEnterPoint()  # задание y
            y = self.d
            '''''
            for i in range(len(self.pointsFlatten)):
                for j in range(len(self.pointsFlatten)):
                    if self.Restriction[i][j] == 1 and j == incr*2 + 1 and self.RestrictionRightVector[j] != 0:  # Для х координаты, которая меняется
                        self.RestrictionRightVector[j] = y
            '''''
            print(x)
            print(y)
            print(self.Points)
            self.scene.removeItem(item)
            print(self.Points)
            if (incr == 0):
                self.Points.remove([line.x1(), line.y1()])
                line.setP1(QPointF(x, y))

            elif (incr == 1):
                self.Points.remove([line.x2(), line.y2()])
                line.setP2(QPointF(x, y))

            self.Points.insert([x, y], item)
            print(self.Points)

            qline = QGraphicsLineItem(line)
            self.lines[idx] = qline
            self.scene.addItem(qline)

            self.update()

        if (self.scPoints.count(item)):
            print("find item")
            idx = self.scPoints.index(item)
            #   elem = self.parent.scPoints_idxs[idx]
            x1, y1, x2, y2 = item.rect().getRect()

            self.showDialogEnterPoint()
            x = self.d
            self.showDialogEnterPoint()
            y = self.d
            self.Points.remove([x1, y1])
            self.scene.removeItem(item)
            print(x)
            print(y)

            rect = QGraphicsRectItem(x, y, x2, y2)
            self.scPoints[idx] = rect
            self.Points.append([x, y])
            self.scene.addItem(rect)
            self.update()


    def repaintByPoint(self,o_x, o_y, n_x, n_y):# меняет координаты точки с номером self.incr и перерисовывает соответствующий ей объект( динию или точку сцены)
        Tr = QTransform()
        item = self.scene.itemAt(o_x , o_y , Tr)
        flag = False
        if(item == None) :
            for i in range(-5, 5):
                for j in range(-5, 5):

                    item = self.scene.itemAt(o_x + i, o_y + j, Tr)

                    if (item != None):
                        flag = True

                    if (flag):
                        break
                if (flag):
                    break

        if self.lines.count(item) > 0:  # аналогично уладению и созданию. сначала удаляем, потом создаем новую
            print("find item")
            idx = self.lines.index(item)


            line = item.line()

            d1 = (line.x1() - o_x) * (line.x1() - o_x) + (line.y1() - o_y) * (line.y1() - o_y)
            d2 = (line.x2() - o_x) * (line.x2() - o_x) + (line.y2() - o_y) * (line.y2() - o_y)



            self.incr = -1

            '''''
            for i in range(len(self.pointsFlatten)):
                for j in range(len(self.pointsFlatten)):
                    if self.Restriction[i][j] == 1 and j == incr*2 + 1 and self.RestrictionRightVector[j] != 0:  # Для х координаты, которая меняется
                        self.RestrictionRightVector[j] = y
            '''''
            print(n_x)
            print(n_y)
            print(self.Points)
            self.scene.removeItem(item)
            print(self.Points)
            if (d1 < d2):
                idx_p = self.Points.index([line.x1(), line.y1()])
                self.Points[idx_p] = [n_x,n_y]
                line.setP1(QPointF(n_x, n_y))

            else:
                idx_p = self.Points.index([line.x2(), line.y2()])
                self.Points[idx_p] = [n_x, n_y]
                line.setP2(QPointF(n_x, n_y))

           # self.Points.insert([n_x, n_y], item)
            print(self.Points)

            qline = QGraphicsLineItem(line)
            self.lines[idx] = qline
            self.scene.addItem(qline)

            self.update()

        if (self.scPoints.count(item)):
            print("find item")
            idx = self.scPoints.index(item)
            #   elem = self.parent.scPoints_idxs[idx]
            x1, y1, x2, y2 = item.rect().getRect()


            idx_p = self.Points.index([x1, y1])

            self.scene.removeItem(item)


            rect = QGraphicsRectItem(n_x, n_y, x2, y2)
            self.scPoints[idx] = rect
            self.Points[idx_p]=[n_x, n_y]
            self.scene.addItem(rect)
            self.update()




    def paintPoint(self,i):# добавление точки на сцену
        if (i < len(self.Points)) :
            self.pen = QPen(Qt.darkBlue)
            self.pen.setStyle(1)
            point = QGraphicsRectItem(self.Points[i][0], self.Points[i][1],5,5)#рисоваться будет как квадрат
            self.scPoints.append(point)
          #  self.scPoints_idxs.append(i)
            self.scene.addItem(point)



    def paintLine(self,i,j):# добавление линии на сцену
        #if QMouseEvent.MouseButtonDblClick:
       # while QtWidgets.QWidget.event(QMouseEvent):
       #     pass

        if(j < len(self.Points) ) :
            self.pen = QPen(Qt.darkBlue)
            self.pen.setStyle(1)
            line = QGraphicsLineItem()
            line.setLine(QLineF(self.Points[i][0], self.Points[i][1], self.Points[j][0], self.Points[j][1]))
            line.setActive(True)
            line.setPen(self.pen)
            self.lines.append(line)
           # self.lines_idxs.append([i,j])
            self.scene.addItem(line)

    def repaintLine(self, i, j):# перерисовка линии с точками с индексами i,j
        # if QMouseEvent.MouseButtonDblClick:
        # while QtWidgets.QWidget.event(QMouseEvent):
        #     pass
        if (j < len(self.Points)):
            self.pen = QPen(Qt.darkBlue)
            self.pen.setStyle(1)
            line = QGraphicsLineItem()
            line.setLine(QLineF(self.Points[i][0], self.Points[i][1], self.Points[j][0], self.Points[j][1]))
            line.setActive(True)
            line.setPen(self.pen)
            if(len(self.lines)  > 0) :
                line1 = self.lines[-1]
                self.lines = self.lines[:-1]
              #  self.lines_idxs = self.lines_idxs[:-1]
                self.scene.removeItem(line1)
            self.lines.append(line)
           # self.lines_idxs.append([i,j])
            self.scene.addItem(line)




def main():
    app = QApplication(sys.argv)
    window = App()

    # myApp = QtWidgets.QWidget()#Ui_MainWindow()
    #window.show()
    sys.exit(app.exec_())

if __name__ ==  "__main__":
    main()