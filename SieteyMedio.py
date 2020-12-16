import pymysql
import random
import xml.etree.ElementTree as ET

# Conexión de base de datos.
conexion = "database-1.cg7nvcimoijq.us-east-1.rds.amazonaws.com"  # aquí pondremos nuestra dirección de la base de datos de Amazon web services
usuario = "nacho"  # usuario de la conexión
password = "lutetalos99"  # contraseña
BBDD = "proyecto"  # base de datos a la cual nos vamos a conectar
db = pymysql.connect(conexion, usuario, password, BBDD)
##################################################
query_sql = ""
def query(outfileName,query_sql):
    print("Mostrando consulta:")
    with open(outfileName, "w") as outfile:
        db = pymysql.connect(conexion, usuario, password, BBDD)
        cursor = db.cursor()
        cursor.execute(query_sql)
        rows = cursor.fetchall()
        for index in range(len(cursor.description)):
            print(str(cursor.description[index][0]).ljust(24),end=" ")
        print()
        for row in rows:
            for data in row:
                print(str(data).ljust(24),end=" ")
            print()

#Configuración del juego
tree = ET.parse("Basic_Config_Game.xml")
root = tree.getroot()
Min_Jugadores = int(root.find("Num_Min_Players").text)
Max_Jugadores = int(root.find("Num_Max_Players").text)
Max_Rondas = int(root.find("Num_Max_Rounds").text)
Puntos_Iniciales = int(root.find("Num_Initial_Points").text)

#Generación del mazo
mazo = []
tree2 = ET.parse("xml_cartas.xml")
root2 = tree2.getroot()
for i in range(1, 13):
    for carta in root2.iter("carta"):
        valor = int(carta.find("valor").text)
        palo = carta.find("palo").text
        valor_juego = float(carta.find("valor_juego").text)
        activa = carta.find("activa").text
        if valor_juego != 0.5:
            valor_juego = int(valor_juego)
        if activa == "SI" and valor == i:
            mazo.append((valor, palo, valor_juego))

#Variables
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
apuestaBot = 0
bots = ["BotAzul", "BotRojo", "BotVerde", "BotAmarillo", "BotBlanco", "BotNegro", "BotRosa"]

#Control de menús
flag_inicio=True
flag_jugar=True
flag_bots=True
flag_multi=True
flag_info=True
flag_salir=False
print("BIENVENIDO AL SIETE Y MEDIO".rjust(20))
while flag_salir==False:
    #Menu Principal
    while flag_inicio==True:
        print("¿Que quieres hacer?\n1)Jugar\n2)Opciones\n3)Salir")
        opcion=int(input("Opción: "))
        print()
        if opcion==1:
            flag_inicio=False
            flag_jugar=False
        if opcion==2:
            flag_inicio=False
            flag_info=False
        if opcion==3:
            flag_inicio=False
            flag_salir=True
            db.close()
        if opcion<1 or opcion>3:
            print("El numero es incorrecto, pon uno de los establecidos.\n")
    #Menú Jugar
    while flag_jugar==False:
        print("¿A que quieres jugar?\n1)Partida vs bots\n2)Partida multijudaor\n3)Volver al inicio")
        opcion=int(input("Opción: "))
        print()
        if opcion==1:
            flag_jugar=True
            flag_bots=False
        if opcion==2:
            flag_jugar=True
            flag_multi=False
        if opcion==3:
            flag_jugar=True
            flag_inicio=True
        if opcion<1 or opcion>3:
            print("El numero es incorrecto, pon uno de los establecidos.")
            print()
    #Jugar Con bots
    while flag_bots==False:
        print("¿Que quieres hacer?\n1)Empezar una partida\n2)Seleccionar modo de juego")
        opcion=int(input("Opción: "))
        print()
        if opcion==1:
            while not flag_bots:
                njug = int(input("Cuantos jugadores participaran?\n"))
                if njug < Min_Jugadores:
                    print("El numero es demasiado pequeño. Introduce otra cantidad.\n")
                elif njug > Max_Jugadores:
                    print("Demasiados jugadores! Introduce otra cantidad\n")
                elif njug >= Min_Jugadores and njug <= Max_Jugadores:
                    print(f"Empezando partida con {njug} jugadores")
                    max_prioridad = njug
                    #Comprobación del nombre
                    nombrecorrecto = False
                    while not nombrecorrecto:
                        nombre = str(input(f"Nombre del jugador: "))
                        for x in nombre:
                            if x.isspace() == True:
                                print("Tiene espacios")
                                break
                        if nombre[0].isalpha() and nombre.isalnum():
                            jugadoresOrden.append(nombre)
                            nombrecorrecto = True
                        elif not nombre.isalnum():
                            print("No es alfanumerico")
                            continue
                        elif not nombre[0].isalpha():
                            print("El primer caracter no es una letra")
                    for i in range(njug - 1):
                        jugadoresOrden.append(bots[i])
                    flag_bots = True
            while flag_bots:
                if mano < Max_Rondas:
                    mano += 1
                    if mano == 1:
                    #Orden de partida
                        dicc = {}
                        mazo2 = mazo.copy()
                        for i in range(len(jugadoresOrden)):
                            carta = random.choice(mazo2)
                            mazo2.pop(mazo2.index(carta))
                            dicc[jugadoresOrden[i]] = carta
                        #Ordenación por valor
                        for k in range(len(jugadoresOrden)):
                            pasada = False
                            for j in range(1, len(jugadoresOrden) - k):
                                if dicc[jugadoresOrden[j]][0] > dicc[jugadoresOrden[j - 1]][0]:
                                    pasada = True
                                    jugadoresOrden[j], jugadoresOrden[j - 1] = jugadoresOrden[j - 1], jugadoresOrden[j]
                            if pasada == False:
                                break
                        #Ordenación por palo
                        for k in range(len(jugadoresOrden)):
                            for j in range(len(jugadoresOrden) - 1):
                                if dicc[jugadoresOrden[j]][0] == dicc[jugadoresOrden[j + 1]][0] and mazo.index(dicc[jugadoresOrden[j]]) > mazo.index(dicc[jugadoresOrden[j + 1]]):
                                    jugadoresOrden[j], jugadoresOrden[j + 1] = jugadoresOrden[j + 1], jugadoresOrden[j]
                        #Creación lista jugadores ya ordenados
                        for prioridad in range(len(jugadoresOrden)):
                            jugadores.append({jugadoresOrden[prioridad]: [[], "jugando", "jugando", prioridad, 0, 0, Puntos_Iniciales, 1]})
                        if jugadoresOrden[0] in bots:
                            print(f"\nEl {jugadoresOrden[0]} es la banca")
                        else:
                            print(f"\nEl jugador {jugadoresOrden[0]} es la banca")
                    #Inicio de la ronda
                    mazo2 = mazo.copy()
                    for i in range(len(jugadoresOrden)):
                        jugadores[i][jugadoresOrden[i]][0].clear()
                        if jugadores[i][jugadoresOrden[i]][2] == "jugando":
                            carta = random.choice(mazo2)
                            mazo2.pop(mazo2.index(carta))
                            jugadores[i][jugadoresOrden[i]][0].append(carta)
                            jugadores[i][jugadoresOrden[i]][4] = carta[2]

                    #Cartas que han salido
                    for i in range(1, len(jugadores)):
                        if jugadores[i][jugadoresOrden[i]][1] == "jugando" and jugadores[i][jugadoresOrden[i]][2] == "jugando":
                            print("\nLas cartas que han salido son: ")
                            cartas_en_linea = 0
                            for j in mazo:
                                if j not in mazo2:
                                    cartas_en_linea += 1
                                    print(j[0], " de ", j[1], end=", ")
                                if cartas_en_linea == 3:
                                    print()
                                    cartas_en_linea = 0
                            if cartas_en_linea != 0:
                                print()
                            #Muestra de cada jugador, sus puntos en mano, apuesta y puntos restantes
                            print(f"\nLa banca  Puntos en la mano: {jugadores[0][jugadoresOrden[0]][4]}  Puentos restante: {jugadores[0][jugadoresOrden[0]][-2]} ")
                            for k in range(1, len(jugadores)):
                                if jugadores[k][jugadoresOrden[k]][2] != "eliminado":
                                    print(f"{jugadoresOrden[k]}  Puntos en la mano: {jugadores[k][jugadoresOrden[k]][4]}  Apuesta: {jugadores[k][jugadoresOrden[k]][-3]}  Puntos restantes: {jugadores[k][jugadoresOrden[k]][-2]}")
                            print()
                            #Muestra quien juega actualmente y que carta tiene
                            print("=" * 25, "JUEGA ", jugadoresOrden[i], "=" * 25)
                            print(f"\nTiene {jugadores[i][jugadoresOrden[i]][0][0][0]} de {jugadores[i][jugadoresOrden[i]][0][0][1]} \n")
                            #Comprobamos si el jugador es bot o no.
                            if jugadoresOrden[i] not in bots:
                                apuestaCorrecta = False
                                #Comprobación de apuesta correcta
                                while not apuestaCorrecta:
                                    apuesta = int(input("Cuantos puntos quiere apostar?: "))
                                    if apuesta < 1:
                                        print("\nLa apuesta es demasiado baja\n")
                                    elif apuesta > jugadores[i][jugadoresOrden[i]][-2]:
                                        print("\nNo puede apostar más puntos de los que tiene\n")
                                    else:
                                        jugadores[i][jugadoresOrden[i]][-3] = apuesta
                                        jugadores[i][jugadoresOrden[i]][-2] = jugadores[i][jugadoresOrden[i]][-2] - apuesta
                                        apuestaCorrecta = True

                                #Pedir carta o plantarse
                                accion = 0
                                while accion != 2:
                                    if jugadores[i][jugadoresOrden[i]][4] <= 7.5:
                                        accion = int(input("\nQue quiere hacer? \n1) Pedir carta \n2) Plantarse \n"))
                                    else:
                                        print("\nSe ha pasado por el 7.5")
                                        accion = 2
                                    if accion == 1:
                                        carta = random.choice(mazo2)
                                        mazo2.pop(mazo2.index(carta))
                                        jugadores[i][jugadoresOrden[i]][0].append(carta)
                                        jugadores[i][jugadoresOrden[i]][4] += carta[2]
                                        print("Sus cartas son:")
                                        for h in jugadores[i][jugadoresOrden[i]][0]:
                                            print(f"{h[0]} de {h[1]}")
                                    elif accion == 2:
                                        if jugadores[i][jugadoresOrden[i]][4] <= 7.5:
                                            jugadores[i][jugadoresOrden[i]][1] = "plantado"
                                        else:
                                            jugadores[i][jugadoresOrden[i]][1] = "eliminado"
                                    else:
                                        print(f"No existe la opcion  {accion}")
                            #Empieza el algoritmo del bot
                            else:
                                #Rango de la apuesta a partir de la mano
                                if mano < 5:
                                    apuestaBot = random.randint(2, 5)
                                elif mano in range(6, 26):
                                    apuestaBot = random.randint(4, 10)
                                elif mano > 25:
                                    apuestaBot = random.randint(6, 12)
                                if apuestaBot > jugadores[i][jugadoresOrden[i]][-2]:
                                    apuestaBot = (jugadores[i][jugadoresOrden[i]][-2] + 1) // 2
                                #Apuesta del bot
                                jugadores[i][jugadoresOrden[i]][-3] = apuestaBot
                                jugadores[i][jugadoresOrden[i]][-2] = jugadores[i][jugadoresOrden[i]][-2] - apuestaBot
                                print(f"El {jugadoresOrden[i]} apuesta {apuestaBot} puntos")

                                #Acciones del bot
                                BotAcaba = False
                                while not BotAcaba:
                                    noSePasa = 0
                                    for carta in mazo2:
                                        if float(carta[2]) + jugadores[i][jugadoresOrden[i]][4] <= 7.5:
                                            noSePasa += 1
                                    #Calculamos la probabilidad de pasarse
                                    probabilidad = int((noSePasa / len(mazo2)) * 100)
                                    pedimos = random.randint(1, 100)

                                    if jugadores[i][jugadoresOrden[i]][4] < jugadores[0][jugadoresOrden[0]][4] or probabilidad >= 65:
                                        carta = random.choice(mazo2)
                                        mazo2.pop(mazo2.index(carta))
                                        jugadores[i][jugadoresOrden[i]][0].append(carta)
                                        jugadores[i][jugadoresOrden[i]][4] += carta[2]
                                        print(f"El {jugadoresOrden[i]} pide una carta y saca {carta[0]} de {carta[1]}")

                                    elif probabilidad in range(50, 66):
                                        if probabilidad in range(pedimos + 1):
                                            carta = random.choice(mazo2)
                                            mazo2.pop(mazo2.index(carta))
                                            jugadores[i][jugadoresOrden[i]][0].append(carta)
                                            jugadores[i][jugadoresOrden[i]][4] += carta[2]
                                            print(f"El {jugadoresOrden[i]} pide una carta y saca {carta[0]} de {carta[1]}")
                                        else:
                                            BotAcaba = True
                                            print(f"El {jugadoresOrden[i]} se planta")

                                    elif probabilidad < 50:
                                        if probabilidad / 3 in range(1, pedimos + 1):
                                            carta = random.choice(mazo2)
                                            mazo2.pop(mazo2.index(carta))
                                            jugadores[i][jugadoresOrden[i]][0].append(carta)
                                            jugadores[i][jugadoresOrden[i]][4] += carta[2]
                                            print(f"El {jugadoresOrden[i]} pide una carta y saca {carta[0]} de {carta[1]}")
                                        else:
                                            BotAcaba = True
                                            print(f"El {jugadoresOrden[i]} se planta")

                                    if jugadores[i][jugadoresOrden[i]][4] > 7.5:
                                        print("\nSe ha pasado por el 7.5")
                                        BotAcaba = True
                                #Comprobamos si se elimina o no
                                if jugadores[i][jugadoresOrden[i]][4] <= 7.5:
                                    jugadores[i][jugadoresOrden[i]][1] = "plantado"
                                else:
                                    jugadores[i][jugadoresOrden[i]][1] = "eliminado"
                        if jugadoresOrden[i] in bots:
                            input("\nPresiona Enter para ver la siguiente jugada")
                        print("_" * 70)
                    #La banca juega
                    flag_banca = False
                    #Comprueba si los otros jugadores se han plantado
                    for n in range(1, len(jugadoresOrden)):
                        if jugadores[n][jugadoresOrden[n]][1] == "plantado":
                            flag_banca = True
                            break
                    if flag_banca == True:
                        print("\nLas cartas que han salido son: ")
                        cartas_en_linea = 0
                        for j in mazo:
                            if j not in mazo2:
                                cartas_en_linea += 1
                                print(j[0], " de ", j[1], end=", ")
                            if cartas_en_linea == 3:
                                print()
                                cartas_en_linea = 0
                        if cartas_en_linea != 0:
                            print()
                        print(f"\nLa banca  Puntos en la mano: {jugadores[0][jugadoresOrden[0]][4]}  Puentos restante: {jugadores[0][jugadoresOrden[0]][-2]} ")
                        for k in range(1, len(jugadores)):
                            if jugadores[k][jugadoresOrden[k]][2] != "eliminado":
                                print(f"{jugadoresOrden[k]}  Puntos en la mano: {jugadores[k][jugadoresOrden[k]][4]}  Apuesta: {jugadores[k][jugadoresOrden[k]][-3]}  Puntos restantes: {jugadores[k][jugadoresOrden[k]][-2]}")
                        print()
                        print("=" * 25, "JUEGA LA BANCA", "=" * 25)
                        print(f"\nTiene {jugadores[0][jugadoresOrden[0]][0][0][0]} de {jugadores[0][jugadoresOrden[0]][0][0][1]} ")
                        #Comprobamos si la banca es humano
                        if jugadoresOrden[0] not in bots:
                            #No sale del bucle hasta que no se planta o elimina
                            accion = 0
                            while accion != 2:
                                if jugadores[0][jugadoresOrden[0]][4] <= 7.5:
                                    accion = int(input("\nQue quiere hacer? \n1) Pedir carta \n2) Plantarse \n"))
                                else:
                                    print("\nSe ha pasado por el 7.5")
                                    accion = 2
                                if accion == 1:
                                    carta = random.choice(mazo2)
                                    mazo2.pop(mazo2.index(carta))
                                    jugadores[0][jugadoresOrden[0]][0].append(carta)
                                    jugadores[0][jugadoresOrden[0]][4] += carta[2]
                                    print("Sus cartas son:")
                                    for h in jugadores[0][jugadoresOrden[0]][0]:
                                        print(f"{h[0]} de {h[1]}")

                                elif accion == 2:
                                    print(f"\nLa banca tiene {jugadores[0][jugadoresOrden[0]][4]} punto en la mano")
                                    for u in range(1, len(jugadores)):
                                        if jugadores[u][jugadoresOrden[u]][2] == "jugando":
                                            print(f"\nEl jugador {jugadoresOrden[u]} tiene {jugadores[u][jugadoresOrden[u]][4]} punto en la mano")
                                else:
                                    print(f"No existe la opcion  {accion}")
                        #Si la banca es un bot
                        else:
                            for w in range(1, len(jugadores)):
                                if jugadores[0][jugadoresOrden[0]][4] < jugadores[w][jugadoresOrden[w]][4] and jugadores[w][jugadoresOrden[w]][4] <= 7.5:
                                    carta = random.choice(mazo2)
                                    mazo2.pop(mazo2.index(carta))
                                    jugadores[0][jugadoresOrden[0]][0].append(carta)
                                    jugadores[0][jugadoresOrden[0]][4] += carta[2]
                                    print(f"La banca pide una carta y saca {carta[0]} de {carta[1]}")
                        #Comparación de los puntos y resultado ronda
                        cont = 0
                        for n in range(1, len(jugadores)):
                            if jugadores[n][jugadoresOrden[n]][2] == "jugando":
                                #La banca gana puntos
                                if jugadores[n][jugadoresOrden[n]][4] > 7.5 or jugadores[n][jugadoresOrden[n]][4] <= jugadores[0][jugadoresOrden[0]][4]:
                                    jugadores[0][jugadoresOrden[0]][-2] += jugadores[n][jugadoresOrden[n]][-3]
                                    print(f"\nLa banca acumula la apuesta del jugador {jugadoresOrden[n]}")
                                #Comprobación si la banca se ha pasado
                                if jugadores[0][jugadoresOrden[0]][4] > 7.5:
                                    if jugadores[n][jugadoresOrden[n]][4] < 7.5:
                                        recompensa = jugadores[n][jugadoresOrden[n]][-3]
                                        if jugadores[0][jugadoresOrden[0]][-2] - recompensa < 0:
                                            recompensa = jugadores[0][jugadoresOrden[0]][-2]
                                            jugadores[n][jugadoresOrden[n]][-2] += recompensa
                                            jugadores[0][jugadoresOrden[0]][-2] -= recompensa
                                        else:
                                            jugadores[n][jugadoresOrden[n]][-2] += recompensa * 2
                                            jugadores[0][jugadoresOrden[0]][-2] -= recompensa
                                        print(f"\nBanca paga al jugador {jugadoresOrden[n]} {recompensa} puntos")

                                    elif jugadores[n][jugadoresOrden[n]][4] == 7.5:
                                        recompensa = jugadores[n][jugadoresOrden[n]][-3]
                                        if jugadores[0][jugadoresOrden[0]][-2] - recompensa * 2 < 0:
                                            recompensa = jugadores[0][jugadoresOrden[0]][-2]
                                            jugadores[n][jugadoresOrden[n]][-2] += recompensa
                                            jugadores[0][jugadoresOrden[0]][-2] -= recompensa
                                        else:
                                            jugadores[n][jugadoresOrden[n]][-2] += recompensa * 3
                                            jugadores[0][jugadoresOrden[0]][-2] -= recompensa * 2
                                            recompensa *= 2
                                        if cont == 0:
                                            jugadores[0][jugadoresOrden[0]][3] = max_prioridad
                                            jugadores[n][jugadoresOrden[n]][3] = 0
                                            max_prioridad += 1
                                            cont += 1
                                        print(f"\nBanca paga al jugador {jugadoresOrden[n]} {recompensa} puntos y el jugador {jugadoresOrden[n]} pasa a ser la banca")
                                #Comprobación si la banca no se ha pasado
                                elif jugadores[0][jugadoresOrden[0]][4] < 7.5:
                                    if jugadores[n][jugadoresOrden[n]][4] < 7.5 and jugadores[n][jugadoresOrden[n]][4] > jugadores[0][jugadoresOrden[0]][4]:
                                        recompensa = jugadores[n][jugadoresOrden[n]][-3]
                                        if jugadores[0][jugadoresOrden[0]][-2] - recompensa < 0:
                                            recompensa = jugadores[0][jugadoresOrden[0]][-2]
                                            jugadores[n][jugadoresOrden[n]][-2] += recompensa
                                            jugadores[0][jugadoresOrden[0]][-2] -= recompensa
                                        else:
                                            jugadores[n][jugadoresOrden[n]][-2] += recompensa * 2
                                            jugadores[0][jugadoresOrden[0]][-2] -= recompensa
                                        print(f"\nBanca paga al jugador {jugadoresOrden[n]} {recompensa} puntos")

                                    elif jugadores[n][jugadoresOrden[n]][4] == 7.5:
                                        recompensa = jugadores[n][jugadoresOrden[n]][-3]
                                        if jugadores[0][jugadoresOrden[0]][-2] - recompensa * 2 < 0:
                                            recompensa = jugadores[0][jugadoresOrden[0]][-2]
                                            jugadores[n][jugadoresOrden[n]][-2] += recompensa
                                            jugadores[0][jugadoresOrden[0]][-2] -= recompensa
                                        else:
                                            jugadores[n][jugadoresOrden[n]][-2] += recompensa * 3
                                            jugadores[0][jugadoresOrden[0]][-2] -= recompensa * 2
                                            recompensa *= 2
                                        print(f"\nBanca paga al jugador {jugadoresOrden[n]} {recompensa} puntos")
                                        if cont == 0:
                                            jugadores[0][jugadoresOrden[0]][3] = max_prioridad
                                            jugadores[n][jugadoresOrden[n]][3] = 0
                                            max_prioridad += 1
                                            cont += 1
                                            print(f"\nEl jugador {jugadoresOrden[n]} pasa a ser la banca")
                        #Comprueba si la banca tiene un siete y media
                                elif jugadores[0][jugadoresOrden[0]][4] == 7.5:
                                    jugadores[0][jugadoresOrden[0]][-2] += jugadores[n][jugadoresOrden[n]][-3]

                        if jugadores[0][jugadoresOrden[0]][4] == 7.5:
                            print("\nLa banca gana a todos por siete y medio")
                    #Si todos los jugadores estan eliminados
                    else:
                        print("\nHa ganado la banca")
                        for a in range(1, len(jugadores)):
                            jugadores[0][jugadoresOrden[0]][-2] += jugadores[a][jugadoresOrden[a]][-3]
                            print(f"\nLa banca acumula la apuesta del jugador {jugadoresOrden[a]}")
                    #Pasar turno de bot
                    if jugadoresOrden[0] in bots:
                        input("\nPresiona Enter para ver la siguiente jugada")
                    print("_" * 70)
                    #Comprueba si la banca ha perdido todos sus puntos
                    if jugadores[0][jugadoresOrden[0]][-2] == 0 and jugadores[0][jugadoresOrden[0]][3] == 0:
                        jugadores[0][jugadoresOrden[0]][3] = max_prioridad
                        max_prioridad += 1
                        #Se cambia la banca
                        for h in range(len(jugadores)):
                            if jugadores[h][jugadoresOrden[h]][-2] > 0:
                                jugadores[h][jugadoresOrden[h]][3] = 0
                                print(f"\nEl jegador {jugadoresOrden[h]} pasa a ser la banca")
                                break
                    #Cambia la banca si el jugador gana con siete y medio
                    if jugadores[0][jugadoresOrden[0]][3] != 0:
                        for s in range(len(jugadores)):
                            pasada = False
                            for g in range(1, len(jugadores) - s):
                                if jugadores[g][jugadoresOrden[g]][3] < jugadores[g - 1][jugadoresOrden[g - 1]][3]:
                                    pasada = True
                                    jugadores[g], jugadores[g - 1] = jugadores[g - 1], jugadores[g]
                                    jugadoresOrden[g], jugadoresOrden[g - 1] = jugadoresOrden[g - 1], jugadoresOrden[g]
                            if pasada == False:
                                break
                    #Resetea los puntos mano y la apuesta y se suma mano
                    for d in range(len(jugadores)):
                        jugadores[d][jugadoresOrden[d]][4] = 0
                        jugadores[d][jugadoresOrden[d]][5] = 0
                        jugadores[d][jugadoresOrden[d]][-1] = mano + 1

                    #Comprueba cuantos jugadores se eliminan de la partida
                    continuan = 0
                    for q in range(len(jugadores)):
                        if jugadores[q][jugadoresOrden[q]][-2] == 0:
                            jugadores[q][jugadoresOrden[q]][2] = "eliminado"
                            jugadores[q][jugadoresOrden[q]][1] = "eliminado"
                            print(f"El jugador {jugadoresOrden[q]} está eliminado de la partida")
                        else:
                            continuan += 1
                            ganador = jugadoresOrden[q]
                            jugadores[q][jugadoresOrden[q]][1] = "jugando"
                    #Si solo queda un jugador en la partida, gana.
                    if continuan == 1:
                        break
                #Elije el ganador cuando se llega al limite de rondas
                else:
                    ganador = jugadoresOrden[0]
                    numero_ganador = 0
                    for s in range(len(jugadores)):
                        if jugadores[s][jugadoresOrden[s]][2] == "jugando" and jugadores[s][jugadoresOrden[s]][-2] > jugadores[numero_ganador][ganador][-2]:
                            ganador = jugadoresOrden[s]
                            numero_ganador = s
                    flag_bots = False
            print(f"\nEl {ganador} ha ganado el juego!!!")
            option = 0
            while option not in range(1, 3):
                option = int(input("¿Que quiere hacer?\n1) Jugar otra vez  \n2)Salir"))
                if option == 1:
                    flag_jugar = False
                    flag_bots = True
                    mano = 0
                    jugadores = []
                    jugadoresOrden = []
                    dicc = {}
                elif option == 2:
                    flag_bots = True
                    flag_inicio = False
                    flag_salir = True
                else:
                    print(f"No existe la opción {option}")

        if opcion==2:
            flag_bots=True
            flag_jugar=False
        if opcion<1 or opcion>2:
            opcion=int(input("El numero es incorrecto, pon uno de los establecidos.\nOpción: "))
    while flag_multi==False:
        print("¿Que quieres hacer?\n1)Empezar una partida\n2)Seleccionar modo de juego")
        opcion=int(input("Opción: "))
        print()
        if opcion==1:
            while not flag_multi:
                #Numero de jugadores en partida
                njug = int(input("Cuantos jugadores participaran?\n"))
                if njug < Min_Jugadores:
                    print("El numero es demasiado pequeño. Introduce otra cantidad.\n")
                elif njug > Max_Jugadores:
                    print("Demasiados jugadores! Introduce otra cantidad\n")
                elif njug >= Min_Jugadores and njug <= Max_Jugadores:
                    print(f"Empezando partida con {njug} jugadores")
                    max_prioridad = njug
                    #Comprobación de nombres
                    for i in range(njug):
                        nombrecorrecto = False
                        while not nombrecorrecto:
                            nombre = str(input(f"Nombre del jugador {i + 1}: "))
                            while nombre in jugadoresOrden:
                                print("Nombre de jugador ya existe,inserta otro")
                                nombre = str(input(f"Nombre del jugador {i + 1}: "))
                            for x in nombre:
                                if x.isspace() == True:
                                    print("Tiene espacios")
                                    break
                            if nombre[0].isalpha() and nombre.isalnum():
                                jugadoresOrden.append(nombre)
                                nombrecorrecto = True
                            elif not nombre.isalnum():
                                print("No es alfanumerico")
                                continue
                            elif not nombre[0].isalpha():
                                print("El primer caracter no es una letra")
                                continue
                    flag_multi = True

            while flag_multi:
                if mano < Max_Rondas:
                    mano += 1
                    if mano == 1:
                        dicc = {}
                        mazo2 = mazo.copy()
                        for i in range(len(jugadoresOrden)):
                            carta = random.choice(mazo2)
                            mazo2.pop(mazo2.index(carta))
                            dicc[jugadoresOrden[i]] = carta

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
                            jugadores.append({jugadoresOrden[prioridad]: [[], "jugando", "jugando", prioridad, 0, 0, Puntos_Iniciales, 1]})
                        print(f"\nEl jugador {jugadoresOrden[0]} es la banca")

                    mazo2 = mazo.copy()
                    for i in range(len(jugadoresOrden)):
                        jugadores[i][jugadoresOrden[i]][0].clear()
                        if jugadores[i][jugadoresOrden[i]][2] == "jugando":
                            carta = random.choice(mazo2)
                            mazo2.pop(mazo2.index(carta))
                            jugadores[i][jugadoresOrden[i]][0].append(carta)
                            jugadores[i][jugadoresOrden[i]][4] = carta[2]

                    for i in range(1, len(jugadores)):
                        if jugadores[i][jugadoresOrden[i]][1] == "jugando" and jugadores[i][jugadoresOrden[i]][2] == "jugando":
                            print("\nLas cartas que han salido son: ")
                            cartas_en_linea = 0
                            for j in mazo:
                                if j not in mazo2:
                                    cartas_en_linea += 1
                                    print(j[0], " de ", j[1], end=", ")
                                if cartas_en_linea == 3:
                                    print()
                                    cartas_en_linea = 0
                            if cartas_en_linea != 0:
                                print()
                            print(f"\nLa banca  Puntos en la mano: {jugadores[0][jugadoresOrden[0]][4]}  Puntos restante: {jugadores[0][jugadoresOrden[0]][-2]} ")
                            for k in range(1, len(jugadores)):
                                if jugadores[k][jugadoresOrden[k]][2] != "eliminado":
                                    print(
                                        f"{jugadoresOrden[k]}  Puntos en la mano: {jugadores[k][jugadoresOrden[k]][4]}  Apuesta: {jugadores[k][jugadoresOrden[k]][-3]}  Puntos restantes: {jugadores[k][jugadoresOrden[k]][-2]}")
                            print()
                            print("=" * 15, "JUEGA ", jugadoresOrden[i], "=" * 15)
                            print(f"\nTiene {jugadores[i][jugadoresOrden[i]][0][0][0]} de {jugadores[i][jugadoresOrden[i]][0][0][1]} \n")
                            apuestaCorrecta = False
                            while not apuestaCorrecta:
                                apuesta = int(input("Cuantos puntos quiere apostar?: "))
                                if apuesta < 1:
                                    print("\nLa apuesta es demasiado baja\n")
                                elif apuesta > jugadores[i][jugadoresOrden[i]][-2]:
                                    print("\nNo puede apostar más puntos de los que tiene\n")
                                else:
                                    jugadores[i][jugadoresOrden[i]][-3] = apuesta
                                    jugadores[i][jugadoresOrden[i]][-2] = jugadores[i][jugadoresOrden[i]][-2] - apuesta
                                    apuestaCorrecta = True
                            accion = 0
                            while accion != 2:
                                if jugadores[i][jugadoresOrden[i]][4] <= 7.5:
                                    accion = int(input("\nQue quiere hacer? \n1) Pedir carta \n2) Plantarse \n"))
                                else:
                                    print("\nSe ha pasado por el 7.5")
                                    accion = 2
                                if accion == 1:
                                    carta = random.choice(mazo2)
                                    mazo2.pop(mazo2.index(carta))
                                    jugadores[i][jugadoresOrden[i]][0].append(carta)
                                    jugadores[i][jugadoresOrden[i]][4] += carta[2]
                                    print("Sus cartas son:")
                                    for h in jugadores[i][jugadoresOrden[i]][0]:
                                        print(f"{h[0]} de {h[1]}")
                                elif accion == 2:
                                    if jugadores[i][jugadoresOrden[i]][4] <= 7.5:
                                        jugadores[i][jugadoresOrden[i]][1] = "plantado"
                                    else:
                                        jugadores[i][jugadoresOrden[i]][1] = "eliminado"
                                else:
                                    print(f"No existe la opcion  {accion}")
                        print("_" * 70)

                    flag_banca = False
                    for n in range(1, len(jugadoresOrden)):
                        if jugadores[n][jugadoresOrden[n]][1] == "plantado":
                            flag_banca = True
                            break
                    if flag_banca == True:
                        print("\nLas cartas que han salido son: ")
                        cartas_en_linea = 0
                        for j in mazo:
                            if j not in mazo2:
                                cartas_en_linea += 1
                                print(j[0], " de ", j[1], end=", ")
                            if cartas_en_linea == 3:
                                print()
                                cartas_en_linea = 0
                        if cartas_en_linea != 0:
                            print()
                        print(f"\nLa banca  Puntos en la mano: {jugadores[0][jugadoresOrden[0]][4]}  Puntos restante: {jugadores[0][jugadoresOrden[0]][-2]} ")
                        for k in range(1, len(jugadores)):
                            if jugadores[k][jugadoresOrden[k]][2] != "eliminado":
                                print(f"{jugadoresOrden[k]}  Puntos en la mano: {jugadores[k][jugadoresOrden[k]][4]}  Apuesta: {jugadores[k][jugadoresOrden[k]][-3]}  Puntos restantes: {jugadores[k][jugadoresOrden[k]][-2]}")
                        print()
                        print("=" * 15, "JUEGA LA BANCA", "=" * 15)
                        print(f"\nTiene {jugadores[0][jugadoresOrden[0]][0][0][0]} de {jugadores[0][jugadoresOrden[0]][0][0][1]} ")
                        accion = 0
                        while accion != 2:
                            if jugadores[0][jugadoresOrden[0]][4] <= 7.5:
                                accion = int(input("\nQue quiere hacer? \n1) Pedir carta \n2) Plantarse \n"))
                            else:
                                print("\nSe ha pasado por el 7.5")
                                accion = 2
                            if accion == 1:
                                carta = random.choice(mazo2)
                                mazo2.pop(mazo2.index(carta))
                                jugadores[0][jugadoresOrden[0]][0].append(carta)
                                jugadores[0][jugadoresOrden[0]][4] += carta[2]
                                print("Sus cartas son:")
                                for h in jugadores[0][jugadoresOrden[0]][0]:
                                    print(f"{h[0]} de {h[1]}")

                            elif accion == 2:
                                print(f"\nLa banca tiene {jugadores[0][jugadoresOrden[0]][4]} punto en la mano")
                                for u in range(1, len(jugadores)):
                                    if jugadores[u][jugadoresOrden[u]][2] == "jugando":
                                        print(f"\nEl jugador {jugadoresOrden[u]} tiene {jugadores[u][jugadoresOrden[u]][4]} punto en la mano")
                                cont = 0
                                for n in range(1, len(jugadores)):
                                    if jugadores[n][jugadoresOrden[n]][2] == "jugando":
                                        if jugadores[n][jugadoresOrden[n]][4] > 7.5 or jugadores[n][jugadoresOrden[n]][4] <= jugadores[0][jugadoresOrden[0]][4]:
                                            jugadores[0][jugadoresOrden[0]][-2] += jugadores[n][jugadoresOrden[n]][-3]
                                            print(f"\nLa banca acumula la apuesta del jugador {jugadoresOrden[n]}")

                                        if jugadores[0][jugadoresOrden[0]][4] > 7.5:
                                            if jugadores[n][jugadoresOrden[n]][4] < 7.5:
                                                recompensa = jugadores[n][jugadoresOrden[n]][-3]
                                                if jugadores[0][jugadoresOrden[0]][-2] - recompensa < 0:
                                                    recompensa = jugadores[0][jugadoresOrden[0]][-2]
                                                    jugadores[n][jugadoresOrden[n]][-2] += recompensa
                                                    jugadores[0][jugadoresOrden[0]][-2] -= recompensa
                                                else:
                                                    jugadores[n][jugadoresOrden[n]][-2] += recompensa * 2
                                                    jugadores[0][jugadoresOrden[0]][-2] -= recompensa
                                                print(f"\nBanca paga al jugador {jugadoresOrden[n]} {recompensa} puntos")

                                            elif jugadores[n][jugadoresOrden[n]][4] == 7.5:
                                                recompensa = jugadores[n][jugadoresOrden[n]][-3]
                                                if jugadores[0][jugadoresOrden[0]][-2] - recompensa * 2 < 0:
                                                    recompensa = jugadores[0][jugadoresOrden[0]][-2]
                                                    jugadores[n][jugadoresOrden[n]][-2] += recompensa
                                                    jugadores[0][jugadoresOrden[0]][-2] -= recompensa
                                                else:
                                                    jugadores[n][jugadoresOrden[n]][-2] += recompensa * 3
                                                    jugadores[0][jugadoresOrden[0]][-2] -= recompensa * 2
                                                    recompensa *= 2
                                                print(f"\nBanca paga al jugador {jugadoresOrden[n]} {recompensa} puntos ")
                                                if cont == 0:
                                                    jugadores[0][jugadoresOrden[0]][3] = max_prioridad
                                                    jugadores[n][jugadoresOrden[n]][3] = 0
                                                    max_prioridad += 1
                                                    cont += 1
                                                    print(f"\nEl jugador {jugadoresOrden[n]} pasa a ser la banca")

                                        elif jugadores[0][jugadoresOrden[0]][4] < 7.5:
                                            if jugadores[n][jugadoresOrden[n]][4] < 7.5 and jugadores[n][jugadoresOrden[n]][4] > jugadores[0][jugadoresOrden[0]][4]:
                                                recompensa = jugadores[n][jugadoresOrden[n]][-3]
                                                if jugadores[0][jugadoresOrden[0]][-2] - recompensa < 0:
                                                    recompensa = jugadores[0][jugadoresOrden[0]][-2]
                                                    jugadores[n][jugadoresOrden[n]][-2] += recompensa
                                                    jugadores[0][jugadoresOrden[0]][-2] -= recompensa
                                                else:
                                                    jugadores[n][jugadoresOrden[n]][-2] += recompensa * 2
                                                    jugadores[0][jugadoresOrden[0]][-2] -= recompensa
                                                print(f"\nBanca paga al jugador {jugadoresOrden[n]} {recompensa} puntos")

                                            elif jugadores[n][jugadoresOrden[n]][4] == 7.5:
                                                recompensa = jugadores[n][jugadoresOrden[n]][-3]
                                                if jugadores[0][jugadoresOrden[0]][-2] - recompensa * 2 < 0:
                                                    recompensa = jugadores[0][jugadoresOrden[0]][-2]
                                                    jugadores[n][jugadoresOrden[n]][-2] += recompensa
                                                    jugadores[0][jugadoresOrden[0]][-2] -= recompensa
                                                else:
                                                    jugadores[n][jugadoresOrden[n]][-2] += recompensa * 3
                                                    jugadores[0][jugadoresOrden[0]][-2] -= recompensa * 2
                                                    recompensa *= 2
                                                if cont == 0:
                                                    jugadores[0][jugadoresOrden[0]][3] = max_prioridad
                                                    jugadores[n][jugadoresOrden[n]][3] = 0
                                                    max_prioridad += 1
                                                    cont += 1
                                                print(f"\nBanca paga al jugador {jugadoresOrden[n]} {recompensa} puntos y el jugador {jugadoresOrden[n]} pasa a ser la banca")

                                        elif jugadores[0][jugadoresOrden[0]][4] == 7.5:
                                            jugadores[0][jugadoresOrden[0]][-2] += jugadores[n][jugadoresOrden[n]][-3]

                                if jugadores[0][jugadoresOrden[0]][4] == 7.5:
                                    print("\nLa banca gana a todos por siete y medio")
                            else:
                                print(f"No existe la opcion  {accion}")
                    else:
                        print("\nHa ganado la banca")
                        for a in range(1, len(jugadores)):
                            jugadores[0][jugadoresOrden[0]][-2] += jugadores[a][jugadoresOrden[a]][-3]
                            print(f"\nLa banca acumula la apuesta del jugador {jugadoresOrden[a]}")

                    print("_" * 70)

                    if jugadores[0][jugadoresOrden[0]][-2] == 0 and jugadores[0][jugadoresOrden[0]][3] == 0:
                        jugadores[0][jugadoresOrden[0]][3] = max_prioridad
                        max_prioridad += 1

                        for h in range(len(jugadores)):
                            if jugadores[h][jugadoresOrden[h]][-2] > 0:
                                jugadores[h][jugadoresOrden[h]][3] = 0
                                print(f"\nEl jugador {jugadoresOrden[h]} pasa a ser la banca")
                                break

                    if jugadores[0][jugadoresOrden[0]][3] != 0:
                        for s in range(len(jugadores)):
                            pasada = False
                            for g in range(1, len(jugadores) - s):
                                if jugadores[g][jugadoresOrden[g]][3] < jugadores[g - 1][jugadoresOrden[g - 1]][3]:
                                    pasada = True
                                    jugadores[g], jugadores[g - 1] = jugadores[g - 1], jugadores[g]
                                    jugadoresOrden[g], jugadoresOrden[g - 1] = jugadoresOrden[g - 1], jugadoresOrden[g]
                            if pasada == False:
                                break

                    for d in range(len(jugadores)):
                        jugadores[d][jugadoresOrden[d]][4] = 0
                        jugadores[d][jugadoresOrden[d]][5] = 0
                        jugadores[d][jugadoresOrden[d]][-1] = mano + 1

                    continuan = 0
                    for q in range(len(jugadores)):
                        if jugadores[q][jugadoresOrden[q]][-2] == 0:
                            jugadores[q][jugadoresOrden[q]][2] = "eliminado"
                            jugadores[q][jugadoresOrden[q]][1] = "eliminado"
                            print(f"El jugador {jugadoresOrden[q]} está eliminado de la partida")
                        else:
                            continuan += 1
                            ganador = jugadoresOrden[q]
                            jugadores[q][jugadoresOrden[q]][1] = "jugando"
                    if continuan == 1:
                        break
                else:
                    ganador = jugadoresOrden[0]
                    numero_ganador = 0
                    for s in range(len(jugadores)):
                        if jugadores[s][jugadoresOrden[s]][2] == "jugando" and jugadores[s][jugadoresOrden[s]][-2] > jugadores[numero_ganador][ganador][-2]:
                            ganador = jugadoresOrden[s]
                            numero_ganador = s
                    flag_multi = False
            print(f"\nEl {ganador} ha ganado el juego!!!")
            option = 0
            while option not in range(1, 3):
                option = int(input("¿Que quiere hacer?\n1) Jugar otra vez  \n2)Salir"))
                if option == 1:
                    flag_jugar = False
                    flag_multi = True
                    mano = 0
                    jugadores = []
                    jugadoresOrden = []
                    dicc = {}
                elif option == 2:
                    flag_multi = True
                    flag_inicio = False
                    flag_salir = True
                else:
                    print(f"No existe la opción {option}")
        if opcion==2:
            flag_multi=True
            flag_jugar=False
        if opcion<1 or opcion>2:
            opcion=int(input("El numero es incorrecto, pon uno de los establecidos.\nOpción: "))
    #Opciones e información
    while flag_info==False:
        print("¿Que quieres ver?\n1)Reglas\n2)Consultas\n3)Volver al inicio")
        opcion=int(input("Opción: "))
        print()
        if opcion==1:
            print("¿Que reglas quieres ver?\n1)Reglas Banca\n2)Reglas Victoria\n3)Volver atrás")
            subopcion=int(input("Opción: "))
            print()
            if subopcion==1:
                print("Uno es banca cuando gana a la banca, la primera banca se establece\n mediante el orden de prioridad inicial.")
            if subopcion==2:
                print("El ganador de un turno es el que consigue siete y medio, o el que se\n acerca mas, sin pasarse. Para ganar la partida no se debe quedar sin puntos.")
            if subopcion==3:
                flag_info = True
                flag_inicio = True
            if subopcion<1 or subopcion>3:
                print("La opción no es correcta. Pon otra. \n")
        if opcion==2:
            #Querys
            print("Que consulta quieres hacer?\n\n"
                  "1)Carta inicial más repetida por cada jugador\n"
                  "2)Jugador que realiza la apuesta más alta por partida.\n"
                  "3)Jugador que realiza apuesta más baja por partida.\n"
                  "4)Porcentaje de partidas ganadas Bots en general.\n"
                  "5)Cuántas rondas se ganan en cada partida según el palo.\n"
                  "6)Cuantas rondas gana la banca en cada partida\n"
                  "7)Cuántos usuarios han sido la banca en una partida.\n"
                  "8)Partida con la puntuación más alta final de todos los jugadores.\n"
                  "9)La apuesta media por partida.\n"
                  "10)El valor total de las cartas y el numero total de cartas que se han dado inicialmente en las manos en la partida.\n"
                  "11)Diferencia de puntos de los participantes de las partidas entre la ronda 1 y 5.")
            subopcion = int(input("Opcion: "))
            print()
            if subopcion == 1:
                query_sql = "select username,descripcion,carta_inicial from (select a.id_participante,username,descripcion,max(a.cnt) contador from (select p.id_participante,u.username,b.descripcion,count(t.carta_inicial) cnt  from turnos t inner join participante p on p.id_participante=t.idparticipante inner join jugador j on j.idjugador=p.id_jugador left join usuario u on u.idusuario=j.idusuario left join bot b on b.idbot=j.idbot group by u.username,b.descripcion,t.carta_inicial) a group by username,descripcion) c inner join (select idparticipante, carta_inicial,count(carta_inicial) contador2 from turnos group by carta_inicial,idparticipante) d on c.id_participante = d.idparticipante where contador = contador2 group by username,descripcion"
                query("Query1", query_sql)
            if subopcion == 2:
                query_sql = "select username,descripcion from(select u.username,descripcion,max(t.apuesta)puntos,t.idpartida,t.idparticipante from turnos t inner join participante p on p.id_participante=t.idparticipante inner join jugador j on j.idjugador=p.id_jugador left join usuario u on u.idusuario=j.idusuario left join bot b on b.idbot = j.idbot group by idpartida,idparticipante order by idpartida) as a inner join (select max(apuesta) puntos2,idpartida,idparticipante from turnos group by idpartida) as c where a.puntos=c.puntos2 and a.idpartida=c.idpartida group by a.idparticipante,a.idpartida"
                query("Query2", query_sql)
            if subopcion == 3:
                query_sql = "select username,descripcion from(select u.username,descripcion,min(t.apuesta)puntos,t.idpartida,t.idparticipante from turnos t inner join participante p on p.id_participante=t.idparticipante inner join jugador j on j.idjugador=p.id_jugador left join usuario u on u.idusuario=j.idusuario left join bot b on b.idbot = j.idbot group by idpartida,idparticipante order by idpartida) as a inner join (select min(apuesta) puntos2,idpartida,idparticipante from turnos group by idpartida) as c where a.puntos=c.puntos2 and a.idpartida=c.idpartida group by a.idpartida"
                query("Query3", query_sql)
            if subopcion == 4:
                query_sql = 'select * from ( select round(count(ganador_partida)*100/count(idpartida)) as "Porcentaje %" from partida p inner join participante pa on p.ganador_partida=pa.id_participante inner join jugador j on pa.id_jugador=j.idjugador inner join bot b on j.idbot=b.idbot where ganador_partida=pa.id_participante) as contador'
                query("Query5", query_sql)
            if subopcion == 5:
                query_sql = 'select idpartida,count(numero_turno) as "Rondas Ganadas",descripcion Palo from turnos t left join cartas c on t.carta_inicial = c.idcartas left join tipo_carta tc on c.tipo = tc.idtipo_carta  where puntos_final > puntos_inicio group by idpartida,Palo;'
                query("Query7", query_sql)
            if subopcion == 6:
                query_sql = 'select idpartida,count(numero_turno) as "Rondas Ganadas" from turnos t left join cartas c on t.carta_inicial = c.idcartas left join tipo_carta tc on c.tipo = tc.idtipo_carta  where puntos_final > puntos_inicio and es_banca = 1 group by idpartida;'
                query("Query8", query_sql)
            if subopcion == 7:
                query_sql = "select count(es_banca), idpartida from turnos where es_banca=1 group by idpartida"
                query("Query9", query_sql)
            if subopcion == 8:
                query_sql = 'select par.idpartida,t.idparticipante,u.username,b.descripcion,par.nombre_sala,max(t.puntos_final),if(par.ganador_partida=t.idparticipante,"Si","No") as ganador from partida par inner join turnos t on t.idpartida=par.idpartida inner join participante p on p.id_participante=t.idparticipante inner join jugador j on j.idjugador=p.id_jugador left join usuario u on u.idusuario=j.idusuario left join bot b on b.idbot=j.idbot where par.idpartida IN (select idparticipante from turnos group by idparticipante) and t.puntos_final IN (select max(puntos_final) from turnos group by idparticipante) group by u.username,b.descripcion'
                query("Query10", query_sql)
            if subopcion == 9:
                query_sql = "select avg(apuesta), idpartida from turnos group by idpartida"
                query("Query11", query_sql)
            if subopcion == 10:
                query_sql = 'select sum(truncate(c.valor,1)) as "Valor por partida", count(t.carta_inicial) as "Cantidad" from cartas c inner join turnos t on c.idcartas=t.carta_inicial group by t.idpartida'
                query("Query13", query_sql)
            if subopcion == 11:
                query_sql = "select t5.p2-t1.p1 diferencia from (select distinct puntos_inicio p1 from turnos t where numero_turno = 1 group by idpartida) t1, ( select puntos_inicio p2 from turnos where numero_turno = 5) t5"
                query("Query14", query_sql)
            if subopcion < 1 or subopcion > 11:
                print("La opción no es correcta. Pon otra.")
            print()
            input("Pulsa cualquier tecla")
            print()
        if opcion==3:
            flag_info=True
            flag_inicio=True
        if opcion<1 or opcion>3:
            print("El numero es incorrecto, pon uno de los establecidos.")