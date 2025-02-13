import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("C:/Users/HP/Documents/ARCHIVOS_GIT/Servidor_movil/app/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
