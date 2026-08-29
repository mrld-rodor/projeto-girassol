import secrets
import time
import os
from datetime import timedelta
from functools import wraps

from flask import Flask, render_template, request, jsonify, session
from flask_session import Session
from dotenv import load_dotenv
import requests  # para verificar OTP (não necessário, mas deixarei para uso futuro)

from control.email_service import (
    Contato,
    send_email,
    EmailDeliveryError,
    EmailNetworkError,
)

load_dotenv()

# ============================================================
# Configuração do Flask
# ============================================================
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

# ============================================================
# Dicionário de códigos OTP (apenas em memória)
# ============================================================
otp_store = {}  # {email: {'code': '123456', 'expires': timestamp, 'attempts': 0, 'data': {...}}}

def generate_otp(email, form_data):
    """Gera um código OTP de 6 dígitos e armazena em memória"""
    code = f"{secrets.randbelow(1000000):06d}"
    otp_store[email] = {
        'code': code,
        'expires': time.time() + 600,  # 10 minutos
        'attempts': 0,
        'data': form_data,
    }
    return code

def validate_otp(email, code):
    """Valida o código e remove da memória se correto"""
    record = otp_store.get(email)
    if not record:
        return False, "Código não encontrado. Solicite um novo."
    
    if record['attempts'] >= 3:
        otp_store.pop(email, None)
        return False, "Limite de tentativas excedido. Solicite um novo código."
    
    if time.time() > record['expires']:
        otp_store.pop(email, None)
        return False, "Código expirado. Solicite um novo."
    
    if record['code'] != code:
        record['attempts'] += 1
        return False, "Código incorreto. Tente novamente."
    
    # Código correto
    otp_store.pop(email, None)
    return True, "Código validado com sucesso."

def send_otp_email(email, code):
    """Envia o e-mail com o código OTP usando o serviço Resend"""
    # Vamos reutilizar a infraestrutura de e-mail existente, mas adaptar para OTP
    try:
        # Enviar e-mail simples com código (podemos criar um template OTP)
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        # Configurações do e-mail (use as variáveis do Resend para API, mas aqui é um e-mail simples)
        # Para simplificar, usaremos o Resend API via requests, já que você já tem configurado
        payload = {
            'from': os.getenv('EMAIL_SENDER', 'Espaço Girassol <onboarding@resend.dev>'),
            'to': [email],
            'subject': 'Seu código de verificação - Espaço Girassol',
            'html': f"""
            <div style="font-family: Arial, sans-serif; max-width: 600px; margin: 0 auto; padding: 20px; background-color: #f7ebcb; border-radius: 10px;">
                <h2 style="color: #2f3a2e; text-align: center;">Espaço Girassol</h2>
                <p style="color: #3d4f3a; font-size: 16px;">Olá!</p>
                <p style="color: #3d4f3a; font-size: 16px;">Seu código de verificação para enviar a mensagem é:</p>
                <div style="text-align: center; margin: 20px 0; padding: 15px; background-color: #ffffff; border-radius: 8px; border: 2px solid #e89b16;">
                    <span style="font-size: 32px; font-weight: bold; color: #2f3a2e; letter-spacing: 10px;">{code}</span>
                </div>
                <p style="color: #7a4b1e; font-size: 14px;">Este código expira em 10 minutos.</p>
                <p style="color: #7a4b1e; font-size: 14px;">Se você não solicitou, ignore este e-mail.</p>
            </div>
            """
        }
        
        response = requests.post(
            'https://api.resend.com/emails',
            headers={
                'Authorization': f'Bearer {os.getenv("RESEND_API_KEY")}',
                'Content-Type': 'application/json',
            },
            json=payload,
            timeout=10,
        )
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"[ERROR] Falha ao enviar OTP: {e}")
        return False

# ============================================================
# Rotas
# ============================================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/enviar-contato', methods=['POST'])
def enviar_contato():
    """Primeira etapa: recebe os dados, gera OTP e envia código"""
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    servico = request.form.get('servico')
    mensagem = request.form.get('mensagem')

    # Validação básica
    if not nome or not email or not telefone or not servico or not mensagem:
        return jsonify({'success': False, 'message': 'Preencha todos os campos obrigatórios.'}), 400

    # Gera OTP
    code = generate_otp(email, {
        'nome': nome,
        'email': email,
        'telefone': telefone,
        'servico': servico,
        'mensagem': mensagem,
    })

    # Envia e-mail com código
    if not send_otp_email(email, code):
        return jsonify({'success': False, 'message': 'Não foi possível enviar o código. Verifique seu e-mail e tente novamente.'}), 500

    return jsonify({
        'success': True,
        'message': 'Código de verificação enviado para seu e-mail. Verifique sua caixa de entrada.',
        'requires_otp': True,
        'email': email
    })

@app.route('/verificar-codigo', methods=['POST'])
def verificar_codigo():
    """Segunda etapa: valida o código e envia o e-mail final"""
    email = request.form.get('email')
    code = request.form.get('code')

    if not email or not code:
        return jsonify({'success': False, 'message': 'Dados incompletos.'}), 400

    valid, message = validate_otp(email, code)

    if not valid:
        return jsonify({'success': False, 'message': message}), 400

    # Recupera os dados do formulário armazenados na memória
    record = otp_store.pop(email, None)
    if not record:
        return jsonify({'success': False, 'message': 'Sessão expirada. Preencha o formulário novamente.'}), 400

    data = record['data']
    contato = Contato(
        nome=data['nome'],
        email=data['email'],
        telefone=data['telefone'],
        servico=data['servico'],
        mensagem=data['mensagem'],
    )

    # Envia o e-mail final para a terapeuta
    try:
        send_email(contato)
        return jsonify({
            'success': True,
            'message': 'Mensagem enviada com sucesso! Em breve entraremos em contato.'
        })
    except EmailNetworkError as e:
        return jsonify({'success': False, 'message': f'Erro de conexão: {str(e)}'}), 503
    except EmailDeliveryError as e:
        return jsonify({'success': False, 'message': f'Erro ao enviar: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'success': False, 'message': f'Erro inesperado: {str(e)}'}), 500

# ============================================================
# Main
# ============================================================
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)