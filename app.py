from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
import sqlite3

app = Flask(__name__)

# Configurações de banco de dados
def init_db():
    conn = sqlite3.connect('agendamentos.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS agendamentos 
                 (id INTEGER PRIMARY KEY, nome TEXT, telefone TEXT, data TEXT, horario TEXT)''')
    conn.commit()
    conn.close()

# Homepage com calendário
@app.route('/')
def index():
    return render_template('index.html')

# Verificar disponibilidade de horários
@app.route('/disponibilidade', methods=['POST'])
def disponibilidade():
    data = request.form['data']
    conn = sqlite3.connect('agendamentos.db')
    c = conn.cursor()
    c.execute("SELECT horario FROM agendamentos WHERE data = ?", (data,))
    agendamentos = c.fetchall()
    horarios_ocupados = [a[0] for a in agendamentos]
    horarios_disponiveis = [f"{h}:00" for h in range(9, 19) if f"{h}:00" not in horarios_ocupados]
    conn.close()
    return render_template('disponibilidade.html', data=data, horarios=horarios_disponiveis)

# Realizar o agendamento
@app.route('/agendar', methods=['POST'])
def agendar():
    nome = request.form['nome']
    telefone = request.form['telefone']
    data = request.form['data']
    horario = request.form['horario']
    conn = sqlite3.connect('agendamentos.db')
    c = conn.cursor()
    c.execute("INSERT INTO agendamentos (nome, telefone, data, horario) VALUES (?, ?, ?, ?)", 
              (nome, telefone, data, horario))
    conn.commit()
    conn.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
