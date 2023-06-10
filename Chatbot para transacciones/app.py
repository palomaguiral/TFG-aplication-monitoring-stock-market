from flask import Flask, request, render_template, jsonify
from flask_cors import CORS, cross_origin
import openai
from io import BytesIO
from dotenv import load_dotenv
import os

from ibapi.client import *
from ibapi.wrapper import *



#Cargar la API Key de OpenAI, que está como variable de entorno
load_dotenv()
apikey_openai = os.getenv('APIKEY_OPENAI')




app = Flask(__name__)
app.debug=True
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# -*- coding: utf-8 -*-
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Autenticación de la API de OpenAI
openai.api_key = apikey_openai


##############################################System1##############################################################
#System:
with open('system_nl_code.txt', 'r') as archivo:
    AIBroker = archivo.read()

# Función para obtener la respuesta de OpenAI a partir de la entrada del usuario
def crear_codigo_operacion(usuario_input):
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": AIBroker},
                        {"role": "user", "content": usuario_input}
                    ]
                )

    # Selecciona la primera respuesta generada por el modelo
    return response['choices'][0]['message']['content']


#code=crear_codigo_operacion('quiero comprar 5 acciones de Apple')



#################################################System2###################################################################
#System:
with open('system_code_explanation.txt', 'r') as archivo:
    TWSAPIexplanator = archivo.read()

# Función para obtener la respuesta de OpenAI a partir de la entrada del usuario
def explicacion_codigo(code_input):
    response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                        {"role": "system", "content": TWSAPIexplanator},
                        {"role": "user", "content": code_input}
                    ]
                )

    # Selecciona la primera respuesta generada por el modelo
    return response['choices'][0]['message']['content']


#code_explanation=explicacion_codigo(str(code))


##################################################Ejecutar código###################################################################
#print('--> SE VA A EJECUTAR EL CÓDIGO...')
#exec(code) # aquí se ejecuta el código


##############################Templates###############################################
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/results', methods=['GET'])
def results():
    query_parameter = request.args.get('query')  # Get the query parameter from the URL

    # ·NL --> Python
    code=crear_codigo_operacion(query_parameter)
    
    #Para quitar posibles explicaciones y comentarios y quedarnos solo con el código
    start = code.find('from ibapi.client import *')
    end = code.find('app.disconnect()') + len('app.disconnect()')
    cleaned_code = code[start:end]

    print(cleaned_code)
    
    print('.......................................')

    # ·Python --> NL explanation
    code_explanation=explicacion_codigo(cleaned_code)
    print(code_explanation)
    print('.......................................')


    # ·Execute the proposed Python code:
    #print('vamos a ejecutar el código')
    exec(cleaned_code)    #Tener la TWS desktop app abierta
    #print('código ejecutado')
    
    

    #return render_template('results.html', user_query = query_parameter, homer_data=homer_result, mohit_data=mohit_result, sql_result=sql_result, plot_name = 'new_plot', plot_url ='/static/charts/new_plot.png')
    return render_template('results.html', user_query = query_parameter, code=cleaned_code, code_explanation=code_explanation)






#######Ejecución#######
if __name__ == '__main__':
    app.run()
