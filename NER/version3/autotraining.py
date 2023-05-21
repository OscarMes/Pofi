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


while True:

    screen = pyautogui.screenshot()
    screen_array = np.array(screen)
    espacioEspecifico = screen_array[200:400,300:1300,:]
    

    corregirColor = cv2.cvtColor(espacioEspecifico, cv2.COLOR_RGB2BGR)


    im_gray = cv2.cvtColor(espacioEspecifico, cv2.COLOR_BGR2GRAY)

    textinscreen = pytesseract.image_to_string(im_gray , lang='eng')

    #objinscreen = pytesseract.image_to_data(im_gray , lang='eng',output_type='data.frame')
    objinscreen = pytesseract.image_to_data(im_gray , lang='eng',output_type='string')
    text = str(textinscreen)
    #buscar = text.find("pofi")
    #print(text)



  

    # for ent in doc.ents:
    #     print(ent.text,ent.label_)
        # if ent.label_ == "CANCION":
        #     cancion = ent.text
        #     print(str(cancion))

    # Obtener las coordenadas de los cuadros alrededor de las palabras reconocidas
    #boxes = pytesseract.image_to_boxes(im_gray)

    #if buscar != -1:
        #print ("hola")

    if control == True:
        doc = nlp_ner(text)
        for ent in doc.ents:
            #print(ent.text,ent.label_)
            labels.append(str(ent.label_))
            texts.append(str(ent.text))
            #print(labels)
        #print(texts[2])
        control = False

    try:
        
        x = objinscreen[objinscreen['text'] ==texts[2]]['left'].iloc[0]
        print(x)
        y= objinscreen[objinscreen['text'] == texts[2]]['top'].iloc[0]

        xfin = objinscreen[objinscreen['text'] == texts[2]]['left'].iloc[0] + \
            objinscreen[objinscreen['text'] == texts[2]]['width'].iloc[0]
        
        yfin = objinscreen[objinscreen['text'] == texts[2]]['top'].iloc[0] + \
            objinscreen[objinscreen['text'] == texts[2]]['height'].iloc[0]



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
        
        pyautogui.moveTo(300+x,200+y,0.5)
        
        # pyautogui.moveTo(x,y,0.5)
        pyautogui.mouseDown()

        pyautogui.moveTo(300+xfin,200+yfin,0.5)
        pyautogui.mouseUp()

        time.sleep(1)
        autoincre += 1
        print(x,y)
        print(xfin,yfin)




     
    except:
    # The text was not found on the screen
        print("No encontrado")
        #pass

    


    #cv2.imshow("lector",corregirColor)

    if cv2.waitKey(1) & 0xFF==ord("q"):
        break

cv2.destroyAllWindows()