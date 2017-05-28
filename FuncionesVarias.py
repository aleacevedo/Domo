import os, shutil


CURRENTDIRECTORY = os.path.dirname(__file__)


def resetarDataBase():
    dataBaseDir = CURRENTDIRECTORY + '/DataBase'
    try:
        shutil.rmtree(dataBaseDir+'/db_repository')
        os.remove(dataBaseDir+'/app.db')
    except FileNotFoundError:
        pass
    os.system("python3 " + dataBaseDir + "/db_create.py")

