import cv2 
import pytesseract
import numpy as np
import pyautogui
from PIL import Image
import time 

pytesseract.pytesseract.tesseract_cmd = r'C:\Users\Oscar\AppData\Local\Tesseract-OCR\tesseract.exe'

while True:

    screen = pyautogui.screenshot()
    screen_array = np.array(screen)
    espacioEspecifico = screen_array[:400,:800,:]

    corregirColor = cv2.cvtColor(espacioEspecifico, cv2.COLOR_RGB2BGR)


    im_gray = cv2.cvtColor(espacioEspecifico, cv2.COLOR_BGR2GRAY)
    # Aplicar OCR para reconocer el texto

    #retval, threshold2 = cv2.threshold(im_gray,125,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)


    textinscreen = pytesseract.image_to_string(im_gray , lang='eng')

    objinscreen = pytesseract.image_to_data(im_gray , lang='eng',output_type='data.frame')

    #string = "hola me llamo p"
    text = str(textinscreen)
    buscar = text.find("pofi")

    # Obtener las coordenadas de los cuadros alrededor de las palabras reconocidas
    boxes = pytesseract.image_to_boxes(im_gray)

    if buscar != -1:
        print ("hola")
        try:
            x, y = objinscreen[objinscreen['text'] ==
                        "pofi"]['left'].iloc[0], objinscreen[objinscreen['text'] == "pofi"]['top'].iloc[0]
            
            xfin, yfin = objinscreen[objinscreen['text'] == "pofi"]['left'].iloc[0] + \
                objinscreen[objinscreen['text'] == "pofi"]['width'].iloc[0], objinscreen[
                    objinscreen['text'] == "pofi"]['top'].iloc[0] + objinscreen[
                        objinscreen['text'] == "pofi"]['height'].iloc[0]
            pyautogui.moveTo(x,y,0.5)
            pyautogui.mouseDown()

            pyautogui.moveTo(xfin,yfin,0.5)
            pyautogui.mouseUp()

            time.sleep(2)
            print(x,y)
        except:
        # The text was not found on the screen
            print("nada")

        
        

    
    # if text.find("pofi"):
    #     print(text)
    #     print(boxes)

    # # Dibujar los cuadros en la imagen original
    # for box in boxes.splitlines():
    #     box = box.split(' ')
    #     x, y, w, h = int(box[1]), int(box[2]), int(box[3]), int(box[4])
    #     cv2.rectangle(corregirColor, (x, corregirColor.shape[0] - y), (w, corregirColor.shape[0] - h), (0, 255, 0), 1)


    cv2.imshow("lector",corregirColor)

    if cv2.waitKey(1) & 0xFF==ord("q"):
        break

cv2.destroyAllWindows()