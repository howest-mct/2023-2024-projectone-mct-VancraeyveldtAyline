from .Database import Database
from datetime import datetime

class DataRepository:
    @staticmethod
    def json_or_formdata(request):
        if request.method != 'GET' and request.content_type == 'application/json':
            gegevens = request.get_json()
        else:
            gegevens = request.form.to_dict()
        return gegevens
    


# ****************** USERS ******************
    @staticmethod
    def read_user(userid: int):
        sql = "SELECT * FROM Gebruikers WHERE gebruiker_id = %s"
        params = [userid]
        return Database.get_one_row(sql, params)
    
    @staticmethod
    def read_users():
        sql = "SELECT * FROM Gebruikers"
        return Database.get_one_row(sql)

    @staticmethod
    def create_user(username, email, password):
        sql = "INSERT INTO Gebruikers (gebruiker_naam, gebruiker_email, gebruiker_wachtwoord) VALUES (%s)"
        params = [username, email, password]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def update_user(userid: int, username, email, password):
        sql = "UPDATE Gebruikers SET gebruiker_naam = %s, gebruiker_email = %s, gebruiker_wachtwoord = %s WHERE treinen.idtrein = %s"
        params = [username, email, password, userid]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def delete_user(userid: int):
        sql = "DELETE FROM Gebruikers WHERE userid = %s"
        params = [userid]
        return Database.execute_sql(sql, params)
    

 # ****************** HISTORIEK ******************   
    @staticmethod
    def insert_values_historiek(deviceid: int, waarde: float, opmerking:str = None):
        sql = "INSERT INTO Historiek (waarde, tijdstip_waarde, opmerking, device_id) VALUES (%s, %s, %s, %s);"
        huidige_tijd = datetime.now()
        mysql_datetime_formaat = huidige_tijd.strftime('%Y-%m-%d %H:%M:%S')
        params = [waarde, mysql_datetime_formaat, opmerking, deviceid]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_records_historiek_by_id(id: int):
        sql = "SELECT * from Historiek WHERE id = %s"
        params = [id]
        return Database.get_rows(sql, params)
    
    @staticmethod
    def read_records_historiek():
        sql = "SELECT * FROM Historiek as h inner join Devices as d on h.device_id = d.device_id"
        return Database.get_rows(sql)
    
    @staticmethod
    def read_records_historiek_by_date(date: str):
        sql = "SELECT * FROM Historiek WHERE DATE(tijdstip_waarde) = %s;"
        params = [date]
        return Database.get_rows(sql, params)


# ****************** TYPES ******************
    @staticmethod
    def read_types():
        sql = "SELECT * FROM Product_Types"
        return Database.get_rows(sql)

    @staticmethod
    def create_type(producttype: str):
        sql = "INSERT INTO Product_Types (product_type) VALUES (%s)"
        params = [producttype]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def delete_type(typeid: int):
        sql = "DELETE FROM Product_Types WHERE type_id = %s"
        params = [typeid]
        return Database.execute_sql(sql, params)
       
    @staticmethod
    def update_type(typeid: int, producttype: str):
        sql = "UPDATE Product_Types SET product_type = %s WHERE type_id = %s"
        params = [producttype, typeid]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def read_type(typeid: int):
        sql = "SELECT * FROM Product_Types WHERE type_id = %s"
        params = [typeid]
        return Database.get_one_row(sql, params)

# ****************** PRODUCTS ******************
    @staticmethod
    def read_products():
        sql = "SELECT * FROM Producten"
        return Database.get_rows(sql)

    @staticmethod
    def create_product(barcode, productnaam: str, producttypeid: int):
        sql = "INSERT INTO Producten (barcode, product_naam, product_type) VALUES (%s, %s, %s)"
        params = [barcode, productnaam, producttypeid]
        return Database.execute_sql(sql, params)
    
    @staticmethod
    def delete_product(productid: int):
        sql = "DELETE FROM Producten WHERE product_id = %s"
        params = [productid]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_product(productid: int, barcode, productnaam: str, producttypeid: int):
        sql = "UPDATE Producten SET barcode = %s, productnaam = %s, producttypeid = %s WHERE productid = %s"
        params = [barcode, productnaam, producttypeid, productid]
        return Database.execute_sql(sql, params)
    

# ****************** PRODUCTEN HISTORIEK ******************
    @staticmethod
    def insert_values_product_historiek(wijziging: int, product_id: int):
        sql = "INSERT INTO Producten_Historiek (product_aantal_wijziging, tijdstip, product_id) VALUES (%s, %s, %s);"
        huidige_tijd = datetime.now()
        mysql_datetime_formaat = huidige_tijd.strftime('%Y-%m-%d %H:%M:%S')
        params = [wijziging, mysql_datetime_formaat, product_id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def read_records_product_historiek_by_productid(productid: int):
        sql = "SELECT * from Producten_Historiek WHERE product_id = %s"
        params = [productid]
        return Database.get_rows(sql, params)
    
    @staticmethod
    def read_records_product_historiek():
        sql = "SELECT * from Producten_Historiek"
        return Database.get_rows(sql)
    
    @staticmethod
    def read_records_product_historiek_by_date(date: str):
        sql = "SELECT * FROM Producten_Historiek WHERE DATE(tijdstip) = %s;"
        params = [date]
        return Database.get_rows(sql, params)
    

# ****************** GEBRUIKER VOORKEUREN ******************
    @staticmethod
    def update_voorkeur(voorkeur_id: int, gebruiker_id: int, voorkeur_beschrijving: str, voorkeur_waarde: int, voorkeur_state: bool):
        sql = "UPDATE Gebruiker_Voorkeuren SET gebruiker_id = %s, voorkeur_beschrijving = %s, voorkeur_waarde = %s, voorkeur_state = %s = %s WHERE voorkeur_id = %s"
        params = [gebruiker_id, voorkeur_beschrijving, voorkeur_waarde, voorkeur_state, voorkeur_id]
        return Database.execute_sql(sql, params)


# ****************** GEBRUIKER MIN PRODUCT ******************
    @staticmethod
    def update_min_product(min_product_id, product_id, gebruiker_id, minimum_waarde):
        sql = "UPDATE Gebruiker_Min_Product SET product_id = %s, gebruiker_id = %s, minimum_waarde = %s WHERE min_product_id = %s"
        params = [product_id, gebruiker_id, minimum_waarde, min_product_id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def create_min_product(product_id, gebruiker_id, minimum_waarde):
        sql = "INSERT INTO Gebruiker_Min_Product (product_id, gebruiker_id, minimum_waarde) VALUES (%s, %s, %s);"
        params = [product_id, gebruiker_id, minimum_waarde]
        return Database.execute_sql(sql, params)



