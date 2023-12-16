""" Data Access Objects """
import json
from typing import Dict
from pymysql.err import Error
from data_access.db_client import MysqlClient
from sqlalchemy.sql import text


class BodyMetricsDAO:
    """ A Data Access Object
    that read and write personalized itinerary data.
     """

    def __init__(self, db_client: MysqlClient):
        self.db_client = db_client

    def get_user_body_metrics_data(self, user_id: str) -> Dict:
        sql_text = text(f"SELECT * FROM body_metrics WHERE user_id = '{user_id}'")

        try:
            res, _ = self.db_client.exec_sql(sql_text)
            if res:
                formatted_data = []
                for record in res:
                    record_dict = {
                        "timestamp": record[1].isoformat(),
                        "weight": float(record[2]),
                        "height": float(record[3]),
                        "body_fat_percentage": float(record[4]),
                        "heart_rate": record[5],
                        "systolic_bp": record[6],
                        "diastolic_bp": record[7]
                    }
                    formatted_data.append(record_dict)

                # Serialize to JSON
                json_output = json.dumps(formatted_data)
                return json_output

        except Error as e:
            print(f"An error occurred during execution sql: {e}")

    def write_user_body_metrics_data(self, request_data: Dict) -> bool:
        keys = list(request_data.keys())
        values = tuple(request_data.values())
        columns = ", ".join(keys)
        placeholders = ", ".join([":{}".format(key) for key in keys])

        sql_text = text(f"INSERT INTO body_metrics ({columns}) VALUES ({placeholders})")

        try:
            self.db_client.exec_sql(sql_text, dict(zip(keys, values)))
            return True
        except Error as e:
            print(f"An error occurred during execution sql: {e}")
            return False

    def delete_user_body_metrics_data(self, user_id: str) -> bool:
        sql_text = text("delete from body_metrics where user_id = :user_id")

        try:
            self.db_client.exec_sql(sql_text, {'user_id': user_id})
            return True
        except Error as e:
            print(f"An error occurred during execution sql: {e}")
            return False
