import requests
import json

url_star_wars = "https://swapi.dev/api/planets"

#----------------------------------------
# Obtener datos de la api con metodo GET
#----------------------------------------
url_api = "http://127.0.0.1:8000/api/producto/"

response = requests.get(url_api)

if response.status_code == 200:

    respoinse_json = json.loads(response.text)
    #print(respoinse_json)

    for i in respoinse_json:
        if i['id'] == 1:
            print(i)


#----------------------------------------
# Subir datos a la api con metodo POST
#----------------------------------------



#---------------------------------------------------------------------------------
# Pruebas con api de star wars. TIene otra pagina en la api, el el atributo "next"
#----------------------------------------------------------------------------------

# response = requests.get(url)

# if response.status_code == 200:
#     data = response.json()
#     planetas = data['results']

#     while True:  # Continuar hasta que no haya más páginas
#         for planeta in planetas:
#             print(planeta['name'])

#         if data['next']:  # Si hay una próxima página, obtenerla
#             response = requests.get(data['next'])
#             data = response.json()
#             planetas = data['results']
#         else:
#             break
# else:
#     print('Algo salió mal, este es el código de respuesta:', response.status_code)