# OCR App imports

# pip install pytesseract
import pytesseract
# pip install opencv-python
import cv2
import os


# region OCR App method

"""
    img_path: Ruta donde se encuentra la imagen que se quiere leer.
"""
def ocr_app_get_text(img_path):
    
    # FOR WINDOWS (uncomment if executed in local Windows pc)
    # If you don't have tesseract executable in your PATH, include the following:
    # pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files/Tesseract-OCR/tesseract'
    # pytesseract.pytesseract.tesseract_cmd = r'C:/Program Files (x86)/Tesseract-OCR/tesseract'


    IMAGE_PATH = img_path

    img = cv2.imread(IMAGE_PATH)

    # More quality image
    imout = cv2.detailEnhance(img)

    # More quality in binarized image 
    imout_grey = cv2.cvtColor(imout, cv2.COLOR_BGR2GRAY)

    print('IMAGE_PATH:', IMAGE_PATH)


    # Get txt files for each read image
    text = pytesseract.image_to_string(img)
    text_imout_grey = pytesseract.image_to_string(imout_grey)

    print('text:', text)
    print()
    print('text_imout_grey:', text_imout_grey)


    remove_picture(IMAGE_PATH)
    
    if os.path.exists(IMAGE_PATH):
        print("File still exists.")

    return text_imout_grey

# endregion


# Fuente: https://appdividend.com/2021/08/13/how-to-delete-file-if-exists-in-python/#:~:text=To%20delete%20a%20file%20if,remove()%20method.
def remove_picture(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        print("The file has been deleted successfully")
    else:
        print("The file does not exist!")


# region More OCR tests

import socket
from datetime import datetime
from flask import request, jsonify
from pprint import pprint
import pyodbc
import requests
from requests import get

os.environ["ODBCSYSINI"] = r"./home/Nubia/flask-ocr-app-2/"
def validate_user(origin = None):

    print('From:',origin) if origin else print('From: OCR Index')
    print("pyodbc.drivers():", pyodbc.drivers())
    try:

        hostname = socket.gethostname()    
        IPAddr = socket.gethostbyname(hostname)
        my_IPAddr = request.remote_addr
        # ip_addr_env = request.environ['HTTP_X_FORWARDED_FOR'] # For proxy requests
        ip = get('https://api.ipify.org').content.decode('utf8')

        # datetime object containing current date and time
        now = datetime.now()

        # date and time: dd/mm/YY H:M:S
        dt_string = now.strftime("%d-%m-%Y %H:%M:%S")

        print("Your Computer Name is:",hostname)    
        print("Your Computer IP Address is:",IPAddr)
        print(f'My public IP address is: {ip}')
        print("My remote IP Address is:",my_IPAddr)
        print("Page checked at",dt_string)


        url = 'http://localhost:3000/empleado/validate_user' # Localhost
        url = 'https://node-pm-proy.herokuapp.com/empleado/validate_user' # Heroku

        data = {
            "hostname": hostname,
            "ip_addr": IPAddr,
            "remote_ip_addr": my_IPAddr,
            "proxy_ip_addr": 'proxy_addr',
            "checked_time": dt_string,
        }
        # Los datos se vuelven undefined con este header
        headers = {'Content-type': 'text/html; charset=UTF-8'} 
        print(data)
        response = requests.post(url, json=data)
        # response = requests.post(url, data=data, verify=False, headers=headers)

        print("response:", response)

        # wait for the response. it should not be higher 
        # than keep alive time for TCP connection

        # render template or redirect to some url:
        # return redirect("some_url")
        # return render_template("some_page.html", message=str(response.text)) # or response.json()


        # sql = 'EXEC nb_set_checked_time ?, ?, ?, ?, ?'
        # values = (hostname, IPAddr, my_IPAddr, '', dt_string)

        # cursor = create_connection()

        # cursor.execute(sql, (values)) # (values)
        # for row in cursor.fetchall():
        #     print(row)
        
        # cursor.commit() # Aunque ya haya trans en el proc, esto termina de guardar datos

        print()
        # pprint(vars(request))

    except Exception as e:
        print("Error:", e)
        pass



def create_connection():
    # Fuente: https://help.pythonanywhere.com/pages/MSSQLServer/
    # .freetds: https://www.freetds.org/userguide/freetdsconf.html
    cnxn_str = ("DSN={0};"
            # "DRIVER={FreeTDS};"
            "Uid={1};"
            "Pwd={2};" # Encrypt=yes;Connection Timeout=30;
            .format(
                '[sqlserverdatasource]',
                os.getenv("SQL_SVR_USER_ID"),
                os.getenv("SQL_SVR_PWD")
            ))

    # Connection to SQL Server
    cnxn = pyodbc.connect(cnxn_str)

    cursor = cnxn.cursor()

    return cursor 

# endregion
