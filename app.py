from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_mysqldb import MySQL
from datetime import datetime  # Importando o módulo datetime
from datetime import timedelta
import sqlite3

app = Flask(__name__)

# Configurações do MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'shalon'

mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('home-page.html')

@app.route('/login', methods=['GET'])
def login():
    return render_template('login.html')  # Renderiza o formulário de login

@app.route('/login', methods=['POST'])
def logar():
    username = request.form['username']
    password = request.form['password']
    
    # Exemplo de validação simples
    if username == 'feliciano' and password == '123456':
        return render_template('agendado.html')  # Redireciona para a página agendada
    
    elif username == 'kawana' and password == '123456':
        return render_template('manicure.html')  # Redireciona para a página agendada
    
    elif username == 'silveria' and password == '123456':
        return render_template('confirmacao.html')  # Redireciona para a página agendada
    else:
        return render_template('login.html')


@app.route('/esmalteria')
def esmalteria():
    return render_template('esmalteria.html')

@app.route('/podologia')
def podologia():
    return render_template('podologia.html')

@app.route('/manicure')
def manicure():
    return render_template('manicure.html')

#===============================  MANICURE  ===============================================

@app.route('/m1agendamento')
def m1agendamento():
    return render_template('agenda1manicure.html')

@app.route('/m2agendamento')
def m2agendamento():
    return render_template('agenda2manicure.html')

@app.route('/m3agendamento')
def m3agendamento():
    return render_template('agenda3manicure.html')

@app.route('/m4agendamento')
def m4agendamento():
    return render_template('agenda4manicure.html')

@app.route('/m5agendamento')
def m5agendamento():
    return render_template('agenda5manicure.html')

#==============================================================================
@app.route('/agenda1manicure', methods=['POST'])
def agenda1manicure():
    # Pegando os dados do formulário
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']

    # Inserir no banco de dados
    cursor = mysql.connection.cursor()
    query = "INSERT INTO agendamentomanicure (nome, contato, data, horario, pagamento) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (nome, contato, data, horario, pagamento))
    mysql.connection.commit()

    # Converter a string da data para um objeto datetime
    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    # Processando os dados e retornando a confirmação
    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)


@app.route('/agenda2manicure', methods=['POST'])
def agenda2manicure():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']

    # Criação de uma lista com os 2 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentomanicure WHERE data = %s AND horario IN (%s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return "Serviço selecionado não está disponível por esse horario. Por favor, escolha outros horários."

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentomanicure (nome, contato, data, horario, pagamento) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, contato, data, h, pagamento))
    mysql.connection.commit()

    # Converter a string da data para um objeto datetime
    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao1.html', data=data_formatada, horarios=horarios, pagamento=pagamento)


@app.route('/agenda3manicure', methods=['POST'])
def agenda3manicure():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']

    # Criação de uma lista com os 3 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:  
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+60min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentomanicure WHERE data = %s AND horario IN (%s, %s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1], horarios[2]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return "Um ou mais horários selecionados já estão ocupados. Por favor, escolha outros horários."

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentomanicure (nome, contato, data, horario, pagamento) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, contato, data, h, pagamento))
    mysql.connection.commit()

    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao1.html', data=data_formatada, horarios=horarios, pagamento=pagamento)


@app.route('/agenda4manicure', methods=['POST'])
def agenda4manicure():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']

    # Criação de uma lista com os 4 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+60min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+90min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentomanicure WHERE data = %s AND horario IN (%s, %s, %s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1], horarios[2], horarios[3]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return "Um ou mais horários selecionados já estão ocupados. Por favor, escolha outros horários."

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentomanicure (nome, contato, data, horario, pagamento) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, contato, data, h, pagamento))
    mysql.connection.commit()

    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao1.html', data=data_formatada, horarios=horarios, pagamento=pagamento)


@app.route('/agenda5manicure', methods=['POST'])
def agenda5manicure():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']

    # Criação de uma lista com os 4 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+60min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+90min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+120min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+150min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+180min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+210min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+240min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+270min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")


    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentomanicure WHERE data = %s AND horario IN (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1], horarios[2], horarios[3],horarios[4], horarios[5], horarios[6], horarios[7], horarios[8], horarios[9]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return "Um ou mais horários selecionados já estão ocupados. Por favor, escolha outros horários."

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentomanicure (nome, contato, data, horario, pagamento) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, contato, data, h, pagamento))
    mysql.connection.commit()

    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao1.html', data=data_formatada, horarios=horarios, pagamento=pagamento)













#===============================  PODOLOGIA  ===============================================
@app.route('/p1agendamento')
def p1agendamento():
    return render_template('agenda1podologia.html')

@app.route('/p2agendamento')
def p2agendamento():
    return render_template('agenda2podologia.html')

@app.route('/p3agendamento')
def p3agendamento():
    return render_template('agenda3podologia.html')

@app.route('/p4agendamento')
def p4agendamento():
    return render_template('agenda4podologia.html')

@app.route('/p5agendamento')
def p5agendamento():
    return render_template('agenda5podologia.html')


#==============================================================================
@app.route('/agenda1podologia', methods=['POST'])
def agenda1podologia():
    # Pegando os dados do formulário
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']

    # Inserir no banco de dados
    cursor = mysql.connection.cursor()
    query = "INSERT INTO agendamentopodologia (nome, contato, data, horario, pagamento) VALUES (%s, %s, %s, %s, %s)"
    cursor.execute(query, (nome, contato, data, horario, pagamento))
    mysql.connection.commit()

    # Converter a string da data para um objeto datetime
    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    # Processando os dados e retornando a confirmação
    return render_template('confirmacao.html', data=data_formatada, horario=horario, pagamento=pagamento)


@app.route('/agenda2podologia', methods=['POST'])
def agenda2podologia():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']

    # Criação de uma lista com os 2 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentopodologia WHERE data = %s AND horario IN (%s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return "Serviço selecionado não está disponível por esse horario. Por favor, escolha outros horários."

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentopodologia (nome, contato, data, horario, pagamento) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, contato, data, h, pagamento))
    mysql.connection.commit()

    # Converter a string da data para um objeto datetime
    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao1.html', data=data_formatada, horarios=horarios, pagamento=pagamento)


@app.route('/agenda3podologia', methods=['POST'])
def agenda3podologia():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']

    # Criação de uma lista com os 3 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:  
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+60min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentopodologia WHERE data = %s AND horario IN (%s, %s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1], horarios[2]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return "Um ou mais horários selecionados já estão ocupados. Por favor, escolha outros horários."

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentopodologia (nome, contato, data, horario, pagamento) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, contato, data, h, pagamento))
    mysql.connection.commit()

    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao1.html', data=data_formatada, horarios=horarios, pagamento=pagamento)


@app.route('/agenda4podologia', methods=['POST'])
def agenda4podologia():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']

    # Criação de uma lista com os 4 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+60min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+90min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentopodologia WHERE data = %s AND horario IN (%s, %s, %s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1], horarios[2], horarios[3]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return "Um ou mais horários selecionados já estão ocupados. Por favor, escolha outros horários."

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentopodologia (nome, contato, data, horario, pagamento) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, contato, data, h, pagamento))
    mysql.connection.commit()

    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao1.html', data=data_formatada, horarios=horarios, pagamento=pagamento)


@app.route('/agenda5podologia', methods=['POST'])
def agenda5podologia():
    nome = request.form['nome']
    contato = request.form['contato']
    data = request.form['data']
    horario = request.form['horario']
    pagamento = request.form['pagamento']

    # Criação de uma lista com os 4 horários
    horarios = []
    hora, minuto = map(int, horario.split(':'))

    # Adiciona o horário selecionado
    horarios.append(f"{hora:02d}:{minuto:02d}")
    
    # Adiciona o próximo horário (+30min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+60min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+90min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+120min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+150min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+180min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+210min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+240min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")

    # Adiciona o próximo horário (+270min)
    minuto += 30
    if minuto >= 60:
        minuto -= 60
        hora += 1
    horarios.append(f"{hora:02d}:{minuto:02d}")


    # Verificar se os horários já estão ocupados no banco de dados
    cursor = mysql.connection.cursor()
    query = "SELECT COUNT(*) FROM agendamentopodologia WHERE data = %s AND horario IN (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, (data, horarios[0], horarios[1], horarios[2], horarios[3],horarios[4], horarios[5], horarios[6], horarios[7], horarios[8], horarios[9]))  
    result = cursor.fetchone()

    if result[0] > 0:
        return "Um ou mais horários selecionados já estão ocupados. Por favor, escolha outros horários."

    # Inserir os horários no banco de dados, caso estejam livres
    for h in horarios:
        query = "INSERT INTO agendamentopodologia (nome, contato, data, horario, pagamento) VALUES (%s, %s, %s, %s, %s)"
        cursor.execute(query, (nome, contato, data, h, pagamento))
    mysql.connection.commit()

    data_obj = datetime.strptime(data, '%Y-%m-%d')
    data_formatada = data_obj.strftime('%d-%m-%Y')

    return render_template('confirmacao1.html', data=data_formatada, horarios=horarios, pagamento=pagamento)



#==========================================================================================================================
#==========================================================================================================================
@app.route('/agendado')
def agendado():
    return render_template('agendado.html')


@app.route('/get_horarios/<data>')
def get_horarios(data):
    # Conectar ao banco de dados
    cursor = mysql.connection.cursor()

    # A data será recebida como parâmetro na URL, no formato 'YYYY-MM-DD'
    querry = "SELECT horario FROM agendamentomanicure WHERE data = %s"
    cursor.execute(querry, (data,))  # Passando a data como parâmetro seguro

    agendamentos = cursor.fetchall()

    horario_agendado = []
    for agendamento in agendamentos:
        # Verifica se agendamento[0] é do tipo timedelta
        if isinstance(agendamento[0], timedelta):
            horas = agendamento[0].seconds // 3600
            minutos = (agendamento[0].seconds % 3600) // 60
            horario_agendado.append(f"{horas:02}:{minutos:02}")
        else:
            # Caso contrário, assume-se que é um datetime
            horario_agendado.append(agendamento[0].strftime('%H:%M'))  # Converte para 'HH:MM'

    cursor.close()  # Fecha o cursor

    return jsonify(horario_agendado)  # Retorna os horários em formato JSON



@app.route('/get_horariop/<data>')
def get_horariop(data):
    # Conectar ao banco de dados
    cursor = mysql.connection.cursor()

    # A data será recebida como parâmetro na URL, no formato 'YYYY-MM-DD'
    querry = "SELECT horario FROM agendamentopodologia WHERE data = %s"
    cursor.execute(querry, (data,))  # Passando a data como parâmetro seguro

    agendamentos = cursor.fetchall()

    horario_agendado = []
    for agendamento in agendamentos:
        # Verifica se agendamento[0] é do tipo timedelta
        if isinstance(agendamento[0], timedelta):
            horas = agendamento[0].seconds // 3600
            minutos = (agendamento[0].seconds % 3600) // 60
            horario_agendado.append(f"{horas:02}:{minutos:02}")
        else:
            # Caso contrário, assume-se que é um datetime
            horario_agendado.append(agendamento[0].strftime('%H:%M'))  # Converte para 'HH:MM'

    cursor.close()  # Fecha o cursor

    return jsonify(horario_agendado)  # Retorna os horários em formato JSON


#==========================================================================================================================
#==========================================================================================================================


if __name__ == '__main__':
    app.run(debug=True)

