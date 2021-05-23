# Cryptage RSA
# Codeur: Emett    
print("                           __                           __                                   ")
print("   ____    _____  ____    / /_   ____   ____   ____    / /   __        _____   ___   ____    ")
print("  / __ \  / ___/ / __ \  / ___/ / __ \ / ___\ / __ \  / /  / _ \      / ___/  /  _\ / __ \   ")
print(" / ____/ / /    / /_/ / / /    / /_/ // /___ / /_/ / / /  /  __/     / /     _\  \ / /_/  \  ")
print("/_/     /_/     \____/ /_/     \____/ \____/ \____/ /_/   \___/     /_/      \___/ \____/\_\ ")
print("_____________________________________________________________________________________________")

from random import randint
from math import log

def fichier_nombres_premiers():
   mon_fichier = open("nombres_premiers.txt", "r")
   contenu = mon_fichier.read()
   liste_nombres_premiers = list(map(int,contenu.split(", ")))
   mon_fichier.close()
   return liste_nombres_premiers
def fichier_Phi():
   mon_fichier = open("Phi.txt", "r")
   contenu = mon_fichier.read()
   nombre_Phi = list(map(int,contenu.split(", ")))
   mon_fichier.close()
   return nombre_Phi
def pgcd(a,b):
    return a if b%a == 0 else pgcd(b,a%b)
def phi(n):
   # phi(n) = Prod_{p|n} 1 - (1/p) avec p facteur premier de n
   if n<1000000: Phi = Nombres_phi[n]
   else : 
      Phi,d = n,n
      for p in Nombres_premiers:
         if d%p == 0:
            while d%p == 0: d /= p
            Phi *= 1 - (1/p)
            if d == 1: break
   return int(Phi)

Nombres_premiers = fichier_nombres_premiers()
Nombres_phi = fichier_Phi()

def Cryptage_RSA_1(p,q):
    # N = p*q  et n = (p-1)*(q-1)
    N, n = p*q, (p-1)*(q-1)
    return N,n

def Cryptage_RSA_2(n):
    # pgcd(c,n) = 1
    for i in range(3,n,2):
        if pgcd(i,n) == 1:
            c = i
            break
    return c
def Cryptage_RSA_3(n,c):
    # c*d = 1[n]
    for k in range(0,c):
        if k*n % c == c-1:
            d = (1 + k*n)//c
            break
    return d

def Casseur_RSA(N,c):
    #n = phi(N)
    n = phi(N)
    return Cryptage_RSA_3(n,c)

def Encryptage(N,c,a):
    # a^c = b[N]
    return a**c % N
def Decryptage(N,d,b):
    #b^d = a[N]
    return b**d % N
   
def Encryptage_2(N,c,a):
    A = a
    for i in range(c-1):
       a = a*A % N
    return a 
def Decryptage_2(N,d,b):
    B = b
    for i in range(d-1):
       b = b*B % N
    return b
   
def Encryptage_3(N,c,a):
    A = a
    Cycle,cycle = False, 0
    for i in range(c-1):
       a = a*A % N
       if a == 1:
          if cycle == 0: cycle = i
          elif cycle != 0:
             Cycle,cycle = True, i-cycle
             break
    if Cycle:
       for _ in range((c-cycle) % c): a = a*A % N
    return a 
def Decryptage_3(N,d,b):
    B = b
    Cycle,cycle = False, 0
    for i in range(d-1):
       b = b*B % N
       if b == 1:
          if cycle == 0: cycle = i
          elif cycle != 0:
             Cycle,cycle = True, i-cycle
             break
    if Cycle:
       for _ in range((d-cycle) % d): b = b*B % N
    return b
   
def Cryptage_Texte(texte):
   nb_texte = 0
   for i,lettre in enumerate(texte):
      nb_texte += ((ord(lettre)-ord(" "))*100**i)
   return nb_texte
def Decryptage_Texte(nb_texte):
   texte, nb_texte=[], str(nb_texte)
   if len(nb_texte)%2==1: nb_texte = "0" + nb_texte
   for i in range(len(nb_texte)//2):
      texte.append(chr(int(nb_texte[i*2])*10+int(nb_texte[i*2+1])+ord(" ")))
   texte = "".join(texte[::-1])
   return texte

alphabet = "azertyuiopqsdfghjklmwxcvbn1234567890AZERTYUIOPQSDFGHJKLMWXCVBN,;:!?./*^<>&é(-è_çà)=+=² #|[`\^@]"

def Cryptage_Texte_2(texte):
   nb_texte = 0
   for i,lettre in enumerate(texte):
      nb_texte += ((alphabet.index(lettre))*100**i)
   return int(nb_texte)
def Decryptage_Texte_2(nb_texte):
   texte, nb_texte=[], str(nb_texte)
   if len(nb_texte)%2==1: nb_texte = "0" + nb_texte
   for i in range(len(nb_texte)//2):
      texte.append(alphabet[int(nb_texte[i*2])*10+int(nb_texte[i*2+1])])
   texte = "".join(texte[::-1])
   return texte

def main():
    print("----Protocole RSA------")
    MIN, MAX = 1000, 2000
    ip,iq = randint(MIN,MAX),randint(MIN,MAX)
    p,q = Nombres_premiers[ip], Nombres_premiers[iq]
    N,n = Cryptage_RSA_1(p,q)
    c = Cryptage_RSA_2(n)
    d = Cryptage_RSA_3(n,c)
    print(Casseur_RSA(N,c))
    print("N:",N,"n:",n,"p:",p,"q:",q, "Nb lettres:", int( log(N) / (2*log(10)) ) )
    print("c:",c,"d:",d)
    texte = input("Texte: ")
    a = Cryptage_Texte_2(texte)
    print("a:",a)
    b = Encryptage_3(N,c,a)
    a = Decryptage_3(N,d,b)
    print("a:",a,"b:",b)
    print("Texte :",Decryptage_Texte_2(a))
    print("-----------------------")
    print("")
while 1 :main()
