from flask import Flask, render_template,  request, jsonify
from control.email_service import Contato, send_email, EmailDeliveryError, EmailNetworkError



app = Flask(
    __name__,
    template_folder='app/templates',
    static_folder='app/static'
)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/enviar-contato', methods=['POST'])
def enviar_contato():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    servico = request.form.get('servico')
    mensagem = request.form.get('mensagem')

    contato = Contato(
        nome=nome,
        email=email,
        telefone=telefone,
        servico=servico,
        mensagem=mensagem
    )

    try:
        send_email(contato)
        return jsonify({
            'success': True,
            'message': 'Mensagem enviada com sucesso! Em breve entraremos em contato.'
        })
    except EmailNetworkError as e:
        return jsonify({
            'success': False,
            'message': f'Erro de conexão: {str(e)}'
        }), 503
    except EmailDeliveryError as e:
        return jsonify({
            'success': False,
            'message': f'Erro ao enviar: {str(e)}'
        }), 500
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'Erro inesperado: {str(e)}'
        }), 500




if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
