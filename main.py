from flask import Flask, render_template, url_for, request, redirect, flash
import csv
import os
import pandas as pd #especifico para tratar e manipular dados
from datetime import datetime

app = Flask(__name__)
# app.secrety_key

#nome do arquivo
csv_file = 'dados_pessoais.csv'

def int_csv():
    """inicializa o arquivo csv com cabeçalhos se não existir"""
    if not os.path.exists(csv_file):
        with open(csv_file, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Nome_Completo','Email','Telefone','Sexo','Cidade','Estado','Endereço'])

@app.route('/')
def index():
    return render_template('forms_limo.html')

@app.route('/processar', methods=['post'])
def processar_formulario():
    nome = request.form.get('nome')
    email = request.form.get('email')
    telefone = request.form.get('telefone')
    sexo = request.form.get('genero')
    cidade = request.form.get('cidade')
    estado = request.form.get('estado')
    endereco = request.form.get('endereco')
    data_nascimento = request.form.get('data_nascimento')


    with open(csv_file, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([nome, email, telefone, sexo, data_nascimento, cidade, estado, endereco])

    return redirect(url_for('tabela')) 



@app.route('/tabela')
def tabela():
    """Página para visualizar os dados salvos"""
    try:
        dados = []
        if os.path.exists(csv_file):
            with open(csv_file,'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                dados = list(reader)
            print(dados)
            return render_template('tabela.html', dados=dados)
    except Exception as e:
        flash(f'Erro ao carregar dados: {str(e)}', 'error')
        return redirect(url_for('tabela'))    



@app.route('/voltar', methods=['post'])
def voltar():
    return render_template('forms_limo.html')


if __name__ == '__main__':
    int_csv()
    app.run(debug=True)