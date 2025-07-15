import os
from datetime import datetime
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import pandas as pd
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import html
from werkzeug.utils import secure_filename

# Configuración de la aplicación Flask
application = Flask(__name__, static_folder='static', template_folder='templates')
CORS(application)

# Configuración
CONFIG = {
    'EXCEL_FILE': 'contactos_ronald.xlsx',
    'EMAIL': {
        'SMTP_SERVER': 'smtp.gmail.com',
        'SMTP_PORT': 587,
        'SENDER_EMAIL': 'ronaldmartinezgcbs@gmail.com',
        'SENDER_PASSWORD': 'xzan cnwp oapc omem',
        'RECIPIENT_EMAIL': 'ronaldmartinezgcbs@gmail.com'
    },
    'REQUIRED_FIELDS': ['name', 'email', 'subject', 'message'],
    'MAX_CONTENT_LENGTH': 5 * 1024 * 1024
}

application.config['MAX_CONTENT_LENGTH'] = CONFIG['MAX_CONTENT_LENGTH']

def init_excel_file():
    if not os.path.exists(CONFIG['EXCEL_FILE']):
        df = pd.DataFrame(columns=['Fecha', 'Nombre', 'Email', 'Asunto', 'Mensaje'])
        df.to_excel(CONFIG['EXCEL_FILE'], index=False)

def save_to_excel(data):
    df = pd.read_excel(CONFIG['EXCEL_FILE'])
    new_row = {
        'Fecha': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Nombre': html.escape(data.get('name', '')),
        'Email': html.escape(data.get('email', '')),
        'Asunto': html.escape(data.get('subject', '')),
        'Mensaje': html.escape(data.get('message', ''))
    }
    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
    df.to_excel(CONFIG['EXCEL_FILE'], index=False)

def send_email(data):
    msg = MIMEMultipart()
    msg['From'] = CONFIG['EMAIL']['SENDER_EMAIL']
    msg['To'] = CONFIG['EMAIL']['RECIPIENT_EMAIL']
    msg['Subject'] = f"Mensaje de contacto: {html.escape(data.get('subject', ''))}"
    
    body = f"""
    <h2>Nuevo mensaje de contacto</h2>
    <p><strong>Fecha:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
    <p><strong>Nombre:</strong> {html.escape(data.get('name', ''))}</p>
    <p><strong>Email:</strong> {html.escape(data.get('email', ''))}</p>
    <p><strong>Asunto:</strong> {html.escape(data.get('subject', ''))}</p>
    <p><strong>Mensaje:</strong> {html.escape(data.get('message', ''))}</p>
    """
    
    msg.attach(MIMEText(body, 'html'))
    
    try:
        server = smtplib.SMTP(CONFIG['EMAIL']['SMTP_SERVER'], CONFIG['EMAIL']['SMTP_PORT'])
        server.starttls()
        server.login(CONFIG['EMAIL']['SENDER_EMAIL'], CONFIG['EMAIL']['SENDER_PASSWORD'])
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error al enviar email: {e}")
        return False

# Rutas
@application.route('/')
def home():
    return send_from_directory('templates', 'iniciob.html')

@application.route('/contacto', methods=['GET', 'POST'])  # Cambiado a /contacto
@application.route('/contactob', methods=['GET', 'POST'])  # Mantenemos ambas por compatibilidad
def contacto():
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            missing_fields = [field for field in CONFIG['REQUIRED_FIELDS'] if not data.get(field)]
            
            if missing_fields:
                return jsonify({
                    'success': False,
                    'message': f'Faltan campos: {", ".join(missing_fields)}'
                }), 400
                
            sanitized_data = {k: html.escape(v) for k, v in data.items()}
            init_excel_file()
            save_to_excel(sanitized_data)
            email_sent = send_email(sanitized_data)
            
            return jsonify({
                'success': True,
                'message': 'Mensaje enviado correctamente'
            })
        
        except Exception as e:
            print(f"Error: {e}")
            return jsonify({
                'success': False,
                'message': 'Error al enviar el mensaje'
            }), 500
    else:
        return send_from_directory('templates', 'contactob.html')

@application.route('/<path:filename>')
def custom_static(filename):
    # Manejo de archivos estáticos genérico
    if filename.startswith('static/'):
        return send_from_directory('.', filename)
    elif filename.startswith('templates/'):
        return send_from_directory('.', filename)
    return "Not Found", 404

if __name__ == '__main__':
    os.makedirs('static/images', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    init_excel_file()
    application.run(port=5000, debug=True)