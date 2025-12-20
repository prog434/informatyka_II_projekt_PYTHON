# informatyka_II_projekt_PYTHON
wizualizacja procesu przemysłowego "SCADA"


I etap - plany i założenia:
  symulacja procesu destylacji, wizualizacja będzie zawierać:
    1)ekran głowny, a na nim (jako odrębne obiekty w kodzie):
      - 4 zbiorniki (magazynowanie, proces, odpady, produkt)
      - grzałka w zbiorniku pracy
      - zawory pomiędzy zbiornikami
      - panel z przyciskami itp. (start, stop, ustawianie temperatury, wywóz odpadów)
      - przyciski przejscia do innych ekranów
    2)ekran błędów 
      - lista komunikatów błędów, np. jak ktoś uruchomi proces podgrzewania bez substancji
      - pewnie zapis w pliku json 
      - może jakiś przycisk reset
      - przyciski przejscia do innych ekranów
    3)ekran raportów 
      - lista co i kiedy udało się wyprodukować, ile wywieziono odpadów
      - pewnie zapis w pliku json
      - może jakiś przycisk reset, ewentualnie edycji ręcznej danych
      - przyciski przejscia do innych ekranów
