import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QPointF
from PyQt5.QtGui import QPainter, QColor, QPen, QPainterPath


class Zbiornik:
   def __init__(self, x, y, width=100, height=140, nazwa=""):
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.nazwa = nazwa
      self.pojemnosc = 100.0
      self.aktualna_ilosc = 0.0
      self.poziom = 0.0  # Wartosc 0.0 - 1.0

   def dodaj_ciecz(self, ilosc):
      wolne = self.pojemnosc - self.aktualna_ilosc
      dodano = min(ilosc, wolne)
      self.aktualna_ilosc += dodano
      self.aktualizuj_poziom()
      return dodano

   def usun_ciecz(self, ilosc):
      usunieto = min(ilosc, self.aktualna_ilosc)
      self.aktualna_ilosc -= usunieto
      self.aktualizuj_poziom()
      return usunieto

   def aktualizuj_poziom(self):
      self.poziom = self.aktualna_ilosc / self.pojemnosc

   def czy_pusty(self):
      return self.aktualna_ilosc <= 0.1

   def czy_pelny(self):
      return self.aktualna_ilosc >= self.pojemnosc - 0.1

   # Punkty zaczepienia dla rur
   def punkt_gora_srodek(self):
      return (self.x + self.width / 2, self.y)

   def punkt_dol_srodek(self):
      return (self.x + self.width / 2, self.y + self.height)

   def draw(self, painter):
      # Rysowanie cieczy
      if self.poziom > 0:
         h_cieczy = self.height * self.poziom
         y_start = self.y + self.height - h_cieczy
         painter.setPen(Qt.NoPen)
         painter.setBrush(QColor(0, 120, 255, 200))
         painter.drawRect(int(self.x + 3), int(y_start), int(self.width - 6), int(h_cieczy - 2))

      # Rysowanie obrysu
      pen = QPen(Qt.white, 4)
      pen.setJoinStyle(Qt.MiterJoin)
      painter.setPen(pen)
      painter.setBrush(Qt.NoBrush)
      painter.drawRect(int(self.x), int(self.y), int(self.width), int(self.height))

      # Podpis
      painter.setPen(Qt.white)
      painter.drawText(int(self.x), int(self.y - 10), self.nazwa)



class Rura:
   def __init__(self, poczatek, koniec, grubosc=12, kolor=Qt.gray):
      self.poczatek = poczatek   #lewy górny róg
      self.koniec = koniec       #prawy dolny róg
      self.grubosc = grubosc
      self.kolor_rury = kolor
      self.kolor_cieczy = QColor(0, 180, 255)  # Jasny niebieski
      self.czy_plynie = False

   def ustaw_przeplyw(self, plynie):
      self.czy_plynie = plynie

   def draw(self, painter):         
      # Rysowanie obudowy rury
      pen_rura = QPen(self.kolor_rury, self.grubosc)
      painter.setPen(pen_rura)
      # Rysowanie cieczy w środku (jeśli płynie)
      if self.czy_plynie:  
         painter.setBrush(QBrush(self.kolor_cieczy))
      else:
         painter.setBrush(Qt.NoBrush)
      x = self.poczatek[0]
      y = self.poczatek[1]
      wysokosc = self.koniec[1] - self.poczatek[1]
      szerokosc = self.koniec[0] - self.poczatek[0]
      painter.drawRect(x, y, szerokosc, wysokosc)

      


# class Zawór(Rura):
#    def __init__(self, punkty, grubosc=12, kolor=Qt.gray):
#       super().__init__(punkty, grubosc, kolor)
#       self.otwarty = 0          # określa w ilu % otwarty jest zawór, będzie to potrzebne do przepływu cieczy

#    def ustaw_otwarcie(self, otwarcie):
#       self.otwarty = otwarcie                

class Grzalka():
   def __init__(self, srodek):
      self.srodek = srodek
      self.kolor = Qt.gray
      self.praca = 0    # 0 znaczy nie pracuje, 1 znaczy pracuje
      self.srednica = 10
      

   def grzej(self):
      self.kolor = Qt.red
      self.praca = 0

   def nie_grzej(self):
      self.kolor = Qt.grey
      self.praca = 0

   def draw(self, painter):
      pen_grzalka = QPen(self.kolor, 3, Qt.SolidLine)
      painter.setPen(pen_grzalka)
      for i in range(8):
         painter.drawEllipse(self.srodek[0] + int(self.srednica/2)*(-4+i),self.srednica,self.srednica)


      
