import unittest, requests, sys
sys.path.append("../FuncionesVarias")
from FuncionesVarias import resetarDataBase

AUTH = ("admin", "admin")
BASEURL = "http://localhost:5555/Data/api/v1.0"


class DataBaseTest(unittest.TestCase):

    def setUp(self):
        resetarDataBase()

    def test_emptyDataBase(self):
        """ La base de datos se crea siempre con el usuario admin"""
        url = BASEURL + "/Users"
        r = requests.get(url, auth=AUTH)
        self.assertEqual(len(r.json()), 1, "La base de datos no esta vacia")

    def test_addUserDataBase(self):
        """ Agrego usuario, debe responder con status code 200"""
        url = BASEURL + "/User"
        nwuser = ("Alejo", "19051996")
        payload1 = {'email':"ale.acevedo@live.com.ar", 'nickName':"Alejo", 'password':"19051996"}
        payload2 = {'email': "fede.cava@live.com.ar", 'nickName': "Federico", 'password': "20091995"}
        r = requests.post(url, json=payload1, auth=AUTH)
        self.assertEquals(r.status_code, 200, "El usuario 1 no pudo ser agregado")
        r = r = requests.post(url, json=payload2, auth=nwuser)
        self.assertEquals(r.status_code, 200, "El usuario 2 no pudo ser agregado, revise el usuario 1p")


if __name__ == '__main__':
    unittest.main()