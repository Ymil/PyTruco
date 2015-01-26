class Msg:
    mensaje = {}

    #Mensajes de error
    mensaje['error'] = {}
    mensaje['error'][0] = '[ERROR]No se puedo conectar con el servidor\nLo intentaremos devuelta en %d segundos'
    
    mensaje[0] = 'Bienvenido a PyTruco\nNesecitamos que ingreses tu nombre de usuario'
    mensaje[1] = '[ERROR] Deves ingresar un nombre'
    mensaje[2] = 'Excelente, ya estas ingresado'
    mensaje[5] = 'Ahora puede entrar en una mesa o crear una\n\t1 - Crear mesa\n\t2 - Entrar en una mesa\n\t3 - Mostrar mesas'
    mensaje[3] = 'La mesa ya esta armada\nEsperando Jugadores...'
    mensaje[4] = 'Es tu turno de jugar, ingresa tu jugada'
    
    mensaje[400] = '[Error] Deves ingresar un valor %s'
    
    mensaje[100] = 'Conexion exitosa!'
    
    mensaje[1000] = 'Creando mesa...\nIngresa la cantidad de jugadores\n\t1 - 2 Jugadores\n\t2 - 4 Jugadores\n\t3 - 6 Jugadores'
    mensaje[1001] = 'La mesa ya esta creada'
    mensaje[1002] = '\tEsperando Jugadores...'
    mensaje[1003] = 'Bienvenido a la mesa creada por %s'
    mensaje[1004] = '%s ha ingresado a la mesa'
    mensaje[1005] = 'Ingresa el numero de mesa al cual deseas ingresar'
    mensaje[1006] = 'Iniciando partida'
    mensaje[1007] = '\tHa jugar'
    mensaje[1050] = 'La mesa que as elijido no existe'
    mensaje[1100] = 'Mesa: %s jugadores %s/%s creada por %s'
    
    mensaje[2000] = ''