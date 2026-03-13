from TD3 import *

l = Livre('Le Pere Goriot','Honore de Balzac',101,2)
print(l)

l.set_auteur("Emilie Bronte")
print(l.get_auteur())
    
l.set_titre("Les Hauts de Hurlevent")
print(l.get_titre())
    
l.set_numero(102)
print(l.get_numero())

l.set_nb_total(5)
print(l.get_nb_total())

l.set_nb_dispo(4)
print(l.get_nb_dispo())

print(l)
