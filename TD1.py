import random
import re

#k = int(input("Entree le nombre souhaiter :  "))

# if k % 2 == 0:
#     print("Le nombre est pair")
# else:    print("Le nombre est impair")

#VI-2
def quadratique(a,b,c):
    delta = b**2 - 4*a*c
    if delta < 0:
        print("Pas de solution reelle")
    elif delta == 0:
        x = -b / (2*a)
        print("Une solution reelle : ", x)
    else:
        x1 = (-b + delta**0.5) / (2*a)
        x2 = (-b - delta**0.5) / (2*a)
        print("Deux solutions reelles : ", x1, "et", x2)

#VI-3
def moyenne(liste):
    return (sum(liste)/len(liste))

def ecart_type(liste):
    moy = moyenne(liste)
    variance = sum((x - moy) ** 2 for x in liste) / len(liste)
    return variance ** 0.5

echantillon=[random.gauss(16,2) for n in range(100)]    
print("Moyenne : ", moyenne(echantillon))
print("Ecart type : ", ecart_type(echantillon))

#VI-4
def variance(liste):
    moy = moyenne(liste)
    for i in liste:
        i**2
    moy_2 = moyenne(liste)
    var = abs(moy_2-(moy**2))
    return var 

#print(variance(echantillon)**0.5)*

#IX-2 

def convertir(S = str) : 
    if S.isdigit() == True : 
        s = int(S)
        return print('Methode 1',s) 
    else: 
        if S[0] == '-':
            s = re.sub('-','',S)
            s = int(S)
            return (s)


S = '-351'
#print(convertir(S))



min=max=0
val=input("donner le premier entier ")
try :
    val=int(val)
    min=max=val
    except ValueError : #On vient ici si on n’a pas donné un entier
    print("Fallait donner un entier")
    input("Taper sur entrée pour fermer la fenetre et quitter.")
    exit(0)
    # Ici, on a lu un entier et initialisé min et max
    while True:
        try :
            val=input("donner un entier ")
            val=int(val)
            if (val < min) :
                min=val
            if val > max :
                max=val
        except ValueError : #On vient ici si on n’a pas donné un entier
            print("Il faut donner des entiers")
            exit(0)
except EOFError: #On vient ici si on a fait CTRL-D (ou CTRL-Z) DANS un "terminal"
    print("c’est fini : min =",min, " max = ", max)
        break
input("pour ne pas fermer la fenetre de suite ..")