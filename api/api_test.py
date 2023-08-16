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


<<<<<<< HEAD
    def test_register1(self):
=======
    def setUp(self):
        #criando o contexto, esse codigo roda antes de cada teste
        app.app_context().push()
            
>>>>>>> 10bc771b42374a32ecd1e589157cf6b5c1acf1c2

    def test_register_valido(self):

        #gera um user valido enquanto nao conseguimos deletar o user valido padrao do db
        usr = gerar_user(self.CPF_VALIDO, self.EMAIL_VALIDO)


        #teste valido
        r = requests.post(self.REGISTER_URL, json=usr)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.text, '{"message":"Confirmation code sent to your email"}\n')
<<<<<<< HEAD
        #self.assertTrue(User.query.filter_by(cpf=ApiTest.USER_VALIDO["cpf"]).first())
        
    def test_register2(self):
        usr = gerar_user(ApiTest.CPF_VALIDO, ApiTest.EMAIL_VALIDO)
=======
        self.assertTrue(User.query.filter_by(cpf=self.CPF_VALIDO).first())
        #removendo usuario cadastrado no teste anterior
        user_valido_anterior = User.query.filter_by(cpf=self.CPF_VALIDO).first()
        db.session.delete(user_valido_anterior)
        db.session.commit()
        self.assertFalse(User.query.filter_by(cpf=self.CPF_VALIDO).first())

        
    def test_register_cpf_zero(self):
>>>>>>> 10bc771b42374a32ecd1e589157cf6b5c1acf1c2
        
        #cpf zero
        r = requests.post(self.REGISTER_URL, json=gerar_user("0", "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"Invalid CPF"}\n')
<<<<<<< HEAD
        #self.assertFalse(User.query.filter_by(email="joaozineves@email.com".first()))
        
    def test_register3(self):
        usr = gerar_user(ApiTest.CPF_VALIDO, ApiTest.EMAIL_VALIDO)
=======
        self.assertFalse(User.query.filter_by(email="joaozineves@email.com").first()) 
        
    def test_register_cpf_vazio(self):
>>>>>>> 10bc771b42374a32ecd1e589157cf6b5c1acf1c2
        
        #cpf vazio
        r = requests.post(self.REGISTER_URL, json=gerar_user("", "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"Invalid CPF"}\n')
        self.assertFalse(User.query.filter_by(email="joaozineves@email.com").first()) 
        
    def test_register_cpf_menor(self):
        
    def test_register4(self):
        usr = gerar_user(ApiTest.CPF_VALIDO, ApiTest.EMAIL_VALIDO)
        
        #cpf com menos digitos que o normal
        r = requests.post(self.REGISTER_URL, json=gerar_user("1234567891", "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"Invalid CPF"}\n')
<<<<<<< HEAD
        #self.assertFalse(User.query.filter_by(email="joaozineves@email.com".first()))
    
    def test_register5(self):
        usr = gerar_user(ApiTest.CPF_VALIDO, ApiTest.EMAIL_VALIDO)
        
=======
        self.assertFalse(User.query.filter_by(email="joaozineves@email.com").first()) 
    
    def test_register_cpf_maior(self):

>>>>>>> 10bc771b42374a32ecd1e589157cf6b5c1acf1c2
        #cpf com mais digitos que o normal
        r = requests.post(self.REGISTER_URL, json=gerar_user("123456789101", "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"Invalid CPF"}\n')
<<<<<<< HEAD
        #self.assertFalse(User.query.filter_by(email="joaozineves@email.com".first()))
        
    def test_register6(self):
        usr = gerar_user(ApiTest.CPF_VALIDO, ApiTest.EMAIL_VALIDO)
        
        #cpf nao validado
        r = requests.post(ApiTest.REGISTER_URL, json=gerar_user("12345678910", "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"Invalid CPF"}\n')
        #self.assertFalse(User.query.filter_by(email="joaozineves@email.com".first()))
        
    def test_register7(self):
        usr = gerar_user(ApiTest.CPF_VALIDO, ApiTest.EMAIL_VALIDO)
        
        #cpf repetido
        r = requests.post(ApiTest.REGISTER_URL, json=gerar_user(ApiTest.CPF_VALIDO, "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"CPF already registered"}\n')
        #self.assertFalse(User.query.filter_by(email="joaozineves@email.com".first())) 
=======
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

>>>>>>> 10bc771b42374a32ecd1e589157cf6b5c1acf1c2
        
if __name__ == '__main__':
    unittest.main()