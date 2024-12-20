from flask import current_app as app, render_template, redirect, url_for, flash, session, request
from app.forms import LoginForm, RegistrationForm, UserForm
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import csv
import os

UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'pdf', 'jpg', 'png'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        matricula = form.matricula.data
        password = form.password.data
        # Verificar as credenciais no arquivo CSV
        with open('users.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 3 and row[1] == matricula and check_password_hash(row[2], password):
                    session['user'] = {'name': row[0], 'matricula': row[1]}
                    flash('Login bem-sucedido!', 'success')
                    return redirect(url_for('user_form'))  # Redirecionar para a página de formulário
        flash('Matrícula ou senha incorretos.', 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        # Salvar os dados do usuário no arquivo CSV
        with open('users.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([form.name.data, form.matricula.data, hashed_password])
        flash('Cadastro realizado com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/user_form', methods=['GET', 'POST'])
def user_form():
    form = UserForm()
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    if form.validate_on_submit():
        # Verificar se a certificação foi selecionada e o arquivo foi anexado
        if form.certification.data and not form.file.data:
            flash('Por favor, anexe o arquivo de certificação.', 'danger')
            return render_template('user_form.html', form=form)

        # Verificar se o curso de graduação foi preenchido e o arquivo foi anexado
        if form.graduacao.data and not form.file_graduacao.data:
            flash('Por favor, anexe o arquivo do curso de graduação.', 'danger')
            return render_template('user_form.html', form=form)

        # Ler o conteúdo do arquivo CSV
        rows = []
        user_found = False
        with open('user_data.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 8 and row[1] == user['matricula']:
                    # Atualizar a linha existente
                    row[0] = form.name.data
                    row[2] = form.torre.data
                    row[3] = form.operacao_principal.data
                    row[4] = ';'.join(form.operacao_compartilhado.data)
                    row[5] = form.conhecimento.data
                    row[6] = form.cursos_treinamentos.data
                    row[7] = form.graduacao.data
                    user_found = True
                rows.append(row)

        # Se o usuário não foi encontrado, adicionar uma nova linha
        if not user_found:
            rows.append([form.name.data, form.matricula.data, form.torre.data, form.operacao_principal.data, ';'.join(form.operacao_compartilhado.data), form.conhecimento.data, form.cursos_treinamentos.data, form.graduacao.data])

        # Escrever o conteúdo atualizado de volta ao arquivo CSV
        with open('user_data.csv', mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(rows)

        # Lidar com o upload de arquivos de certificação
        if form.file.data and allowed_file(form.file.data.filename):
            filename = secure_filename(form.file.data.filename)
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user['matricula'])
            os.makedirs(user_folder, exist_ok=True)
            file_path = os.path.join(user_folder, filename)
            form.file.data.save(file_path)

            # Salvar a informação do arquivo no user_files.csv
            with open('user_files.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([user['matricula'], filename, form.certification.data])

        # Lidar com o upload de arquivos de graduação
        if form.file_graduacao.data and allowed_file(form.file_graduacao.data.filename):
            filename = secure_filename(form.file_graduacao.data.filename)
            user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user['matricula'])
            os.makedirs(user_folder, exist_ok=True)
            file_path = os.path.join(user_folder, filename)
            form.file_graduacao.data.save(file_path)

            # Salvar a informação do arquivo no user_file_graduacao.csv
            with open('user_file_graduacao.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([user['matricula'], filename, form.graduacao.data])

        flash('Dados salvos com sucesso!', 'success')
        return redirect(url_for('user_form'))

    # Carregar dados existentes do usuário
    if request.method == 'GET':
        with open('user_data.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                if len(row) >= 8 and row[1] == user['matricula']:
                    form.name.data = row[0]
                    form.matricula.data = row[1]
                    form.torre.data = row[2]
                    form.operacao_principal.data = row[3]
                    form.operacao_compartilhado.data = row[4].split(';')
                    form.conhecimento.data = row[5]
                    form.cursos_treinamentos.data = row[6]
                    form.graduacao.data = row[7]
                    break

    # Carregar arquivos do usuário
    user_files = []
    with open('user_files.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3 and row[0] == user['matricula']:
                user_files.append({'filename': row[1], 'certification': row[2]})

    # Carregar arquivos de graduação do usuário
    user_files_graduacao = []
    with open('user_file_graduacao.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3 and row[0] == user['matricula']:
                user_files_graduacao.append({'filename': row[1], 'graduacao': row[2]})

    return render_template('user_form.html', form=form, user_files=user_files, user_files_graduacao=user_files_graduacao)

@app.route('/delete_file/<filename>', methods=['POST'])
def delete_file(filename):
    user = session.get('user')
    if not user:
        return redirect(url_for('login'))

    user_folder = os.path.join(app.config['UPLOAD_FOLDER'], user['matricula'])
    file_path = os.path.join(user_folder, filename)

    # Remover o arquivo do sistema de arquivos
    if os.path.exists(file_path):
        os.remove(file_path)

    # Remover a entrada do arquivo do user_files.csv
    rows = []
    with open('user_files.csv', mode='r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) >= 3 and (row[0] != user['matricula'] or row[1] != filename):
                rows.append(row)

    with open('user_files.csv', mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(rows)

    flash('Arquivo excluído com sucesso!', 'success')
    return redirect(url_for('user_form'))