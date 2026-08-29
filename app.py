import secrets
import os
from datetime import timedelta
from functools import wraps

from flask import Flask, render_template, request, jsonify
from flask_session import Session
from dotenv import load_dotenv
import requests
import time

from control.email_service import Contato, send_email, EmailDeliveryError, EmailNetworkError

load_dotenv()

app = Flask(
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))
app.config['SESSION_TYPE'] = 'cachelib'
app.config['SESSION_CACHELIB'] = {'type': 'simple'}
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=15)
Session(app)

# Dicionário para registrar timestamps de envio por IP (rate limit simples)
rate_limit = {}  # {ip: [timestamps]}
RATE_LIMIT_WINDOW = 60  # segundos
RATE_LIMIT_MAX = 3  # máximo de envios por janela

def is_rate_limited(ip):
    now = time.time()
    # Remove timestamps fora da janela
    rate_limit[ip] = [t for t in rate_limit.get(ip, []) if now - t < RATE_LIMIT_WINDOW]
    if len(rate_limit[ip]) >= RATE_LIMIT_MAX:
        return True
    rate_limit[ip].append(now)
    return False

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar-contato', methods=['POST'])
def enviar_contato():
    # 1. Verificação de Honeypot (campo invisível "website")
    honeypot = request.form.get('website', '')
    if honeypot:
        # Bot detectado - retorna sucesso falso para não revelar a proteção
        return jsonify({'success': True, 'message': 'Mensagem enviada!'})

    # 2. Verificação de tempo mínimo (se o formulário foi preenchido muito rápido, é bot)
    form_start = request.form.get('form_start', type=float)
    if form_start and (time.time() - form_start) < 2.0:
        # Tempo menor que 2 segundos -> provavelmente bot
        return jsonify({'success': False, 'message': 'Preencha o formulário com calma. Tente novamente.'}), 400

    # 3. Rate limit por IP (simples)
    ip = request.remote_addr
    if is_rate_limited(ip):
        return jsonify({'success': False, 'message': 'Muitas tentativas. Aguarde um minuto e tente novamente.'}), 429

    # 4. Captura dos dados
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    servico = request.form.get('servico')
    mensagem = request.form.get('mensagem')

    # Validação básica
    if not nome or not email or not telefone or not servico or not mensagem:
        return jsonify({'success': False, 'message': 'Preencha todos os campos obrigatórios.'}), 400

    # 5. Envio do e-mail
    contato = Contato(nome, email, telefone, servico, mensagem)

    try:
        send_email(contato)
        return jsonify({'success': True, 'message': 'Mensagem enviada com sucesso! Em breve entraremos em contato.'})
    except EmailNetworkError as e:
        return jsonify({'success': False, 'message': f'Erro de conexão: {str(e)}'}), 503
    except EmailDeliveryError as e:
        return jsonify({'success': False, 'message': f'Erro ao enviar: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro inesperado: {str(e)}'}), 500


@app.route('/politica-privacidade')
def politica_privacidade():
    return render_template('politica_privacidade.html')

@app.route('/termos-uso')
def termos_uso():
    return render_template('termos_uso.html')


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)