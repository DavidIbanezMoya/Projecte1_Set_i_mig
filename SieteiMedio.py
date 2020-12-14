import random
mazo=[(1,"oros",1),(1,"copas",1),(1,"bastos",1),(1,"espadas",1),(2,"oros",2),(2,"copas",2),(2,"bastos",2),(2,"espadas",2),
(3,"oros",3),(3,"copas",3),(3,"bastos",3),(3,"espadas",3),(4,"oros",4),(4,"copas",4),(4,"bastos",4),(4,"espadas",4),
(5,"oros",5),(5,"copas",5),(5,"bastos",5),(5,"espadas",5),(6,"oros",6),(6,"copas",6),(6,"bastos",6),(6,"espadas",6),
(7,"oros",7),(7,"copas",7),(7,"bastos",7),(7,"espadas",7),(11,"oros",0.5),(11,"copas",0.5),(11,"bastos",0.5),
(11,"espadas",0.5),(11,"oros",0.5),(11,"copas",0.5),(11,"bastos",0.5),(11,"espadas",0.5),(12,"oros",0.5),(12,"copas",0.5),
(12,"bastos",0.5),(12,"espadas",0.5)]

flag_ejemplo=True
jugadores=[]
nombrecorrecto=True
puntos = 20
mano = 0
while flag_ejemplo==True:
  njug = int(input("Cuantos jugadores participaran?\n"))
  if njug<2:
      print("El numero es demasiado pequeño. Introduce otra cantidad.")
      njug = int(input("Cuantos jugadores participaran?\n"))
  if njug>8:
      print("Demasiados jugadores! Introduce otra cantidad")
      njug = int(input("Cuantos jugadores participaran?\n"))
  if njug>=2 and njug<=8:
      print(f"Empezando partida con {njug} jugadores")
      for i in range (njug):
          nombrecorrecto=False
          while nombrecorrecto==False:
              nombre=str(input(f"Nombre del jugador {i + 1}: "))
              while nombre in jugadores:
                  print("Nombre de jugador ya existe,inserta otro")
                  nombre = str(input(f"Nombre del jugador {i + 1}: "))
              for x in nombre:
                  if x.isspace() == True:
                      print("Tiene espacios")
                      break
              if nombre[0].isalpha() and nombre.isalnum():
                  jugadores.append(nombre)
                  nombrecorrecto=True
              elif not nombre.isalnum():
                  print("No es alfanumerico")
                  continue
              elif not nombre[0].isalpha():
                  print("El primer caracter no es una letra")
                  continue
  print(jugadores)
  flag_ejemplo = False
prioridad = 0
dicc = {}
jugadoresOrden= []
mazo2 = mazo.copy()
for i in range(len(jugadores)):
   carta = random.choice(mazo2)
   mazo2.pop(mazo2.index(carta))
   dicc[jugadores[i]]= carta

print(dicc)
for i in dicc:
    jugadoresOrden.append(i)
    cartaMax = i[0]

for k in range(len(jugadoresOrden)):
    for j in range(len(jugadoresOrden)-1):
        if dicc[jugadoresOrden[j]][0] < dicc[jugadoresOrden[j+1]][0]:
            jugadoresOrden[j],jugadoresOrden[j+1] = jugadoresOrden[j+1],jugadoresOrden[j]
        elif dicc[jugadoresOrden[j]][0] == dicc[jugadoresOrden[j+1]][0]:
            print()
print(jugadoresOrden)
diccJug= {}
cartas = []
info = [cartas]
for jugador in range(len(jugadoresOrden)):
    #diccJug[jugadoresOrden[jugador]] =[[dicc[jugadoresOrden[jugador]]],"jugando","jugando",jugador,dicc[jugadoresOrden[jugador]][2],0,puntos,mano]
    diccJug[jugadoresOrden[jugador]] =[[],"jugando","jugando",jugador,0,0,puntos,mano]
print(diccJug)
