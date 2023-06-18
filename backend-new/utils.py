import re

def is_valid_cpf(cpf):
    cpf = ''.join(filter(str.isdigit, cpf))

    if len(cpf) != 11:
        return False

    if cpf == cpf[0] * 11:
        return False

    sum_ = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digit_1 = (sum_ * 10) % 11
    if digit_1 == 10:
        digit_1 = 0

    sum_ = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digit_2 = (sum_ * 10) % 11
    if digit_2 == 10:
        digit_2 = 0

    is_valid = cpf[-2:] == str(digit_1) + str(digit_2)
    return is_valid

def is_valid_email(email):
    if re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email):
        return True
    return False

def is_valid_phone_number(number):
    number = re.sub(r'\D', '', number)

    number_length = len(number)
    if not(number_length == 9 or number_length == 11 or number_length == 13):
        return False

    return True