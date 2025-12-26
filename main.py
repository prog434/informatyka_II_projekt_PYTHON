import sys
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QTimer, QPointF, QPoint
from PyQt5.QtGui import *


class Zbiornik:
   def __init__(self, x, y, width=100, height=140, nazwa="", kolor_cieczy = Qt.blue):
      self.x = x
      self.y = y
      self.width = width
      self.height = height
      self.nazwa = nazwa
      self.pojemnosc = 100.0
      self.aktualna_ilosc = 0.0
      self.poziom = 0.0  # Wartosc 0.0 - 1.0
      self.kolor_cieczy = kolor_cieczy

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
   def punkt_gora(self):
      return (self.x, int(self.y+10))

   def punkt_dol(self):
      return (int(self.x + self.width), int(self.y + self.height-10))

   def draw(self, painter):
      # Rysowanie cieczy
      if self.poziom > 0:
         h_cieczy = self.height * self.poziom
         y_start = self.y + self.height - h_cieczy
         painter.setPen(Qt.NoPen)
         painter.setBrush(self.kolor_cieczy)
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
   def __init__(self, poczatek, koniec, grubosc=2, kolor=Qt.gray, kolor_cieczy = Qt.blue):
      self.poczatek = poczatek   #lewy górny róg
      self.koniec = koniec       #prawy dolny róg
      self.grubosc = grubosc
      self.kolor_rury = kolor
      self.kolor_cieczy = kolor_cieczy
      self.czy_plynie = False

   def ustaw_przeplyw(self, plynie):
      self.czy_plynie = plynie

   def draw(self, painter):         
      # Rysowanie obudowy rury
      pen_rura = QPen(self.kolor_rury, self.grubosc)
      painter.setPen(pen_rura)
      # Rysowanie cieczy w środku (jesli plynie)
      if self.czy_plynie:  
         painter.setBrush(QBrush(self.kolor_cieczy))
      else:
         painter.setBrush(Qt.NoBrush)
      x = self.poczatek[0]
      y = self.poczatek[1]
      wysokosc = self.koniec[1] - self.poczatek[1]
      szerokosc = self.koniec[0] - self.poczatek[0]
      painter.drawRect(x, y, szerokosc, wysokosc)

   def punkty_prawe(self):       #prawe wierzcholki rury
      return (self.koniec[0], self.poczatek[1], self.koniec[1])   # x, y(gora), y(dol)

      
               

class Zawor:
   def __init__(self, poczatek, grubosc=2):    #poczatek to 3 wspolrzedne, x=lewa krawedz zaworu, y1= wysokosc gora, y2= wysokosc dol
      self.x = poczatek[0]
      self.yg = poczatek[1]
      self.yd = poczatek[2]
      self.grubosc = grubosc
      self.otwarcie = 100  # określa w ilu % otwarty jest zawór, będzie to potrzebne do przepływu cieczy
      self.szer = 30
      self.xp = self.x+self.szer
      
      
   def ustaw(self, procent_otw):
      self.otwarcie = procent_otw
      
   def pobierz_otwarcie(self):
      return (int(self.otwarcie))

   def draw(self,painter):
      pen_zaw = QPen(Qt.gray,self.grubosc)
      painter.setPen(pen_zaw)
      #skladnik_rgb = int(255-int(self.otwarcie*2.55)) #bialy-zamkniecie, czarny-otwarcie  (oba pelne) #lepiej jest na odwrot
      skladnik_rgb = int(self.otwarcie*2.55)
      kolor = QColor(skladnik_rgb, skladnik_rgb, skladnik_rgb)
      painter.setBrush(QBrush(kolor))
      painter.drawPolygon(QPolygon([QPoint(self.x,self.yg), QPoint(self.x,self.yd), QPoint(int(self.x+self.szer/2),int((self.yg+self.yd)/2))]))
      painter.drawPolygon(QPolygon([QPoint(int(self.x+self.szer),self.yg), QPoint(int(self.x+self.szer),self.yd), QPoint(int(self.x+self.szer/2),int((self.yg+self.yd)/2))]))

   def punkty_prawe(self):       #prawe wierzcholki zaworu
      return (self.xp, self.yg, self.yd)   # x, y(gora), y(dol)  
   
   



class Grzalka:
   def __init__(self, srodek):
      self.srodek = srodek
      self.kolor = Qt.gray
      self.praca = False   # 0 znaczy nie pracuje, 1 znaczy pracuje
      self.srednica = 10
      

   def grzej(self):
      self.praca = 1

   def nie_grzej(self):
      self.praca = 0

   def draw(self, painter):
      if self.praca:
         self.kolor = Qt.red
      else:
         self.kolor = Qt.gray
      pen_grzalka = QPen(self.kolor, 3, Qt.SolidLine)
      painter.setPen(pen_grzalka)
      painter.setBrush(Qt.NoBrush)
      for i in range(8):
         painter.drawEllipse(int(self.srodek[0] + int(self.srednica/2)*(-4+i)),self.srodek[1],self.srednica,self.srednica)


      
class Skraplacz:
   def __init__(self, x, y, grubosc=2, fi=5, szer=100, wys=130):
      self.x = x 
      self.y = y + 5       #odstęp dobrany taki, by rura byla na tej samej wysokosci co skraplacz
      self.grubosc = grubosc
      self.fi = fi           #tutaj to akurat srednica wewnetrzna rury
      self.szer = szer
      self.wys = wys
      self.skraplanie = False

   def draw(self, painter):
      pen_skr = QPen(Qt.gray, int(self.grubosc+self.fi))
      pen_ciecz = QPen(Qt.white, int(self.fi))

      path = QPainterPath()
      path.moveTo(self.x, self.y)
      path.lineTo(int(self.x+self.szer-10), self.y)
      path.lineTo(int(self.x+self.szer-10), int(self.y+self.wys/2))
      path.lineTo(int(self.x+10), int(self.y+self.wys/2))
      path.lineTo(int(self.x+10), int(self.y+self.wys))
      path.lineTo(int(self.x+self.szer), int(self.y+self.wys))

      painter.setBrush(Qt.NoBrush)
      painter.setPen(pen_skr)
      painter.drawPath(path)
      if self.skraplanie:
         painter.setPen(pen_ciecz)
         painter.drawPath(path)


class Symulacja(QWidget):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("scada")
      self.setFixedSize(900, 600)
      self.setStyleSheet("background-color: #D3D3D3;")


      # --- Konfiguracja Zbiornikow ---
      self.z_magazyn = Zbiornik(30,30, nazwa = "MAGAZYN")
      self.z_magazyn.aktualna_ilosc = 100
      self.z_magazyn.aktualizuj_poziom()
      self.z_grzanie = Zbiornik(200,self.z_magazyn.punkt_dol()[1], nazwa = "GRZANIE")
      self.z_odpad = Zbiornik(350,self.z_grzanie.punkt_dol()[1],nazwa="ODPAD", kolor_cieczy=QColor(165, 42, 42))
      self.z_skraplacz = Zbiornik(500,self.z_magazyn.punkt_dol()[1], nazwa ="SKRAPLANIE")
      self.z_produkt = Zbiornik(650,self.z_skraplacz.punkt_dol()[1], nazwa= "PRODUKT", kolor_cieczy=QColor(0, 180, 255))

      # --- Konfiguracja Rur ---
      self.r_mg = Rura(self.z_magazyn.punkt_dol(),[int(200-30),self.z_grzanie.punkt_gora()[1]])
      self.r_go = Rura(self.z_grzanie.punkt_dol(),[int(350-30),self.z_odpad.punkt_gora()[1]],kolor_cieczy=QColor(165, 42, 42))
      self.r_gs = Rura([self.z_grzanie.punkt_dol()[0],int(self.z_grzanie.punkt_gora()[1]-10)],[int(500-30),self.z_skraplacz.punkt_gora()[1]], kolor_cieczy=Qt.white)
      self.r_sp = Rura(self.z_skraplacz.punkt_dol(),[int(650-30),self.z_produkt.punkt_gora()[1]])

      # --- Konfiguracja Zaworow ---
      self.zaw_mg = Zawor(self.r_mg.punkty_prawe())
      self.zaw_go = Zawor(self.r_go.punkty_prawe())
      self.zaw_gs = Zawor(self.r_gs.punkty_prawe())
      self.zaw_sp = Zawor(self.r_sp.punkty_prawe())

      # --- Konfiguracja Grzalki ---
      self.grzalka = Grzalka([int((self.z_grzanie.punkt_gora()[0]+self.z_grzanie.punkt_dol()[0])/2), int(self.z_grzanie.punkt_dol()[1]-10)])

      # --- Konfiguracja Skraplacza ---
      self.skraplacz = Skraplacz(500,self.z_magazyn.punkt_dol()[1])

      # pakowanie do tablic
      self.zbiorniki = [self.z_magazyn, self.z_grzanie,self.z_odpad,self.z_skraplacz,self.z_produkt]
      self.rury = [self.r_mg, self.r_go, self.r_gs, self.r_sp]
      self.zawory = [self.zaw_mg, self.zaw_go, self.zaw_gs, self.zaw_sp]


      # # --- Timer i sterowanie ---

      self.przyciski_kontoroli_recznej()
      self.timer = QTimer()
      self.timer.timeout.connect(self.logika_przeplywu)
      self.pracuje = False
      
      for z in self.zbiorniki:
         z.aktualizuj_poziom()
      
   def logika_przeplywu(self):
      self.przeplyw = self.zaw_go.pobierz_otwarcie()/100
      #magazyn->grzanie
      plynie_1 = False
      if not self.z_magazyn.czy_pusty() and not self.z_grzanie.czy_pelny():
         ilosc = self.z_magazyn.usun_ciecz(self.przeplyw)
         self.z_grzanie.dodaj_ciecz(ilosc)
         plynie_1 = True
      self.r_mg.ustaw_przeplyw(plynie_1)

      #grzanie->skraplanie->produkt
      plynie_2 = False
      if self.z_grzanie.czy_pelny():
         self.grzalka.grzej()
      if self.z_grzanie.czy_pusty():
         self.grzalka.nie_grzej()
      if not self.z_grzanie.czy_pusty() and not self.z_produkt.czy_pelny():
            if self.grzalka.praca:
               ilosc = self.z_grzanie.usun_ciecz(self.przeplyw)
               self.z_produkt.dodaj_ciecz(ilosc/2)
               self.z_odpad.dodaj_ciecz(ilosc/2)
               plynie_2 = True
      self.r_gs.ustaw_przeplyw(plynie_2)
      self.r_go.ustaw_przeplyw(plynie_2)
      self.skraplacz.skraplanie = plynie_2 

      self.update()
                
     

   def przyciski_kontoroli_recznej(self):
      ramka_guzikow = QFrame(self)
      ramka_guzikow.setGeometry(0,500,500,100)
      siatka_guzikow = QGridLayout()

      #guziki
      self.btn_start = QPushButton("START", self)
      self.btn_start.clicked.connect(self.uruchom)
      self.btn_stop = QPushButton("STOP", self)
      self.btn_stop.clicked.connect(self.zatrzymaj)
      self.btn_wyw_odp = QPushButton("wywoz ODPADOW", self)
      self.btn_wyw_odp.clicked.connect(self.wywiez_odpady)
      self.btn_wyw_prod = QPushButton("wywoz PRODUKTU", self)
      self.btn_wyw_prod.clicked.connect(self.wywiez_produkt)
      self.btn_uzup_magazyn = QPushButton("dostawa SUROWCA", self)
      self.btn_uzup_magazyn.clicked.connect(self.przywiez_surowiec)
      guziki = [self.btn_start, self.btn_stop, self.btn_wyw_odp, self.btn_wyw_prod, self.btn_uzup_magazyn]
      for btn in guziki:
         btn.setStyleSheet("background-color: #444; color: white;")

      # suwak zaworow
      self.opis_otw_zaw = QLabel("Otwarcie ZAWOROW: 100%", self)
      self.otwarcie_zaw = QSlider(Qt.Horizontal)
      self.otwarcie_zaw = QSlider(Qt.Horizontal)
      self.otwarcie_zaw.setMinimum(0)
      self.otwarcie_zaw.setMaximum(100)
      self.otwarcie_zaw.setValue(100)
      self.otwarcie_zaw.valueChanged.connect(self.aktualizuj_opis)
      self.otwarcie_zaw.valueChanged.connect(self.ustaw_zawory)

  
      # pakowanie guzikow i suwaka w siatke
      siatka_guzikow.addWidget(self.btn_start,1,1)
      siatka_guzikow.addWidget(self.btn_stop,2,1)
      siatka_guzikow.addWidget(self.opis_otw_zaw,1,2)
      siatka_guzikow.addWidget(self.otwarcie_zaw,2,2)
      siatka_guzikow.addWidget(self.btn_wyw_odp,1,3)
      siatka_guzikow.addWidget(self.btn_wyw_prod,2,3)
      siatka_guzikow.addWidget(self.btn_uzup_magazyn,1,4)
      # pakowanie siatki w ramkę
      ramka_guzikow.setLayout(siatka_guzikow)

   def aktualizuj_opis(self, value):   #aktualizacja opisu suwaka
     self.opis_otw_zaw.setText(f"Otwarcie: {value}%")
   def uruchom(self):   #uruchomienie symulacji
      if not self.pracuje:
         self.timer.start(20)
         self.pracuje = True
   def zatrzymaj(self): #zatrzymanie symulacji
      if self.pracuje:
         self.timer.stop()
         self.pracuje = False 
   def wywiez_odpady(self):
      self.z_odpad.usun_ciecz(100)
      self.update()
   def wywiez_produkt(self):
      self.z_produkt.usun_ciecz(100)
      self.update()
   def przywiez_surowiec(self):
      self.z_magazyn.dodaj_ciecz(100)
      self.update()
   def ustaw_zawory(self, wartosc):
      self.zaw_mg.ustaw(wartosc)
      self.zaw_go.ustaw(wartosc)
      self.zaw_gs.ustaw(wartosc)
      self.zaw_sp.ustaw(wartosc)
      self.update()



   def paintEvent(self, event):
      p = QPainter(self)
      p.setRenderHint(QPainter.Antialiasing)
      for r in self.rury:
          r.draw(p)
      for z in self.zbiorniki:
          z.draw(p)
      self.grzalka.draw(p)
      self.skraplacz.draw(p)
      for za in self.zawory:
          za.draw(p)
         
if __name__ == "__main__":
    app = QApplication(sys.argv)
    okno = Symulacja()
    okno.show()
    sys.exit(app.exec_())
