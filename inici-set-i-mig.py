flag_inicio=True
flag_jugar=True
flag_bots=True
flag_multi=True
flag_info=True
flag_salir=False
while flag_salir==False:
    while flag_inicio==True:
        print("¿Que quieres hacer?\n1)Jugar\n2)Opciones\n3)Salir")
        opcion=int(input("Opción: "))
        if opcion==1:
            flag_inicio=False
            flag_jugar=False
        if opcion==2:
            flag_inicio=False
            flag_info=False
        if opcion==3:
            flag_inicio=False
            flag_salir=True
        if opcion<1 or opcion>3:
            opcion=int(input("El numero es incorrecto, pon uno de los establecidos.\nOpción: "))
    while flag_jugar==False:
        print("¿A que quieres jugar?\n1)Partida vs bots\n2)Partida multijudaor\n3)Volver al inicio")
        opcion=int(input("Opción: "))
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
            opcion=int(input("El numero es incorrecto, pon uno de los establecidos.\nOpción: "))
    while flag_bots==False:
        print("¿Que quieres hacer?\n1)Empezar una partida\n2)Seleccionar modo de juego")
        opcion=int(input("Opción: "))
        if opcion==1:
            print("Se realiza una partida contra bots")
        if opcion==2:
            flag_bots=True
            flag_jugar=False
        if opcion<1 or opcion>2:
            opcion=int(input("El numero es incorrecto, pon uno de los establecidos.\nOpción: "))
    while flag_multi==False:
        print("¿Que quieres hacer?\n1)Empezar una partida\n2)Seleccionar modo de juego")
        opcion=int(input("Opción: "))
        if opcion==1:
            print("Se realiza una partida multijugador")
        if opcion==2:
            flag_multi=True
            flag_jugar=False
        if opcion<1 or opcion>2:
            opcion=int(input("El numero es incorrecto, pon uno de los establecidos.\nOpción: "))
    #Opciones e información
    while flag_info==False:
        print("¿Que quieres ver?\n1)Reglas\n2)Consultas\n3)Volver al inicio")
        opcion=int(input("Opción: "))
        if opcion==1:
            print("¿Que reglas quieres ver?\n1)Reglas Banca\n2)Reglas Victoria\n3)Volver atrás")
            subopcion=int(input("Opción: "))
            if subopcion==1:
                print("Uno es banca cuando gana a la banca, la primera banca se establece\n mediante el orden de prioridad inicial.")
            if subopcion==2:
                print("El ganador de un turno es el que consigue siete y medio, o el que se\n acerca mas, sin pasarse. Para ganar la partida no se debe quedar sin puntos.")
            if subopcion==3:
                print()
            if subopcion<1 or subopcion>3:
                subopcion=int(input("La opción no es correcta. Pon otra. \nOpción: "))
        if opcion==2:
            print("Aqui se muestran las diferentes consultas de mySQL")
        if opcion==3:
            flag_info=True
            flag_inicio=True
        if opcion<1 or opcion>3:
            opcion=int(input("El numero es incorrecto, pon uno de los establecidos.\nOpción: "))