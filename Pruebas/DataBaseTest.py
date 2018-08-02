import unittest, requests, sys
sys.path.append("../FuncionesVarias")
from FuncionesVarias import resetarDataBase

AUTH = ("admin", "admin")
BASEURL = "http://localhost:5555/Data/api/v1.0"


class DataBaseTest(unittest.TestCase):

    def setUp(self):
        resetarDataBase()

    def test_emptyUserDataBase(self):
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
        r2 = requests.get(url+"/"+nwuser[0], auth=AUTH)
        self.assertEqual(r.json()[str(r2.json()['id'])]['nickName'],nwuser[0], "El usuario 1 no fue agregado")

    def test_delUserDataBase(self):
        """Borro usuario, debe responder con status code 200"""
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
        """Modifico un usuario, debe responder con status code 200"""
        url = BASEURL + "/User"
        urlusers = BASEURL + "/Users"
        nwuser = ("Alejo", "19051996")
        payload1 = {'email': "ale.acevedo@live.com.ar", 'nickName': "Alejo", 'password': "19051996"}
        modpayload = {'email': "fede@live.com.ar", 'nickName': "Fede", 'password': "20091995"}
        r = requests.post(url, json=payload1, auth=AUTH)
        r = requests.put(url, json={'email': modpayload['email']}, auth=nwuser)
        self.assertEqual(r.status_code, 200, "No se pudo modificar el usuario")
        r = requests.get(urlusers, auth=AUTH)
        self.assertEqual(r.json()["2"]['email'], modpayload['email'], "El email usuario no fue modificado")
        r = requests.put(url, json={'nickName': modpayload['nickName']}, auth=nwuser)
        self.assertEqual(r.status_code, 200, "No se pudo modificar el usuario")
        r = requests.get(urlusers, auth=AUTH)
        self.assertEqual(modpayload['nickName'], r.json()["2"]['nickName'], "El nickName usuario no fue modificado")
        r = requests.put(url, json={'password': modpayload['password']}, auth=(modpayload['nickName'], nwuser[1]))
        self.assertEqual(r.status_code, 200, "No se pudo modificar el usuario")
        r = requests.get(urlusers, auth=(modpayload['nickName'], modpayload['password']))
        self.assertEqual(r.status_code, 200, "La password usuario no fue modificado")

    def test_unauthUserDataBase(self):
        """Trato de modificar la base de datos desde un usuario no autorizado, debe fallar"""
        url = BASEURL + "/User"
        nwuser = ("Alejo", "19051996")
        payload1 = {'email': "ale.acevedo@live.com.ar", 'nickName': "Alejo", 'password': "19051996"}
        payload2 = {'email': "fede@live.com.ar", 'nickName': "Federico", 'password': "20091995"}
        r = requests.get(url, auth=nwuser)
        self.assertEqual(r.status_code, 405, "Usuario no registrado recibio informacion")
        r = requests.post(url, json=payload1, auth=nwuser)
        self.assertEqual(r.status_code, 401, "Usuario no registrado agrego usuario")
        r = requests.put(url, json=payload1, auth=nwuser)
        self.assertEqual(r.status_code, 401, "Usuario no registrado modifico a otro")
        r = requests.delete(url, auth=nwuser)
        self.assertEqual(r.status_code, 401, "Usuario no registrado borro a otro")
        requests.post(url, json=payload1, auth=AUTH)
        r = requests.post(url,json=payload2, auth=nwuser)
        self.assertEqual(r.status_code, 401, "Usuario no admin trato de agregar otro")

    def test_mixUserDataBase(self):
        """Trato de mezclar los mails de los usuarios, debe devolver status code 500"""
        url = BASEURL + "/User"
        payload1 = {'email': "ale.acevedo@live.com.ar", 'nickName': "Alejo", 'password': "19051996"}
        payload2 = {'email': "fede@live.com.ar", 'nickName': "Federico", 'password': "20091995"}
        requests.post(url, json=payload1, auth=AUTH)
        requests.post(url, json=payload2, auth=AUTH)
        r = requests.post(url, json=payload1, auth=AUTH)
        self.assertEqual(r.status_code, 500, "Se solaparon los usuarios al agregarse")
        r = requests.put(url, json=payload1, auth=(payload2['nickName'], payload2['password']))
        self.assertEqual(r.status_code, 500, "Se solaparon usuarios al modificarse")

    def test_emptyModDataBase(self):
        """Constato base de datos vacia"""
        url = BASEURL + "/Mods"
        r = requests.get(url, auth=AUTH)
        self.assertEqual(len(r.json()), 0, "Hay algun modulo")

    def test_addModDataBase(self):
        """Agrego 100 modulos, debe devolver status code 200 y debe tener atributo new igual a True"""
        url = BASEURL + "/Mod"
        urlMods = BASEURL + "/Mods"
        payload = {'uniqueID':0}
        for x in range(100):
            payload['uniqueID'] = x
            r = requests.post(url, json=payload, auth=AUTH)
            self.assertEqual(r.status_code, 200, "El modulo " + str(x) + " fallo")
        r = requests.get(urlMods, auth=AUTH)
        r = r.json()
        for keys in r:
            self.assertTrue(r[keys]['new'], 'El atributo new del mod ' + keys + " no es True")

    def test_delModDataBase(self):
        """Agrego un modulo y lo borro"""
        url = BASEURL + "/Mod"
        urlMods = BASEURL + "/Mods"
        payload = {'uniqueID': 0}
        r = requests.get(urlMods, auth=AUTH)
        self.assertEqual(len(r.json()), 0, "Hay algun modulo")
        r = requests.post(url, json=payload, auth=AUTH)
        self.assertEqual(r.status_code, 200, "El modulo no fue agregado ")
        r = requests.delete(url, json={"idMod": 1}, auth=AUTH)
        self.assertEqual(r.status_code, 200, "El modulo no fue borrado")
        r = requests.get(urlMods, auth=AUTH)
        self.assertEqual(len(r.json()), 0, "Hay algun modulo")

    def test_errorModDataBase(self):
        """Pruebo los codigo de error"""
        url = BASEURL + "/Mod"
        urlMods = BASEURL + "/Mods"
        payload = {'uniqueID': 0}
        r = requests.get(urlMods)
        self.assertEqual(r.status_code, 401, "Devolvio los modulos sin auth")
        r = requests.post(url, json=payload)
        self.assertEqual(r.status_code, 401, "Agrego un modulo sin auth")
        r = requests.delete(url, json={"idMod": 1})
        self.assertEqual(r.status_code, 401, "Borro un modulo sin auth")
        r = requests.delete(url, json={"idMod": 1}, auth=AUTH)
        self.assertEqual(r.status_code, 500, "Borro un modulo inexistente")

    def test_addModToUserDataBase(self):
        """Agrego modulos a los usuarios"""
        urlUser = BASEURL + "/User"
        urlMod = BASEURL + "/Mod"
        idUser = "2"
        url = BASEURL + "/User/"+str(idUser)+"/mod"
        user = {"nickName": "Alejo", "email":"ale.acevedo", "password":"19051996"}
        mod1 = {"uniqueID": 0}
        authUser = ("Alejo", "19051996")
        requests.post(urlUser, json=user, auth=AUTH)
        requests.post(urlMod, json=mod1, auth=AUTH)
        r = requests.post(url, json={"idMod": 1}, auth=authUser)
        self.assertEqual(r.status_code, 200, "El modulo no se agrego al usuario")
        r = requests.get(urlUser+"s", auth=authUser)
        r = r.json()
        self.assertEqual(len(r[idUser]["mods"]), 1, "El modulo no no fue agregado")

    def test_delModToUserDataBase(self):
        """Agrego los modulos a los usurios y luego los borro para asegurarme que desaparezcan"""
        urlUser = BASEURL + "/User"
        urlMod = BASEURL + "/Mod"
        idUser = "2"
        url = BASEURL + "/User/mod"
        url1 = BASEURL + "/User/"+str(idUser)+"/mod"
        user = {"nickName": "Alejo", "email":"ale.acevedo", "password":"19051996"}
        mod1 = {"uniqueID": 0}
        mod2 = {"uniqueID": 1}
        authUser = ("Alejo", "19051996")
        requests.post(urlUser, json=user, auth=AUTH)
        requests.post(urlMod, json=mod1, auth=AUTH)
        requests.post(urlMod, json=mod2, auth=AUTH)
        r = requests.post(url1, json={"idMod": 1}, auth=authUser)
        r = requests.post(url1, json={"idMod": 2}, auth=authUser)
        self.assertEqual(r.status_code, 200, "El modulo no se agrego al usuario")
        r = requests.get(urlUser+"s", auth=authUser)
        r = r.json()
        self.assertEqual(len(r[idUser]["mods"]), 2, "El modulo no fue agregado")
        r = requests.delete(url, json={"idMod": 1}, auth=authUser)
        self.assertEqual(r.status_code, 200, "El modulo no se elimino del usuario")
        r = requests.get(urlUser+"s", auth=authUser)
        r = r.json()
        self.assertEqual(len(r[idUser]["mods"]), 1, "El modulo no fue eliminado")
        requests.delete(urlMod, json={"idMod": 2}, auth=AUTH)
        r = requests.get(urlUser+"s", auth=authUser)
        r = r.json()
        self.assertEqual(len(r[idUser]["mods"]), 0, "El modulo no fue eliminado")

    def test_addTaskDataBase(self):
        urlUser = BASEURL + "/User"
        urlMod = BASEURL + "/Mod"
        urlTask = BASEURL + "/Mod/1/task"
        user = {"nickName": "Alejo", "email":"ale.acevedo", "password":"19051996"}
        mod1 = {"uniqueID": 0}
        authUser = ("Alejo", "19051996")
        url1 = BASEURL + "/User/2/mod"
        task = {"hour": 12, "minute":12, "newState": 12, "wDay": 5}
        requests.post(urlUser, json=user, auth=AUTH)
        requests.post(urlMod, json=mod1, auth=AUTH)
        requests.post(url1, json={"idMod": 1}, auth=authUser)
        r = requests.get(urlTask, auth=authUser)
        self.assertEqual(len(r.json()), 0, "Los task no estan vacios")
        r = requests.post(urlTask, json=task, auth=authUser)
        self.assertEqual(r.status_code, 200, "El task no se agrego")
        r = requests.get(urlTask, auth=authUser)
        self.assertEqual(len(r.json()), 1, "El task no fue agregado")

    def test_chModDataBase(self):
        urlUser = BASEURL + "/User"
        urlMod = BASEURL + "/Mod"
        urlTask = BASEURL + "/Mod/1/task"
        user = {"nickName": "Alejo", "email":"ale.acevedo", "password":"19051996"}
        mod1 = {"uniqueID": 1, "newState": "255"}
        authUser = ("Alejo", "19051996")
        url1 = BASEURL + "/User/2/mod"
        task = {"hour": 12, "minute":12, "newState": 12, "wDay": 5}
        requests.post(urlUser, json=user, auth=AUTH)
        requests.post(urlMod, json=mod1, auth=AUTH)
        requests.post(url1, json={"idMod": 1}, auth=authUser)
        r = requests.get(urlTask, auth=authUser)
        self.assertEqual(len(r.json()), 0, "Los task no estan vacios")
        r = requests.post(urlTask, json=task, auth=authUser)
        self.assertEqual(r.status_code, 200, "El task no se agrego")
        r = requests.get(urlTask, auth=authUser)
        self.assertEqual(len(r.json()), 1, "El task no fue agregado")
        r = requests.put(urlMod, json=mod1, auth=authUser)

    def test_uModDataBase(self):
        urlUser = BASEURL + "/User"
        urlMod = BASEURL + "/Mod"
        urlUMod = BASEURL + "/UMod"
        user = {"nickName": "Alejo", "email":"ale.acevedo", "password":"19051996"}
        mod1 = {"uniqueID": 1, "newState": "250"}
        authUser = ("Alejo", "19051996")
        url1 = BASEURL + "/User/2/mod"
        requests.post(urlUser, json=user, auth=AUTH)
        requests.post(urlMod, json=mod1, auth=AUTH)
        requests.post(url1, json={"idMod": 1}, auth=authUser)
        r = requests.put(urlUMod+"/1/"+mod1["newState"])
        r = requests.get(urlMod+"/1", auth=authUser)
        r = r.json()
        self.assertEqual(str(r["1"]['state']), mod1['newState'])










if __name__ == '__main__':
    unittest.main()