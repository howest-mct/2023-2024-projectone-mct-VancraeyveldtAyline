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

    @staticmethod
    def read_status_lampen():
        sql = "SELECT * from lampen"
        return Database.get_rows(sql)

    @staticmethod
    def read_status_lamp_by_id(id):
        sql = "SELECT * from lampen WHERE id = %s"
        params = [id]
        return Database.get_one_row(sql, params)

    @staticmethod
    def update_status_lamp(id, status):
        sql = "UPDATE lampen SET status = %s WHERE id = %s"
        params = [status, id]
        return Database.execute_sql(sql, params)

    @staticmethod
    def update_status_alle_lampen(status):
        sql = "UPDATE lampen SET status = %s"
        params = [status]
        return Database.execute_sql(sql, params)
    
    
    @staticmethod
    def insert_values_historiek(deviceid: int, waarde: float, opmerking:str = None):
        sql = "INSERT INTO lampen SET status = %s"
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
        sql = "SELECT * from Historiek"
        return Database.get_rows(sql)