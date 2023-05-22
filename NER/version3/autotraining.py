import cv2 
import pytesseract
import numpy as np
import pyautogui
from PIL import Image
import time 
import spacy 


pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Oscar\AppData\Local\Tesseract-OCR\tesseract.exe'
nlp_ner = spacy.load(r"NER\version3\model-last")

control = True 
labels = []
texts = []
autoincre = 0


pofi = []
orden = []
cancion = []
preposicion = []
artista = []

listaTexts = [pofi, orden, cancion, preposicion, artista]

dicListas = {
    "POFI" : pofi.extend,
    "ORDEN" : orden.extend,
    "CANCION" : cancion.extend,
    "PREPOSICION" : preposicion.extend,
    "ARTISTA" : artista.extend
}


while True:
    
    #toma un pantallazo
    screen = pyautogui.screenshot()
    #convierte el pantallazo a un arreglo numpy 
    screen_array = np.array(screen)
    #le establezco un espacio especifico para que solo tome ese fragmento de la pantalla
    espacioEspecifico = screen_array[150:335,300:1300,:]
    #la imagen viene en una especie de gris entonces arreglo eso pasandola a BGR
    corregirColor = cv2.cvtColor(espacioEspecifico, cv2.COLOR_RGB2BGR)
    #convierto la imagen a gris puro para que pytesseract pueda entenderla
    im_gray = cv2.cvtColor(espacioEspecifico, cv2.COLOR_BGR2GRAY)
    #me extraer las imagenes y me las convierte en datos pandas (data.frame)
    objinscreen = pytesseract.image_to_data(im_gray , lang='eng',output_type='data.frame')


    #este bucle sirve para extraer las etiquetas y el texto, 
    #ejemplo si cancion: ella es mi todo, agrega cada palabra por separado a la lista cancion
    if control == True:
        #print("estoy dentro")
        textinscreen = pytesseract.image_to_string(im_gray , lang='eng')
        text = str(textinscreen)
 

        doc = nlp_ner(text)
        for ent in doc.ents:    
            etiqueta = str(ent.label_)
            labels.append(etiqueta)
            
            texto = str(ent.text.rstrip('\n'))
            texto = texto.split()
            #en el diccionario busco por la etiqueta y agrego el texto, el código 
            #extend se encuentra en el diccionario
            dicListas[etiqueta](texto)

        #una vez el bucle haya terminado de agregar las etiquetas y los texto encontrados en sus
        #respectivas listas, la variable de control pasa a cambiar, esto con el fin de que 
        #mientras busco las coordenadas de cada palabra (que van a cambiar constantemente)
        #1. el modelo NER deje de predecir
        #2. el modelo Pytesseract deje de sacar el texto
        #3. no se sobreescriban las listas
   
        control = False

    #este try intentará hallar las coordenadas de las palabras 
    try:
        
        #este bucle sirve para iterar la cantidad de veces en que indique la lista seleccionada
        #ejemplo: listaTexts[autoincre= 0] == pofi["pofi"]
        #i = 0
        #esto quiere decir que la lista pofi solo será iterada 1 vez porque solo tiene 1 elemento
        for i in range(len(listaTexts[autoincre])):
            print(f"numero actual: {i}")
            print(autoincre)
            #si los elementos de la lista son mayores a 0, es decir 
            #hay 2 o 3 palabras en la lista, quiero que tome nuevas capturas
            #de pantalla para que se actualice la posición de los elementos 
            # if i > 0:

            #     screen = pyautogui.screenshot()
            #     screen_array = np.array(screen)
            #     espacioEspecifico = screen_array[150:335,300:1300,:]
            #     corregirColor = cv2.cvtColor(espacioEspecifico, cv2.COLOR_RGB2BGR)
            #     im_gray = cv2.cvtColor(espacioEspecifico, cv2.COLOR_BGR2GRAY)
            #     objinscreen = pytesseract.image_to_data(im_gray , lang='eng',output_type='data.frame')

        
            x = objinscreen[objinscreen['text'] ==listaTexts[autoincre][i]]['left'].iloc[0]

            y= objinscreen[objinscreen['text'] == listaTexts[autoincre][i]]['top'].iloc[0]

            xfin = objinscreen[objinscreen['text'] == listaTexts[autoincre][i]]['left'].iloc[0] + \
                objinscreen[objinscreen['text'] == listaTexts[autoincre][i]]['width'].iloc[0]
            
            yfin = objinscreen[objinscreen['text'] == listaTexts[autoincre][i]]['top'].iloc[0] + \
                objinscreen[objinscreen['text'] == listaTexts[autoincre][i]]['height'].iloc[0]
            
       #este condicional es para saber si la lista posee más de un elemento
       #el metodo len cuenta apartir del 1, entonces si la lista tiene 3
       #elementos, va a decir que tiene 3 elementos en lugar de 2
       #2 fuese si se contara desde el 0
        if len(listaTexts[autoincre]) > 1:
            #en caso tal de que la lista posea más de un elemento, entonces quiero
            #almacenar las coordenadas de la primera palabra 
            x = objinscreen[objinscreen['text'] ==listaTexts[autoincre][0]]['left'].iloc[0]
            y= objinscreen[objinscreen['text'] == listaTexts[autoincre][0]]['top'].iloc[0]

            #y las coordenadas de la última palabra que conforma la lista 
            #debo restarle -1 porque estoy intentano acceder al último elemento de una lista
            #ejemplo: listaTexts[autoincre=2] == cancion["en","tu","luna"]
            #la estructura para acceder a un elemento de una lista DENTRO de otra lista es:
            #listaDeListas[listaDentro][posicionElementoListaDentro]
            #listaTexts[2][2] == "luna"
            xfin = objinscreen[objinscreen['text'] == listaTexts[autoincre][len(listaTexts[autoincre])-1]]['left'].iloc[0] + \
            objinscreen[objinscreen['text'] == listaTexts[autoincre][len(listaTexts[autoincre])-1]]['width'].iloc[0]
            yfin = objinscreen[objinscreen['text'] == listaTexts[autoincre][len(listaTexts[autoincre])-1]]['top'].iloc[0] + \
            objinscreen[objinscreen['text'] == listaTexts[autoincre][len(listaTexts[autoincre])-1]]['height'].iloc[0]
            

        if labels[autoincre] == "POFI":
            pyautogui.press("1")
        elif labels[autoincre] == "ORDEN":
            pyautogui.press("2")
        elif labels[autoincre] == "CANCION":
            pyautogui.press("3")
        elif labels[autoincre] == "PREPOSICION":
            pyautogui.press("4")
        elif labels[autoincre] == "ARTISTA":
            pyautogui.press("5")
        
        pyautogui.moveTo(300+x,150+y,0.5)
        pyautogui.mouseDown()
        pyautogui.moveTo(300+xfin,150+yfin,0.5)
        pyautogui.mouseUp()
        

     
    except:
        print("No encontrado")
        
 
    autoincre += 1
    if autoincre == 5:
        autoincre = 0
        control = True
        pofi.clear()
        orden.clear()
        cancion.clear()
        preposicion.clear()
        artista.clear()
        labels.clear()
        texts.clear()
        pyautogui.press("space")
        time.sleep(3)
    

    #cv2.imshow("lector",corregirColor)

    if cv2.waitKey(1) & 0xFF==ord("q"):
        break

cv2.destroyAllWindows()