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
        urlusers = BASEURL + "/Users"
        nwuser = ("Alejo", "19051996")
        payload1 = {'email':"ale.acevedo@live.com.ar", 'nickName':"Alejo", 'password':"19051996"}
        r = requests.post(url, json=payload1, auth=AUTH)
        self.assertEquals(r.status_code, 200, "El usuario 1 no pudo ser agregado")
        r = requests.get(urlusers, auth=AUTH)
        self.assertEqual(len(r.json()), 2, "El usuario 1 no fue agregado")
        self.assertEqual(r.json()[nwuser[0]]['nickName'],nwuser[0], "El usuario 1 no fue agregado")

    def test_delUserDataBase(self):
        url = BASEURL + "/User"
        urlusers = BASEURL + "/Users"
        nwuser = ("Alejo", "19051996")
        payload1 = {'email': "ale.acevedo@live.com.ar", 'nickName': "Alejo", 'password': "19051996"}
        r = requests.post(url, json=payload1, auth=AUTH)
        r = requests.delete(url, auth=nwuser)
        self.assertEqual(r.status_code, 200, "El usuario no pudo ser borrado")
        r = requests.get(urlusers, auth=AUTH)
        self.assertEqual(len(r.json()), 1, "El usuario no fue borrado")

    def test_modUserDataBase(self):
        url = url = BASEURL + "/User"
        urlusers = BASEURL + "/Users"
        nwuser = ("Alejo", "19051996")
        payload1 = {'email': "ale.acevedo@live.com.ar", 'nickName': "Alejo", 'password': "19051996"}
        modpayload = {'email': "fede@live.com.ar", 'nickName': "Fede", 'password': "20091995"}
        r = requests.post(url, json=payload1, auth=AUTH)
        r = requests.put(url, json={'email': modpayload['email']}, auth=nwuser)
        self.assertEqual(r.status_code, 200, "No se pudo modificar el usuario")
        r = requests.get(urlusers, auth=AUTH)
        self.assertEqual(r.json()[nwuser[0]]['email'], modpayload['email'], "El email usuario no fue modificado")
        r = requests.put(url, json={'nickName': modpayload['nickName']}, auth=nwuser)
        self.assertEqual(r.status_code, 200, "No se pudo modificar el usuario")
        r = requests.get(urlusers, auth=AUTH)
        self.assertEqual(modpayload['nickName'] in r.json(), True, "El nickName usuario no fue modificado")
        r = requests.put(url, json={'password': modpayload['password']}, auth=(modpayload['nickName'], nwuser[1]))
        self.assertEqual(r.status_code, 200, "No se pudo modificar el usuario")
        r = requests.get(urlusers, auth=(modpayload['nickName'], modpayload['password']))
        self.assertEqual(r.status_code, 200, "La password usuario no fue modificado")


if __name__ == '__main__':
    unittest.main()