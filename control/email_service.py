import traceback
from html import escape

import requests
from flask import url_for

from control.email_config import (
    email_api_key,
    email_api_timeout,
    email_api_url,
    email_receiver,
    email_sender,
)


class EmailDeliveryError(Exception):
    """Erro base para falhas no envio de email."""


class EmailNetworkError(EmailDeliveryError):
    """Falha de conectividade com a API."""


class Contato:
    def __init__(self, nome, email, telefone, servico, mensagem):
        self.nome = nome
        self.email = email
        self.telefone = telefone
        self.servico = servico
        self.mensagem = mensagem


def _build_logo_url():
    return url_for(
        'static',
        filename='images/logo_logo_header.png',
        _external=True,
    )


def _build_plain_text(contato):
    return f"""
Novo contato no Espaço Girassol!

Nome: {contato.nome}
E-mail: {contato.email}
Telefone: {contato.telefone}
Serviço de interesse: {contato.servico}

Mensagem:
{contato.mensagem}
""".strip()


def _build_html_email(contato):
    nome = escape(contato.nome)
    email = escape(contato.email)
    telefone = escape(contato.telefone)
    servico = escape(contato.servico)
    mensagem = escape(contato.mensagem).replace('\n', '<br>')
    logo_url = _build_logo_url()

    return f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Novo contato - Espaço Girassol</title>
    </head>
    <body style="margin:0; padding:0; background-color:#f7ebcb; color:#2f3a2e; font-family:'Source Sans 3', 'Segoe UI', sans-serif;">
        <div style="background: radial-gradient(circle at top, #fffefb 0%, #f7ebcb 62%); padding: 32px 16px;">
            <table role="presentation" width="100%" cellspacing="0" cellpadding="0" border="0" style="max-width: 680px; margin: 0 auto; border-collapse: collapse;">
                <tr>
                    <td style="padding: 0;">
                        <!-- CARD PRINCIPAL -->
                        <div style="border:2px solid #f6c445; background: rgba(255,255,255,0.92); box-shadow: 0 22px 60px rgba(122,75,30,0.2); border-radius: 16px; overflow: hidden;">
                            
                            <!-- CABEÇALHO -->
                            <div style="padding: 32px 28px 24px; border-bottom: 2px solid #f6c445; text-align:center; background: linear-gradient(180deg, #fffefb 0%, #f7ebcb 100%);">
                                <div style="display:inline-block; padding: 8px 16px; border:1px solid #e89b16; border-radius: 9999px; color:#7a4b1e; font-size:11px; font-weight:700; letter-spacing:0.18em; text-transform:uppercase; background: rgba(255,255,255,0.8); box-shadow: 0 2px 8px rgba(232,155,22,0.15);">
                                    ✉️ Novo contato recebido
                                </div>
                                <div style="margin: 20px 0 12px;">
                                    <img src="{logo_url}" alt="Espaço Girassol" style="width: 140px; max-width: 140px; height: auto; display: inline-block; filter: drop-shadow(0 4px 12px rgba(122,75,30,0.15));">
                                </div>
                                <h1 style="margin: 0; color:#2f3a2e; font-family:'Cormorant Garamond', 'Times New Roman', serif; font-size:38px; font-weight:640; letter-spacing:0.02em; line-height: 1.1;">
                                    Espaço Girassol
                                </h1>
                                <p style="margin: 6px 0 0; color:#466b3a; font-size:13px; font-weight:600; letter-spacing:0.22em; text-transform:uppercase;">
                                    Terapias Integrativas
                                </p>
                            </div>

                            <!-- CORPO -->
                            <div style="padding: 30px 28px 8px;">
                                
                                <!-- REMETENTE -->
                                <div style="background: rgba(246,196,69,0.06); border:1px solid rgba(246,196,69,0.35); border-radius: 12px; padding: 20px 22px; margin-bottom: 20px;">
                                    <div style="color:#7a4b1e; text-transform:uppercase; letter-spacing:0.22em; font-size:10px; font-weight:700; margin-bottom:10px;">
                                        👤 Remetente
                                    </div>
                                    <div style="font-size:24px; color:#2f3a2e; font-family:'Cormorant Garamond', serif; font-weight:630; margin-bottom:4px;">
                                        {nome}
                                    </div>
                                    <div style="font-size:14px; color:#466b3a; letter-spacing:0.03em;">
                                        {email} &nbsp;•&nbsp; {telefone}
                                    </div>
                                </div>

                                <!-- SERVIÇO -->
                                <div style="margin-bottom: 20px;">
                                    <div style="color:#7a4b1e; text-transform:uppercase; letter-spacing:0.22em; font-size:10px; font-weight:700; margin-bottom:8px;">
                                        🌻 Serviço de interesse
                                    </div>
                                    <div style="background:#fffefb; border-left:4px solid #e89b16; border-radius: 8px; padding: 14px 18px; color:#2f3a2e; font-size:15px; font-weight:600; box-shadow: 0 2px 8px rgba(246,196,69,0.08);">
                                        {servico}
                                    </div>
                                </div>

                                <!-- MENSAGEM -->
                                <div style="margin-bottom: 24px;">
                                    <div style="color:#7a4b1e; text-transform:uppercase; letter-spacing:0.22em; font-size:10px; font-weight:700; margin-bottom:8px;">
                                        💬 Mensagem
                                    </div>
                                    <div style="background:#fffefb; border-left:4px solid #e89b16; border-radius: 8px; padding: 20px 22px; color:#3d4f3a; font-size:15px; line-height:1.8; box-shadow: 0 2px 8px rgba(246,196,69,0.08);">
                                        {mensagem}
                                    </div>
                                </div>

                                <!-- BOTÃO RESPONDER -->
                                <div style="text-align:center; margin: 28px 0 10px;">
                                    <a href="mailto:{email}" style="display:inline-block; padding:14px 32px; background: linear-gradient(135deg, #e89b16 0%, #d88e0f 100%); color:#2b1a0a; text-decoration:none; border-radius:9999px; font-size:13px; font-weight:700; letter-spacing:0.12em; text-transform:uppercase; box-shadow: 0 8px 24px rgba(232,155,22,0.35); border: 1px solid rgba(255,255,255,0.3);">
                                        Responder contato
                                    </a>
                                </div>
                            </div>

                            <!-- RODAPÉ -->
                            <div style="padding: 20px 28px 26px; text-align:center; border-top:1px solid rgba(246,196,69,0.25); background: rgba(247,235,203,0.4); color:#7a4b1e; font-size:11px; letter-spacing:0.14em; text-transform:uppercase;">
                                <div style="margin-bottom: 8px;">
                                    🌻 Enviado automaticamente pelo formulário do site
                                </div>
                                <div style="color:#466b3a; font-weight:600;">
                                    Espaço Girassol • Terapias Integrativas
                                </div>
                            </div>
                        </div>
                    </td>
                </tr>
            </table>
        </div>
    </body>
    </html>
    """.strip()


def send_email(contato):
    html_body = _build_html_email(contato)
    text_body = _build_plain_text(contato)

    if not email_api_key or not email_sender or not email_receiver:
        missing = []
        if not email_api_key:
            missing.append('RESEND_API_KEY')
        if not email_sender:
            missing.append('EMAIL_SENDER')
        if not email_receiver:
            missing.append('EMAIL_RECEIVER')
        raise EmailDeliveryError(
            f"Configuracao de email incompleta: {', '.join(missing)}"
        )

    try:
        payload = {
            'from': email_sender,
            'to': [email_receiver],
            'subject': f'Novo contato no Espaço Girassol - {contato.nome}',
            'reply_to': contato.email,
            'html': html_body,
            'text': text_body,
        }

        response = requests.post(
            email_api_url,
            headers={
                'Authorization': f'Bearer {email_api_key}',
                'Content-Type': 'application/json',
            },
            json=payload,
            timeout=email_api_timeout,
        )
        response.raise_for_status()
        print('[INFO] Email enviado com sucesso via API HTTP.')
        return 202
    except requests.exceptions.Timeout as e:
        print(f"[ERROR] Timeout ao enviar email via API HTTP: {e}")
        print(traceback.format_exc())
        raise EmailNetworkError('Timeout na comunicacao com o provedor de email') from e
    except requests.exceptions.ConnectionError as e:
        print(f"[ERROR] Falha de conexao com a API de email: {e}")
        print(traceback.format_exc())
        raise EmailNetworkError('Provedor de email indisponivel ou inacessivel') from e
    except requests.exceptions.HTTPError as e:
        response_body = ''
        if e.response is not None:
            response_body = e.response.text
        print(f"[ERROR] API de email retornou erro HTTP: {response_body}")
        print(traceback.format_exc())
        raise EmailDeliveryError('Provedor de email rejeitou a solicitacao') from e
    except Exception as e:
        print(f"[ERROR] Erro ao enviar e-mail: {e}")
        print(traceback.format_exc())
        raise EmailDeliveryError("Erro inesperado ao enviar email") from e