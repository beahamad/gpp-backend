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


class RegisterTest(unittest.TestCase):

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

        
if __name__ == '__main__':
    unittest.main()