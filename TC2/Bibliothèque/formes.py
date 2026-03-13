import math

class Figure: 
    def __init__(self, x, y):
        self.__x = x 
        self.__y = y 
        self.__dessins = set()

    def get_x(self):
        return self.__x

    def get_y(self):
        return self.__y

    def get_pos(self):
        return (self.__x, self.__y)

    def set_pos(self, x, y):
        self.__x = x 
        self.__y = y 

    def translation(self, dx, dy):
        self.__x += dx
        self.__y += dy
    
    def __str__(self):
        return f"Figure(x={self.__x}, y={self.__y})"
    
    def ajouter_dessin(self, dessin):
        if dessin not in self.__dessins:
            self.__dessins.add(dessin)
            dessin.ajouter_forme(self) 

    def supprimer_dessin(self, dessin):
        if dessin in self.__dessins:
            self.__dessins.remove(dessin)
            dessin.supprimer_forme(self)

    def afficher_appartenance(self):
        noms = [d.nom for d in self.__dessins]
        print(f"Cette forme appartient aux dessins : {', '.join(noms) if noms else 'Aucun'}")

    def get_x(self): return self.__x
    def get_y(self): return self.__y
    def set_pos(self, x, y):
        self.__x = x
        self.__y = y

class Rectangle(Figure):
    def __init__(self, x, y, l, h):
        Figure.__init__(self, x, y)
        self.__l = l 
        self.__h = h 

    def get_dim(self): 
        return self.__l, self.__h

    def set_dim(self, l, h):
        self.__l = l 
        self.__h = h 

    def contient_point(self, px, py):
        return self.get_x() <= px <= self.get_x() + self.__l and \
               self.get_y() <= py <= self.get_y() + self.__h   

    def redimension_par_points(self, x0, y0, x1, y1):
        self.set_pos(min(x0, x1), min(y0, y1))
        self.__l = abs(x1 - x0)
        self.__h = abs(y1 - y0)

    def __str__(self):
        return f"Rectangle(x={self.get_x()}, y={self.get_y()}, l={self.__l}, h={self.__h})"

class Ellipse(Figure): 
    def __init__(self, x, y, rx, ry):
        Figure.__init__(self, x, y)
        self.__rx = rx
        self.__ry = ry

    def get_rayon(self):
        return self.__rx, self.__ry

    def set_rayon(self, rx, ry):
        self.__rx = rx
        self.__ry = ry

    def contient_point(self, px, py):
        if self.__rx == 0 or self.__ry == 0: 
            return px == self.get_x() and py == self.get_y()
        return ((px - self.get_x())**2 / self.__rx**2) + \
               ((py - self.get_y())**2 / self.__ry**2) <= 1
    
    def redimension_par_points(self, x0, y0, x1, y1):
        self.set_pos((x0 + x1) / 2, (y0 + y1) / 2)
        self.__rx = abs(x1 - x0) / 2
        self.__ry = abs(y1 - y0) / 2

    def __str__(self):
        return f"Ellipse(x={self.get_x()}, y={self.get_y()}, rx={self.__rx}, ry={self.__ry})"

class Cercle(Figure): 
    def __init__(self, x, y, r):
        Figure.__init__(self, x, y)
        self.__r = r

    def get_rayon(self):
        return self.__r

    def set_rayon(self, r):
        self.__r = r 

    def contient_point(self, px, py):
        return (px - self.get_x())**2 + (py - self.get_y())**2 <= self.__r**2

    def redimension_par_points(self, x0, y0, x1, y1):

        diametre = min(abs(x1 - x0), abs(y1 - y0))
        self.__r = diametre / 2
        
        signe_x = 1 if x1 >= x0 else -1
        signe_y = 1 if y1 >= y0 else -1
        
        nx = x0 + (signe_x * self.__r)
        ny = y0 + (signe_y * self.__r)
        self.set_pos(nx, ny)

    def __str__(self):
        return f"Cercle(x={self.get_x()}, y={self.get_y()}, r={self.__r})"
    
class Dessin:
    def __init__(self, nom):
        self.nom = nom
        self.__formes = [] 

    def ajouter_forme(self, forme):
        if forme not in self.__formes:
            self.__formes.append(forme)
            forme.ajouter_dessin(self) 

    def supprimer_forme(self, forme):
        if forme in self.__formes:
            self.__formes.remove(forme)
            forme.supprimer_dessin(self) 

    def afficher_contenu(self):
        print(f"--- Contenu du dessin '{self.nom}' ---")
        if not self.__formes:
            print("Vide.")
        for i, forme in enumerate(self.__formes):
            print(f"{i+1}. {forme}")