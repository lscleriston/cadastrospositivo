from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, FileField, SelectField, SelectMultipleField
from wtforms.validators import DataRequired, Optional
import pandas as pd

# Carregar a lista de certificações a partir do arquivo Excel
try:
    certifications_df = pd.read_excel('data/certificacao.xlsx')
    certifications = [('', 'Selecione uma certificação')] + [(row['Certificacao'], row['Certificacao']) for index, row in certifications_df.iterrows()]
except FileNotFoundError:
    certifications = [('', 'Selecione uma certificação')]

# Carregar a lista de torres de atendimento a partir do arquivo Excel
try:
    torres_df = pd.read_excel('data/torre.xlsx')
    torres = [(row['Torre'], row['Torre']) for index, row in torres_df.iterrows()]
except FileNotFoundError:
    torres = []

# Carregar a lista de operações a partir do arquivo Excel
try:
    operacoes_df = pd.read_excel('data/Relacao de Clientes.xlsx')
    operacoes = [(row['Operacao'], row['Operacao']) for index, row in operacoes_df.iterrows()]
except FileNotFoundError:
    operacoes = []

class LoginForm(FlaskForm):
    matricula = StringField('Matrícula', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    name = StringField('Nome Completo', validators=[DataRequired()])
    matricula = StringField('Matrícula', validators=[DataRequired()])
    password = PasswordField('Senha', validators=[DataRequired()])
    submit = SubmitField('Cadastrar')

class UserForm(FlaskForm):
    name = StringField('Nome Completo', validators=[DataRequired()])
    matricula = StringField('Matrícula', validators=[DataRequired()])
    torre = SelectField('Torre de Atendimento', choices=torres, validators=[DataRequired()])
    operacao_principal = SelectField('Operação Principal', choices=operacoes, validators=[DataRequired()])
    operacao_compartilhado = SelectMultipleField('Operação Compartilhado', choices=operacoes, validators=[DataRequired()])
    conhecimento = TextAreaField('Conhecimento (Ferramentas e Tecnologias)', validators=[DataRequired()])
    cursos_treinamentos = TextAreaField('Curso/Treinamentos')
    certification = SelectField('Certificação', choices=certifications, validators=[Optional()])
    file = FileField('Anexar Certificado', validators=[Optional()])
    graduacao = StringField('Curso de nível Superior / Pós-Graduação', validators=[Optional()])
    file_graduacao = FileField('Anexar Arquivo de Graduação', validators=[Optional()])
    submit = SubmitField('Salvar')