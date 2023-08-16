# Mude o nome do arquivo para config.py e adicione o DATABASE_URL

# DATABASE_URL = "postgres://qemctjlh:fvfSCufnXlDu4qRr0L904XwsDcqNhCCd@babar.db.elephantsql.com/qemctjlh"
# DATABASE_URL = "postgres://fguqqogd:EefId-spP1uZCdCtrn_CG94V-yVVMdxj@babar.db.elephantsql.com/fguqqogd"

from configparser import ConfigParser


def get_config(filename="dbconfig.ini", section="postgresql"):
    parser = ConfigParser()
    parser.read(filename)
    db = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception("erro ao ler arquivo de configurações")
    return db

def get_uri():
    params = get_config()
    uri = f"postgresql://{params['user']}:{params['password']}@{params['host']}:{params['port']}/{params['database']}"
    return uri