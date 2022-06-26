from flask import Flask, request, jsonify, render_template, make_response
import os
from werkzeug.utils import secure_filename

from datetime import datetime

from pprint import pprint
import os


# from dotenv import load_dotenv
# load_dotenv()

from ocr_app import ocr_app_get_text


app = Flask(__name__,
            template_folder='./templates',)
 
# Fuente: https://stackoverflow.com/questions/51436382/runtimeerror-the-session-is-unavailable-because-no-secret-key-was-set-set-the
# Esto arregla un error que sucede cuando se llama
# al método mega_logout desde el método de la app3.py /upload.
# app.secret_key = "caircocoders-ednalan"


UPLOAD_FOLDER = 'static/uploads/' # Original
# OCR_RESULTS_UPLOAD = 'static/ocr_results/' # Funciona en Windows
OCR_RESULTS_UPLOAD = r'./static/ocr_results/'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['OCR_RESULTS_UPLOAD'] = OCR_RESULTS_UPLOAD

app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
 
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# region Html pages

@app.route('/', methods=['GET'])
def index():
    return render_template("index.html")
    # return render_template("index.html", name = name)

@app.route('/index2', methods=['GET'])
def index2():
    return render_template("index2.html")

@app.route('/index3', methods=['GET'])
def index3():
    return render_template("index3.html")

@app.route('/base_html', methods=['GET'])
def base_html(title=None):
    return render_template("base.html", title = title)

@app.route('/result', methods=['GET'])
def html_result(result=None):
    return render_template("result.html", result = result)

@app.route('/result2', methods=['GET'])
def html_result2(result=None):
    return render_template("result2.html", result = result)

# endregion

# En Index, url_for('upload_file_test') apunta a este método
# sin importar la ruta que tenga definida
@app.route('/upload_test', methods=['POST'])
def upload_file_test():
    # Getting files uploaded in form enctype="multipart/form-data"
    files = request.files['files[]']
    
    print('files:', files)

    message, result, status_code = upload_file(files)

    # pprint(vars(result))
    # print('result.response["ocr_extracted_text"]:', result.response["ocr_extracted_text"])
    # print('result.response[0]:', result.response[0])
    # print('result.response[0][1]:', result.response[0][0])
    # print('result.response[0].decode("utf-8"):', result.response[0].decode("utf-8"))
    # print(type(result.response[0]))


    return render_template("result2.html", result = result)


@app.route('/upload', methods=['POST'])
def upload_file():

    # Obtiene del campo 'files[]' en el request hecho por el usuario los archivos que contenga
    files = request.files.getlist('files[]')
    message, result, status_code = upload_file(files)

    print('result:', result)

    if status_code == 200 or status_code == 201:  
        return render_template("result2.html", result = result)
    else: # Para probar esteescenario, en el if dejar solo el status_code == 200
        return render_template("result.html", result = message)


    # # Check if the post request has the file part
    # if 'files[]' not in request.files and 'photo' not in request.files:
    #     # resp = jsonify({'message' : 'No file part in the request'})
    #     # resp = jsonify({'message' : 'No file uploaded in the request :/, go back and upload some.'})
    #     errors['message'] = 'No file uploaded in the request :/, go back and upload some.'
    #     resp = jsonify(errors)
    #     resp.status_code = 400
    #     resp.content_type = "application/json"
    #     # return resp
    #     # return make_response(resp, resp.status_code)
    #     return render_template("result.html", result = errors['message'])


    # # Obtiene del campo 'files[]' en el request hecho por el usuario los archivos que contenga
    # files = request.files.getlist('files[]')
     
    # errors = {}
    # success = False

    # for file in files:      
    #     if file and allowed_file(file.filename):
    #         print(file)
    #         # pprint(vars(file))

    #         filename = file.filename

    #         # Get file extension
    #         ext = '.' in filename and filename.rsplit('.', 1)[1].lower()

    #         filename = secure_filename(file.filename)

    #         # datetime object containing current date and time
    #         now = datetime.now()

    #         # date and time: dd/mm/YY H:M:S
    #         dt_string = now.strftime("%d-%m-%Y %H-%M-%S")

    #         # Para que sea un nombre único, se agrega
    #         # la fecha y hora en la que se hizo la consulta
    #         filename = filename + "_" + dt_string + "." + ext

    #         photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    #         file.save(photo_path)

    #         size = os.path.getsize(photo_path)
    #         print("size:", size, "bytes")

    #         success = True
    #     else:
    #         errors[file.filename] = 'File type is not allowed'
 
    # if success and errors:
    #     """ Así mostraría el mensaje
    #         {
    #             "message": "Files successfully uploaded, but some errors occurred."
    #         }
    #     """
    #     errors['message'] = 'File(s) successfully uploaded, but some errors occurred.'
    #     resp = jsonify(errors)
    #     resp.status_code = 500
    #     resp.content_type = "application/json"
    #     # return resp
    #     # return make_response(resp, resp.status_code)
    #     return render_template("result.html", result = errors['message'])


    # if success:
    #     # Type (print(type(resp))): flask.wrappers.Response
    #     resp = jsonify({'message' : 'Files successfully uploaded'})
    #     # resp.status_code = 201
    #     # resp.content_type = "application/json"

    #     ocr_text_result = ocr_app_get_text(os.path.join(app.config['UPLOAD_FOLDER'], filename))


    #     # Si el texto extraído no está vacío...
    #     if ocr_text_result != '':

    #         ocr_text_result = ocr_text_result.replace("\n\n", " ").replace("\u201c", '\"').replace("\u201d", '"').replace("\\", "")

    #         # if upload_success:
    #         # replace is only for making json esthetic, when returned, left the \n\n and else
    #         resp = jsonify({
    #             'message' : 'Files successfully uploaded',
    #             'ocr_extracted_text': ocr_text_result
    #         })

    #     # return resp
    #     # return make_response(resp, ocr_text_result)
    #     return render_template("result.html", result = ocr_text_result)
    # else:
    #     resp = jsonify(errors) 
    #     resp.status_code = 500
    #     resp.content_type = "application/json"
    #     # return resp
    #     # return make_response(resp, resp.status_code)
    #     return render_template("result.html", result = errors['message'])


def upload_file(files):
    # Check if the post request has the file part
    if 'files[]' not in request.files and 'photo' not in request.files:
        # resp = jsonify({'message' : 'No file part in the request'})
        # resp = jsonify({'message' : 'No file uploaded in the request :/, go back and upload some.'})
        errors['message'] = 'No file uploaded in the request :/, go back and upload some.'
        resp = jsonify(errors)
        resp.status_code = 400
        resp.content_type = "application/json"
        # return resp
        return errors, "No file uploaded", 400


    # Obtiene del campo 'files[]' en el request hecho por el usuario los archivos que contenga
    files = request.files.getlist('files[]')
     
    errors = {}
    success = False

    for file in files:      
        if file and allowed_file(file.filename):
            print(file)
            # pprint(vars(file))

            filename = file.filename

            # Get file extension
            ext = '.' in filename and filename.rsplit('.', 1)[1].lower()

            filename = secure_filename(file.filename)

            # datetime object containing current date and time
            now = datetime.now()

            # date and time: dd/mm/YY H:M:S
            dt_string = now.strftime("%d-%m-%Y %H-%M-%S")

            # Para que sea un nombre único, se agrega
            # la fecha y hora en la que se hizo la consulta
            filename = filename + "_" + dt_string + "." + ext

            photo_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(photo_path)

            size = os.path.getsize(photo_path)
            print("size:", size, "bytes")

            success = True
        else:
            errors[file.filename] = 'File type is not allowed'
 
    if success and errors:
        """ Así mostraría el mensaje
            {
                "message": "Files successfully uploaded, but some errors occurred."
            }
        """
        errors['message'] = 'File(s) successfully uploaded, but some errors occurred.'
        resp = jsonify(errors)
        resp.status_code = 500
        resp.content_type = "application/json"
        # return resp
        return errors, errors['message'], 500


    if success:
        # Type (print(type(resp))): flask.wrappers.Response
        resp = jsonify({'message' : 'Files successfully uploaded'})
        # resp.status_code = 201
        # resp.content_type = "application/json"

        ocr_text_result = ocr_app_get_text(os.path.join(app.config['UPLOAD_FOLDER'], filename))


        # Si el texto extraído no está vacío...
        if ocr_text_result != '':

            message = 'Files successfully uploaded'
            ocr_text_result = ocr_text_result.replace("\n\n", " ").replace("\u201c", '\"').replace("\u201d", '"').replace("\\", "")

            # if upload_success:
            # replace is only for making json esthetic, when returned, left the \n\n and else
            resp = jsonify({
                'message' : message,
                'ocr_extracted_text': ocr_text_result
            })

        return message, ocr_text_result, 201
    else:
        resp = jsonify(errors) 
        resp.status_code = 500
        resp.content_type = "application/json"
        # return resp
        return errors, errors['message'], 500




if __name__ == '__main__':
    app.config['SESSION_TYPE'] = 'filesystem'

    app.run(port = 7000) # ,debug = True

    