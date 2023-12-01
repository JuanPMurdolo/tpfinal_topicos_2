# tpfinal_topicos_2
Trabajo final de topicos 2


Topicos de Ingeniería de Software 2

Enunciado
Este trabajo integrador consiste en el desarrollo de un servicio Web (API) que expone un modelo de red neuronal para clasificar los parámetros del servicio:

El modelo diagnostica riesgo cardíaco (si el paciente tiene o no-tiene riesgo cardíaco) a partir de los datos clínicos del paciente (nivel de colesterol, presión arterial, nivel de azúcar en sangre, edad, sobrepeso y tabaquismo ) .

El servicio solo deberá poder ser invocado por clientes de nuestra plataforma y por lo tanto deberán pasar una API Key.  Las invocaciones (request) HTTP deberá contar con el header HTTP 'Authorization' indicando la API key.  Si la API key no se encuentra en la invocación, ésta deberá ser rechazada.

GET /service
Authorization: <API Key generada>

{
"nivel_colesterol": 2.00,
"presion_arterial":1.20,
"azucar":1.00
"edad":40,
"sobrepeso":1,
"tabaquismo":0
}

Aclaración. los rangos de los datos son
colesterol =  (1.0, 3.0)
presion = (0.6, 1.8)
azucar= (0.5, 2.0)
edad = (0,99)
sobrepeso 0 o 1, donde 1 representa presencia de sobrepeso.
tabaquismo 0 o 1, donde 1 representa presencia de tabaquismo.


Existen dos tipos de cuentas que restringen la cantidad de solicitudes HTTP por minuto que el sistema está autorizado a resolver por minuto:
FREEMIUM; 5 solicitudes por minuto (RPM).
PREMIUM: 50 solicitudes por minuto (RPM).

El servicio deberá satisfacer los siguientes requerimientos:

Deberá correr la red neuronal entrenada previamente.
Todos las  invocaciones que reciba el servicio deberán ser controladas verificando dos aspectos:
Autorización. A partir de la API key, se verifica si exista registrada la API key en la base de datos del sistema.
Limitación. De acuerdo a la suscripción del cliente tiene una limitación de invocaciones por segundo: FREEMIUM y PREMIUM.
Cada solicitud recibida deberá ser registrada en la bitácora (log). Capturando el tiempo que tomo para procesar el requerimiento HTTP de diagnostico: iniciar el timer cuando se recibe la solicitud HTTP, procesar la autenticación de la key, correr la red neuronal, registrar el resultado en la bitácora, y retornar la respuesta.
Para datos de solo lectura y de poca volatilidad, se espera que se implemente cache.


Entregables

La solución deberá contar con los siguientes entregables:
Instructivo para correr el proceso de entrenamiento del modelo de ML
Informe de diseño donde se presenten diagramas, aclaraciones sobre los requerimientos y toma de decisiones.
Bateria de test HTTP para probar el funcionamiento de los servicios.

Fechas de entrega



Preguntas
¿ Si se pueden utilizar librerías para solucionar la capturas de tiempo de procesamiento de los requerimientos HTTP?
Si, se pueden utilizar.
¿Se tiene utilizar cualquier tecnología para resolver el trabajo?
No, el trabajo esta restricto a Python.
¿Se puede realizar el trabajo en grupo?
Si.
 



# Notas de los alumnos

Vamos a usar SQLITE3 para no usar mongo por una cuestion de comodidad.