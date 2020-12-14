import random
mazo=[(1,"oros",1),(1,"copas",1),(1,"bastos",1),(1,"espadas",1),(2,"oros",2),(2,"copas",2),(2,"bastos",2),(2,"espadas",2),
(3,"oros",3),(3,"copas",3),(3,"bastos",3),(3,"espadas",3),(4,"oros",4),(4,"copas",4),(4,"bastos",4),(4,"espadas",4),
(5,"oros",5),(5,"copas",5),(5,"bastos",5),(5,"espadas",5),(6,"oros",6),(6,"copas",6),(6,"bastos",6),(6,"espadas",6),
(7,"oros",7),(7,"copas",7),(7,"bastos",7),(7,"espadas",7),(11,"oros",0.5),(11,"copas",0.5),(11,"bastos",0.5),
(11,"espadas",0.5),(12,"oros",0.5),(12,"copas",0.5),(12,"bastos",0.5),(12,"espadas",0.5)]

flag_ejemplo=False
flag_ronda = False
flag_turno = False
njug = 0
mano = 0
apuesta = 0
jugadores=[]
jugadoresOrden= []
dicc = {}
mazo2 = mazo.copy()
pasada = False
max_prioridad = 0
ganador = None
while not flag_ejemplo:
  njug = int(input("Cuantos jugadores participaran?\n"))
  if njug<2:
      print("El numero es demasiado pequeño. Introduce otra cantidad.")
      njug = int(input("Cuantos jugadores participaran?\n"))
  if njug>8:
      print("Demasiados jugadores! Introduce otra cantidad")
      njug = int(input("Cuantos jugadores participaran?\n"))
  if njug>=2 and njug<=8:
      print(f"Empezando partida con {njug} jugadores")
      max_prioridad = njug - 1
      for i in range (njug):
          nombrecorrecto=False
          while not nombrecorrecto:
              nombre=str(input(f"Nombre del jugador {i+1}: "))
              while nombre in jugadoresOrden:
                  print("Nombre de jugador ya existe,inserta otro")
                  nombre = str(input(f"Nombre del jugador {i + 1}: "))
              for x in nombre:
                  if x.isspace() == True:
                      print("Tiene espacios")
                      break
              if nombre[0].isalpha() and nombre.isalnum():
                  jugadoresOrden.append(nombre)
                  nombrecorrecto=True
              elif not nombre.isalnum():
                  print("No es alfanumerico")
                  continue
              elif not nombre[0].isalpha():
                  print("El primer caracter no es una letra")
                  continue
      flag_ejemplo = True
  print(jugadores)
  print(jugadoresOrden)

while flag_ejemplo:
    if mano < 30:
        mano += 1
        if mano == 1:
            dicc = {}
            mazo2 = mazo.copy()
            for i in range(len(jugadoresOrden)):
                carta = random.choice(mazo2)
                mazo2.pop(mazo2.index(carta))
                dicc[jugadoresOrden[i]] = carta
            print(dicc)

            for k in range(len(jugadoresOrden)):
                pasada = False
                for j in range(1, len(jugadoresOrden) - k):
                    if dicc[jugadoresOrden[j]][0] > dicc[jugadoresOrden[j - 1]][0]:
                        pasada = True
                        jugadoresOrden[j], jugadoresOrden[j - 1] = jugadoresOrden[j - 1], jugadoresOrden[j]
                if pasada == False:
                    break

            for k in range(len(jugadoresOrden)):
                for j in range(len(jugadoresOrden) - 1):
                    if dicc[jugadoresOrden[j]][0] == dicc[jugadoresOrden[j + 1]][0] and mazo.index(dicc[jugadoresOrden[j]]) > mazo.index(dicc[jugadoresOrden[j + 1]]):
                        jugadoresOrden[j], jugadoresOrden[j + 1] = jugadoresOrden[j + 1], jugadoresOrden[j]

            for prioridad in range(len(jugadoresOrden)):
                jugadores.append({jugadoresOrden[prioridad]: [[], "jugando", "jugando", prioridad, 0, 0, 20, 0]})
            print(f"\nEl jugador {jugadoresOrden[0]} es la banca")
            print(jugadoresOrden)
            print(jugadores)

        mazo2 = mazo.copy()
        for i in range(len(jugadoresOrden)):
            jugadores[i][jugadoresOrden[i]][0].clear()
            if jugadores[i][jugadoresOrden[i]][2] == "jugando":
                carta = random.choice(mazo2)
                mazo2.pop(mazo2.index(carta))
                jugadores[i][jugadoresOrden[i]][0].append(carta)
                jugadores[i][jugadoresOrden[i]][4] = carta[2]
        print(jugadoresOrden)
        print(jugadores)

        for i in range(1, len(jugadores)):
            nombreJugador = jugadores[i].keys()
            if jugadores[i][jugadoresOrden[i]][1] == "jugando" and jugadores[i][jugadoresOrden[i]][2] == "jugando":
                jugadores[i][jugadoresOrden[i]][-1] = mano
                print("\nLas cartas: ", end="")
                for j in mazo:
                    if j not in mazo2:
                        print(j[0], " de ", j[1], end=", ")
                print(" han salido\n")
                for k in range(1, len(jugadores)):
                    if jugadores[k][jugadoresOrden[k]][1] != "eliminado":
                        print(f"{jugadoresOrden[k]} tiene {jugadores[k][jugadoresOrden[k]][-2]} puntos y su apuesta son {jugadores[k][jugadoresOrden[k]][-3]} puntos\n")
                print("Juega ", jugadoresOrden[i])
                print(f"\nTiene {jugadores[i][jugadoresOrden[i]][0][0][0]} de {jugadores[i][jugadoresOrden[i]][0][0][1]} \n")
                apuestaCorrecta = False
                while not apuestaCorrecta:
                    apuesta = int(input("Cuantos puntos quiere apostar?: "))
                    if apuesta < 1:
                        print("La apuesta es demasiado baja")
                    elif apuesta > jugadores[i][jugadoresOrden[i]][-2]:
                        print("No puede apostar más puntos de los que tiene")
                    else:
                        jugadores[i][jugadoresOrden[i]][-3] = apuesta
                        jugadores[i][jugadoresOrden[i]][-2] = jugadores[i][jugadoresOrden[i]][-2] - apuesta
                        apuestaCorrecta = True
                accion = 0
                while accion != 2:
                    accion = int(input("\nQue quiere hacer? \n1) Pedir carta \n2) Plantarse \n"))
                    if accion == 1:
                        carta = random.choice(mazo2)
                        mazo2.pop(mazo2.index(carta))
                        jugadores[i][jugadoresOrden[i]][0].append(carta)
                        jugadores[i][jugadoresOrden[i]][3] += carta[2]
                        print("Sus cartas son:")
                        for h in jugadores[i][jugadoresOrden[i]][0]:
                            print(f"{h[0]} de {h[1]}")
                    elif accion == 2:
                        if jugadores[i][jugadoresOrden[i]][3] <= 7.5:
                            jugadores[i][jugadoresOrden[i]][1] = "plantado"
                        else:
                            jugadores[i][jugadoresOrden[i]][1] = "eliminado"
                            jugadores[0][jugadoresOrden[0]][-2] += jugadores[i][jugadoresOrden[i]][-3]
                            print(f"El jugador {jugadoresOrden[i]} esta eliminado de la ronda")
                        print(jugadores)
        flag_banca = False
        for n in range(1, len(jugadoresOrden)):
            if jugadores[n][jugadoresOrden[n]][1] == "plantado":
                flag_banca = True
                break
        if flag_banca == True:
            print("\nLas cartas: ", end="")
            for j in mazo:
                if j not in mazo2:
                    print(j[0], " de ", j[1], end=", ")
            for k in range(1, len(jugadores)):
                if jugadores[k][jugadoresOrden[k]][1] != "eliminado":
                    print(f"{jugadoresOrden[k]} tiene {jugadores[k][jugadoresOrden[k]][-2]} puntos y su apuesta son {jugadores[k][jugadoresOrden[k]][-3]} puntos\n")
            print("Juega la banca\n")
            accion = 0
            while accion != 2:
                accion = int(input("\nQue quiere hacer? \n1) Pedir carta \n2) Plantarse \n"))
                if accion == 1:
                    carta = random.choice(mazo2)
                    mazo2.pop(mazo2.index(carta))
                    jugadores[0][jugadoresOrden[0]][0].append(carta)
                    jugadores[0][jugadoresOrden[0]][3] += carta[2]
                    print("Sus cartas son:")
                    for h in jugadores[0][jugadoresOrden[0]][0]:
                        print(f"{h[0]} de {h[1]}")

                elif accion == 2:
                    cont = 0
                    for n in range(1, len(jugadores)):
                        if jugadores[0][jugadoresOrden[0]][4] > 7.5 or (jugadores[0][jugadoresOrden[0]][4] < 7.5 and jugadores[n][jugadoresOrden[n]][4]>jugadores[0][jugadoresOrden[0]][4]):
                            if jugadores[n][jugadoresOrden[n]][2] == "jugando":
                                if jugadores[n][jugadoresOrden[n]][4] < 7.5:
                                    recompensa = jugadores[n][jugadoresOrden[n]][-3]
                                    if jugadores[0][jugadoresOrden[0]][-2] - recompensa < 0:
                                        recompensa = jugadores[0][jugadoresOrden[0]][-2]
                                        jugadores[n][jugadoresOrden[n]][-2] += recompensa
                                        jugadores[0][jugadoresOrden[0]][-2] -= recompensa
                                    else:
                                        jugadores[n][jugadoresOrden[n]][-2] += recompensa * 2
                                        jugadores[0][jugadoresOrden[0]][-2] -= recompensa
                                    print(f"Banca paga al jugador {jugadoresOrden[n]} {recompensa} puntos")
                                elif jugadores[n][jugadoresOrden[n]][4] == 7.5:
                                    recompensa = jugadores[n][jugadoresOrden[n]][-3]
                                    if jugadores[0][jugadoresOrden[0]][-2] - recompensa < 0:
                                        recompensa = jugadores[0][jugadoresOrden[0]][-2]
                                        jugadores[n][jugadoresOrden[n]][-2] += recompensa
                                        jugadores[0][jugadoresOrden[0]][-2] -= recompensa
                                    else:
                                        jugadores[n][jugadoresOrden[n]][-2] += recompensa * 3
                                        jugadores[0][jugadoresOrden[0]][-2] -= recompensa * 2
                                    if cont == 0:
                                        jugadores[0][jugadoresOrden[0]][3] = max_prioridad + 1
                                        jugadores[n][jugadoresOrden[n]][3] = 0
                                        cont += 1
                                    print(f"Banca paga al jugador {jugadoresOrden[n]} {recompensa} puntos y el jugador {jugadoresOrden[n]} pasa a ser la banca")
                        elif jugadores[0][jugadoresOrden[0]][4] == 7.5:
                            if jugadores[n][jugadoresOrden[n]][4] <= 7.5:

                             jugadores[0][jugadoresOrden[0]][-2] += jugadores[n][jugadoresOrden[n]][-3]

            if jugadores[0][jugadoresOrden[0]][3] != 0:
                for s in range(len(jugadores)):
                    pasada = False
                    for g in range(1, len(jugadores) - s):
                        if jugadores[g][jugadoresOrden[g]][3] < jugadores[g-1][jugadoresOrden[g-1]][3]:
                            pasada = True
                            jugadores[g], jugadores[g-1] =  jugadores[g-1],  jugadores[g]
                            jugadoresOrden[g], jugadoresOrden[g-1] = jugadoresOrden[g-1], jugadoresOrden[g]
                    if pasada == False:
                        break
            for d in range(len(jugadores)):
                jugadores[d][jugadoresOrden[d]][4] = 0
                jugadores[d][jugadoresOrden[d]][5] = 0

            continuan = 0
            for q in range(len(jugadores)):
                if jugadores[q][jugadoresOrden[q]][-2] == 0:
                    continuan += 1
                    jugadores[q][jugadoresOrden[q]][2] = "eliminado"
                    jugadores[q][jugadoresOrden[q]][1] = "eliminado"
                    print(f"El jugador {jugadoresOrden[q]} está eliminado de la partida")
                else:
                    continuan += 1
                    ganador = jugadoresOrden[q]
            if continuan == 1:
                break

        else:
            print("Ha ganado la banca")
            jugadores[0][jugadoresOrden[0]][-1] = mano
            for a in range(1, len(jugadores)):
                jugadores[0][jugadoresOrden[0]][-2] += jugadores[a][jugadoresOrden[a]][-3]
                jugadores[a][jugadoresOrden[a]][-3] = 0
    else:
        ganador = jugadoresOrden[0]
        for s in range(len(jugadores)):
            if jugadores[s][jugadoresOrden[s]][2] == "jugando" and jugadores[s][jugadoresOrden[s]][-2] > jugadores[s][ganador][-2]:
                ganador = jugadoresOrden[s]
print(f"\nHa ganado el jugador {ganador}!!!")