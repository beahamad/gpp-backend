import requests
import unittest
import random
import string
from models import User

from app import app, db

def cpf_generate():
    #  Gera os primeiros nove dígitos (e certifica-se de que não são todos iguais)
    while True:
        cpf = [random.randint(0, 9) for i in range(9)]
        if cpf != cpf[::-1]:
            break

    #  Gera os dois dígitos verificadores
    for i in range(9, 11):
        value = sum((cpf[num] * ((i + 1) - num) for num in range(0, i)))
        digit = ((value * 10) % 11) % 10
        cpf.append(digit)

    #  Retorna o CPF como string
    result = ''.join(map(str, cpf))
    return str(result)


def gerar_user(cpf, email):
    return {'cpf': cpf, 'full_name': "Joao das Neves", "date_of_birth": "01/02/2001", "address": "rua groove", "email": email, "password": "senha32123"}


def gerar_email_valido():
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(7))

    return result_str + "@emailtest.com"

def gerar_confirmacao(email, codigo):
    return {"email": email, "confirmation_code": codigo}

def gerar_login(email, senha):
    return {"email": email, "password": senha}

# unittest.TestCase
class RegisterTest():

    #TODO
    #confirmar o codigo pegando diretamente no bd
    #salvar o token ao fazer login

    API_URL = "http://127.0.0.1:5000/api/"
    REGISTER_URL = "{}/register".format(API_URL)


    CPF_VALIDO = cpf_generate()
    EMAIL_VALIDO = gerar_email_valido()


    def setUp(self):
        #criando o contexto, esse codigo roda antes de cada teste
        app.app_context().push()
            

    def test_register_valido(self):

        #gera um user valido enquanto nao conseguimos deletar o user valido padrao do db
        usr = gerar_user(self.CPF_VALIDO, self.EMAIL_VALIDO)


        #teste valido
        r = requests.post(self.REGISTER_URL, json=usr)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.text, '{"message":"Confirmation code sent to your email"}\n')
        self.assertTrue(User.query.filter_by(cpf=self.CPF_VALIDO).first())
        #removendo usuario cadastrado no teste anterior
        user_valido_anterior = User.query.filter_by(cpf=self.CPF_VALIDO).first()
        db.session.delete(user_valido_anterior)
        db.session.commit()
        self.assertFalse(User.query.filter_by(cpf=self.CPF_VALIDO).first())

        
    def test_register_cpf_zero(self):
        
        #cpf zero
        r = requests.post(self.REGISTER_URL, json=gerar_user("0", "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"Invalid CPF"}\n')
        self.assertFalse(User.query.filter_by(email="joaozineves@email.com").first()) 
        
    def test_register_cpf_vazio(self):
        
        #cpf vazio
        r = requests.post(self.REGISTER_URL, json=gerar_user("", "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"Invalid CPF"}\n')
        self.assertFalse(User.query.filter_by(email="joaozineves@email.com").first()) 
        
    def test_register_cpf_menor(self):
        
        #cpf com menos digitos que o normal
        r = requests.post(self.REGISTER_URL, json=gerar_user("1234567891", "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"Invalid CPF"}\n')
        self.assertFalse(User.query.filter_by(email="joaozineves@email.com").first()) 
    
    def test_register_cpf_maior(self):

        #cpf com mais digitos que o normal
        r = requests.post(self.REGISTER_URL, json=gerar_user("123456789101", "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"Invalid CPF"}\n')
        self.assertFalse(User.query.filter_by(email="joaozineves@email.com").first()) 
        
    def test_register_cpf_invalido(self):
        
        #cpf nao validado
        r = requests.post(self.REGISTER_URL, json=gerar_user("12345678910", "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"Invalid CPF"}\n')
        self.assertFalse(User.query.filter_by(email="joaozineves@email.com").first()) 
        
    def test_register_cpf_repetido(self):
        
        #criando user valido e testando se foi cadastrado corretamente
        cpf = cpf_generate()
        usr = gerar_user(cpf, gerar_email_valido())
        r = requests.post(self.REGISTER_URL, json=usr)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.text, '{"message":"Confirmation code sent to your email"}\n')
        self.assertTrue(User.query.filter_by(cpf=cpf).first())

        #tentando cadastrar com o mesmo cpf do user acima
        r = requests.post(self.REGISTER_URL, json=gerar_user(cpf, "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"CPF already registered"}\n')
        self.assertFalse(User.query.filter_by(email="joaozineves@email.com").first()) 

        #removendo user criado do bd
        user_valido_anterior = User.query.filter_by(cpf=cpf).first()
        db.session.delete(user_valido_anterior)
        db.session.commit()
        self.assertFalse(User.query.filter_by(cpf=cpf).first())


class Confirm_registration_test(unittest.TestCase):

    API_URL = "http://127.0.0.1:5000/api/"
    CONFIRMATION_URL = "{}/confirm".format(API_URL)
    REGISTER_URL = "{}/register".format(API_URL)
    CURRENT_USER = ""

    def setUp(self):
        #registra um usuario para testar o codigo de confirmação
        app.app_context().push()
        cpf = cpf_generate()
        email = gerar_email_valido()
        usr = gerar_user(cpf, email)
        r = requests.post(self.REGISTER_URL, json=usr)
        self.CURRENT_USER = User.query.filter_by(cpf=cpf).first()
        self.assertTrue(self.CURRENT_USER)

    def tearDown(self):
        #apaga o user criado do bd
        cpf = self.CURRENT_USER.cpf
        db.session.delete(self.CURRENT_USER)
        db.session.commit()
        self.assertFalse(User.query.filter_by(cpf=cpf).first())
        self.CURRENT_USER = ""


    def test_confirm_valid(self):
        email = self.CURRENT_USER.email
        code = self.CURRENT_USER.confirmation_code
        self.assertTrue(User.query.filter_by(email=email, confirmed="f").first())
        r = requests.post(self.CONFIRMATION_URL, json=gerar_confirmacao(email, code))
        self.assertTrue(User.query.filter_by(email=email, confirmed="t").first())
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.text)

    def test_confirm_invalid_code(self):
        email = self.CURRENT_USER.email
        code = self.CURRENT_USER.confirmation_code
        self.assertNotEqual(code, "0000")
        self.assertTrue(User.query.filter_by(email=email, confirmed="f").first())
        r = requests.post(self.CONFIRMATION_URL, json=gerar_confirmacao(email, "0000"))
        self.assertTrue(User.query.filter_by(email=email, confirmed="f").first())
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.text, '{"error":"Invalid email or confirmation code"}\n')

class Login_test(unittest.TestCase):
    
    API_URL = "http://127.0.0.1:5000/api/"
    CONFIRMATION_URL = "{}/confirm".format(API_URL)
    REGISTER_URL = "{}/register".format(API_URL)
    LOGIN_URL = "{}/login".format(API_URL)
    CURRENT_USER = ""
    def setUp(self):
        #registra um usuario para testar o codigo de confirmação
        app.app_context().push()
        cpf = cpf_generate()
        email = gerar_email_valido()
        usr = gerar_user(cpf, email)
        r = requests.post(self.REGISTER_URL, json=usr)
        self.CURRENT_USER = User.query.filter_by(cpf=cpf).first()


    def tearDown(self):
        #apaga o user criado do bd
        cpf = self.CURRENT_USER.cpf
        db.session.delete(self.CURRENT_USER)
        db.session.commit()
        self.assertFalse(User.query.filter_by(cpf=cpf).first())
        self.CURRENT_USER = ""

    def test_login_valid(self):
        #confirmando o codigo antes
        code = self.CURRENT_USER.confirmation_code
        r = requests.post(self.CONFIRMATION_URL, json=gerar_confirmacao(self.CURRENT_USER.email, code))
        self.assertTrue(User.query.filter_by(email=self.CURRENT_USER.email, confirmed="t").first())
        #fazendo o login
        r = requests.post(self.LOGIN_URL, json=gerar_login(self.CURRENT_USER.email, self.CURRENT_USER.password))
        self.assertEqual(r.status_code, 200)
        self.assertTrue(r.text)

    def test_login_unconfirmed(self):
        #verificando se o user nao confirmou
        self.assertTrue(User.query.filter_by(email=self.CURRENT_USER.email, confirmed="f").first())
        #fazendo o login
        r = requests.post(self.LOGIN_URL, json=gerar_login(self.CURRENT_USER.email, self.CURRENT_USER.password))
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.text, '{"error":"user not confirmed"}\n')

    def test_login_invalid(self):
        r = requests.post(self.LOGIN_URL, json=gerar_login(self.CURRENT_USER.email, "senhaerrada"))
        self.assertEqual(r.status_code, 401)
        self.assertEqual(r.text, '{"error":"Invalid email or password"}\n')

if __name__ == '__main__':
    unittest.main()