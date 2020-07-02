import numpy as np
import random
import math

# On a utilisé les indices à partir de 1 afin de garder la signification des indices ( l'indice (1,1)-> obtenir 1 point en jettant 1 dès) 
def P(d):
    # déclaration des deux matrices p et q
    # k a une valeur maximale de 6*d 
    p=np.zeros((d+1,6*d+1))
    q=np.zeros((d+1,6*d+1))
    
    #intialisation p
    # en utilisant un dè toutes les surfaces sont équiprobales
    p[1,2:7]=1/6
    
    # la probabilité qu'au moins un dè tombe sur 1
    for i in range(1,d+1):
        p[i,1]=1-((5/6)**i)
    
    
    #initialisation q
    #  en utilisant un dè et sachant que le dè n'a pas tombé sur 1 , toutes les autres surfaces sont équiprobales
    q[1,2:7]=1/5
    
    #remplissage des matrices en utilisant la formule de réccurence    
    for i in range(2,d+1):
        for j in range( 2*i , 6*i+1):
            # exctaction du tableau des valeurs concernées par la réccurence
            indices=np.arange(j-6,j-1)
            indices=np.extract(indices>1, indices)
            q[i,j]=q[i-1,indices].sum()/5
            p[i,j]=q[i,j]*((5/6)**i)
    return p

# calcule l'espérance du nombre de points si on utilise d dès à chaque tour
def espAveugle(d):
    return ((4*d-1)*((5/6)**d))+1

# calclue la valeur de D qui maximise l'espérance du nombre de points
def maxD (D):
    # on intialise le maximum à 0 
    maxEsp=0  
    # pour chaque d entre 1 et D on calcule l'espérance
    for i in range (1,D+1):
        # si cette espérance est superieure à l'espérance maximale on met à jour l'espérance maximale 
        #et on garde le d associé
        if (espAveugle(i) > maxEsp):
            maxEsp=espAveugle(i)
            maxInd=i
    return maxInd 


# la stratégie aveugle renvoi la valeur de D optimale
def strategieAveugle(N,D):
    return maxD(D)

# calcule la matrice des espérances des gains pour D et N données, VERSION ITÉRATIVE 
def espDynamiqueRec(i,j,N,D,memo):
    # les cas de bases:
    # si la valeur est déja calculée on la renvoie
    if (not math.isnan(memo[i,j][0])):
        return memo[i,j]
    # si le joueur 1 a déja gagné
    if(i>=N and i>=j):
        return (1,1)
    # si le joueur 2 a déja gagné
    if (j>=N and j>i):
        return (-1,1)
    
    # on calcule la matrice des probabilté qu'on gagne k points en jettant d dès 
    p=P(D)
    
    #on initialise le gain minimal à + infinie
    gainMinimal=math.inf
    # pour tous les d de 1 à D on calcule le gain
    for d in range(1,D+1):
        gain=0
        for k in range(1,6*D+1):
            gain+=p[d,k]*espDynamiqueRec(j,i+k,N,D,memo)[0]
        # si le gain calculé est meilleur que le gain minimal alors on met à jour le gain minimal et on garde le d associé
        if (gain<gainMinimal):
            gainMinimal=gain
            dopt=d
    memo[i,j]=(-gainMinimal,dopt)
    return (-gainMinimal,dopt)


# la stratégie optimal renvoi la valeur de D optimale
def strategieOptimale(N,D):
    # la matrice memo contient les valeur déja calculées
    memo = np.empty((N+6*D,N+6*D,2))
    # la matrice res contient le d optimal pour chaque état (i,j)
    res=np.empty((N+1,N+1))
    # initialisons les valeurs à nan pour qu'on soit sur qu'on utilise pas des valeurs interdites 
    memo[:]=np.nan
    res[:]=np.nan
    
    #on remplit la matrice des d optimaux 
    for i in range(N,-1,-1):
        for j in range(N,-1,-1): 
            res[i,j]=espDynamiqueRec(i,j,N,D,memo)[1]
    return res


def strategieAleatoire(N,D):
    return random.randint(1,D)

def strategieGourmande(N,D):
    return D

#Dictionnaire des stratégies déja implémantées
strategies = {"aveugle" :strategieAveugle,
           "optimale" : strategieOptimale,
           "aleatoire" : strategieAleatoire,
              "gourmande": strategieGourmande
}

#Jouer contre l'ordinateur
N = input("Entrez N : \n")
D = input("Entrez D : \n")
N = int(N)
D = int(D)
ordre = input("si vous voulez jouer le premier entrez 1 , 2 sinon \n")
st1 = input("entrez la stratégie de l'ordinateur (vous pouvez choisir entre 'optimale','aveugle','aleatoire' et 'gourmande') \n")
# le gain de joueur 1 initialement = 0
g1=0
# le gain de joueur 2
g2=0

# calcule des paramètres nécessaires pour chaque stratégie
strategiePc=strategies[st1](N,D)

# tantque aucun joueur n'a arrivé à N , donc personne n'a gagné
while((g1<N)and(g2<N)):
    print("votre gain est :",g1 if ordre=="1" else g2," ,le gain de l'ordinateur est :",g2 if ordre=="1" else g1)
    if (ordre=="1"):
        # on calcule d en utilisant la stratégie  correspondante pour le joueur 1
        d1 = input("entrez le nombre de dès à lancer \n")
        # on tire aléatoirement d1 valeurs entre 1 et 6
        res1=np.random.randint(1,7,int(d1))
        print("les ",d1," dès sont tombés sur :", res1)
        # s'il existe un dès à 1 le gain est incrémenté de 1 , sinon le gain est augmenté de la somme des valeurs tirée
        g1= (g1+1) if (res1.min()==1) else (g1+res1.sum())
        # si le joueur 1 arrive à N on sort ( c'est bon il a gagné)
        print("maintenant vous avez",g1," points")
        if (g1>=N):
            break
        # on calcule d en utilisant la stratégie  correspondante pour le joueur 1
        d2 = strategiePc if st1!="optimale" else strategiePc[g2,g1] 
        
        # on tire aléatoirement d2 valeurs entre 1 et 6
        res2=np.random.randint(1,7,int(d2))
        # s'il existe un dès à 1 le gain est incrémenté de 1 , sinon le gain est augmenté de la somme des valeurs tirée
        g2=  (g2+1) if (res2.min()==1) else (g2+res2.sum())
        print("l'ordinateur a lancé ",d2," dès, et ils sont tombés sur :",res2," il a maintenant ",g2," points")
    else:
        d1=strategiePc if st1!="optimale" else strategiePc[g2,g1] 
        
        # on tire aléatoirement d2 valeurs entre 1 et 6
        res1=np.random.randint(1,7,int(d1))
        # s'il existe un dès à 1 le gain est incrémenté de 1 , sinon le gain est augmenté de la somme des valeurs tirée
        g1=  (g1+1) if (res1.min()==1) else (g1+res1.sum())
        print("l'ordinateur a lancé ",d1," dès, et ils sont tombés sur :",res1," il a maintenant ",g1," points")
        if (g1>=N):
            break
        # on calcule d en utilisant la stratégie  correspondante pour le joueur 1
        d2 = input("entrez le nombre de dès à lancer \n")
        # on tire aléatoirement d1 valeurs entre 1 et 6
        res2=np.random.randint(1,7,int(d1))
        print("les ",d2," dès sont tombés sur :", res2)
        # s'il existe un dès à 1 le gain est incrémenté de 1 , sinon le gain est augmenté de la somme des valeurs tirée
        g2= (g2+1) if (res2.min()==1) else (g2+res2.sum())
        # si le joueur 1 arrive à N on sort ( c'est bon il a gagné)
        print("maintenant vous avez",g2," points")

       

# si c'est le joueur 1 qui gagné alors on ajoute 1 dans sa trace et -1 dans la trace du joueur 2
if (g1>=N):
    if(ordre=="1"):
        print("vous avez gagner contre l'ordinateur ",g1," a ",g2)
    else:
        print("l'ordinateur a gagné contre vous  ",g1," a ",g2)
# si c'est le joueur 2 qui gagné alors on ajoute 1 dans sa trace et -1 dans la trace du joueur 1
else:
    if(ordre=="2"):
        print("vous avez gagner contre l'ordinateur ",g2," a ",g1)
    else:
        print("l'ordinateur a gagné contre vous  ",g2," a ",g1)
