from flask import Flask
from config import DB_CONFIG
from models.grade import db
from controllers.grade_controller import grade_bp
import time
import os

app = Flask(__name__)
app.config.update(DB_CONFIG)
db.init_app(app)
app.register_blueprint(grade_bp)

if __name__ == '__main__':
    # Añadir un poco de tiempo para asegurar que la base de datos esté lista
    retry_count = 0
    max_retries = 5
    
    while retry_count < max_retries:
        try:
            with app.app_context():
                db.create_all()
                break
        except Exception as e:
            retry_count += 1
            print(f"Intento {retry_count}/{max_retries} fallido: {e}")
            if retry_count < max_retries:
                print("Esperando 5 segundos antes de reintentar...")
                time.sleep(5)
            else:
                print("No se pudo conectar a la base de datos después de varios intentos.")
                raise
    
    app.run(host='0.0.0.0', port=5000, debug=True)
