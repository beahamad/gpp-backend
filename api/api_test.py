import requests
import unittest
import random
import string
from models import User

from app import db

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


class ApiTest(unittest.TestCase):

    #funcao pra verificar usuarios no bd
    #remover usuarios apos teste
    #confirmar o codigo pegando diretamente no bd
    #salvar o token ao fazer login

    API_URL = "http://127.0.0.1:5000/api/"
    REGISTER_URL = "{}/register".format(API_URL)


    CPF_VALIDO = cpf_generate()
    EMAIL_VALIDO = gerar_email_valido()
    #USER_VALIDO = {'cpf': CPF_VALIDO, 'full_name': "Joaquim Silva", "date_of_birth": "01/01/1959", "address": "centro", "email": "joaquim@email.com", "password": "senha32123"}

    #USER_CPF_INVALIDO = {'cpf': "0", 'full_name': "Joao das Neves", "date_of_birth": "01/02/2001", "address": "rua groove", "email": "joaozineves@email.com", "password": "senha32123"}


    def test_register(self):

        #falta colocar o contexto para poder acessar o BD e realizar os testes
        #por algum motivo, ele está considerando isso tudo como apenas um teste





        #removendo usuario cadastrado no teste anterior
        #user_valido_anterior = User.query.filter_by(email="joaquim@email.com").first()
        #db.session.delete(user_valido_anterior)
        #db.session.commit()

        #gera um user valido enquanto nao conseguimos deletar o user valido padrao do db
        usr = gerar_user(ApiTest.CPF_VALIDO, ApiTest.EMAIL_VALIDO)


        #teste valido
        r = requests.post(ApiTest.REGISTER_URL, json=usr)
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.text, '{"message":"Confirmation code sent to your email"}\n')
        #self.assertTrue(User.query.filter_by(cpf=ApiTest.USER_VALIDO["cpf"]).first())


        #cpf zero
        r = requests.post(ApiTest.REGISTER_URL, json=gerar_user("0", "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"Invalid CPF"}\n')
        #self.assertFalse(User.query.filter_by(email="joaozineves@email.com".first()))

        #cpf vazio
        r = requests.post(ApiTest.REGISTER_URL, json=gerar_user("", "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"Invalid CPF"}\n')
        #self.assertFalse(User.query.filter_by(email="joaozineves@email.com".first()))
        
        #cpf com menos digitos que o normal
        r = requests.post(ApiTest.REGISTER_URL, json=gerar_user("1234567891", "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"Invalid CPF"}\n')
        #self.assertFalse(User.query.filter_by(email="joaozineves@email.com".first()))

        #cpf com mais digitos que o normal
        r = requests.post(ApiTest.REGISTER_URL, json=gerar_user("123456789101", "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"Invalid CPF"}\n')
        #self.assertFalse(User.query.filter_by(email="joaozineves@email.com".first()))
                         
        #cpf nao validado
        r = requests.post(ApiTest.REGISTER_URL, json=gerar_user("12345678910", "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"Invalid CPF"}\n')
        #self.assertFalse(User.query.filter_by(email="joaozineves@email.com".first()))
        
        #cpf repetido
        r = requests.post(ApiTest.REGISTER_URL, json=gerar_user(ApiTest.CPF_VALIDO, "joaozineves@email.com"))
        self.assertEqual(r.status_code, 400)
        self.assertEqual(r.text, '{"error":"CPF already registered"}\n')
        #self.assertFalse(User.query.filter_by(email="joaozineves@email.com".first()))
        
                


if __name__ == '__main__':
    unittest.main()