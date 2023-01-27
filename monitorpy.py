#---------------------------------------------------------------------------------------------------------------#
#------------------------------------[Programa realizado por:]--------------------------------------------------#
#---------------------------------[Andres Felipe Ramirez Campos]------------------------------------------------#
#-------------------------------------[Juan David Rosas Diaz]---------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------#

#--------------------------------------[Modulos Importados]-----------------------------------------------------#

import network, time, urequests
import dht
import utime
import ujson
import ufirebase as firebase
from machine import Pin

#-----------------------------------------[Objeto Creado]-------------------------------------------------------#

sensor = dht.DHT22(Pin(2))

#-----------------------------------------[Conexion WIFI]-------------------------------------------------------#

time.sleep(20)

def conectaWifi (red, password):
      global miRed
      miRed = network.WLAN(network.STA_IF)     
      if not miRed.isconnected():              
          miRed.active(True)                   
          miRed.connect(red, password)         
          print('Conectando a la red', red +"…")
          timeout = time.time ()
          while not miRed.isconnected():          
              if (time.ticks_diff (time.time (), timeout) > 10):
                  return False
      return True

if conectaWifi ("Red/2.4", "123456789J"):

    print ("Conexión exitosa!")
    print('Datos de la red (IP/netmask/gw/DNS):', miRed.ifconfig())
 
#----------------------------------------[Destino Firebase]-----------------------------------------------------#
    
    firebase.setURL("https://monitorpy-a8e4c-default-rtdb.firebaseio.com/")
    
#------------------------------------------[Destino IFTTT]------------------------------------------------------#

    url = "https://maker.ifttt.com/trigger/monitorpy/with/key/cGmbG-rQ7sCsvJW3piNq1r?"

#----------------------------------------------[Core]-----------------------------------------------------------#

    while True:
        time.sleep(60)
        sensor.measure()
        temperatura = sensor.temperature()
        humedad = sensor.humidity()     
        message = {"Humedad":humedad, "Temperatura":temperatura}
      
        #Datos enviados
        firebase.put("MonitorPY", message, bg=0)
        print("Enviado...", message)

        #Datos obtenidos 
        firebase.get("MonitorPY", "dato_recuperado", bg=0)
        print("Recuperado.... "+str(firebase.dato_recuperado))
        
        if temperatura >= 10 and humedad >= 10:

            respuesta = urequests.get(url+"&value1="+str(temperatura)+"&value2="+str(humedad))
            print(respuesta.text)
            print(respuesta.status_code)
            respuesta.close ()
        
else:
       print ("Imposible conectar")
       miRed.active (False)

#------------------------------------------------[FIN]-----------------------------------------------------------#
