import mysql.connector

class Database:
    def __init__(self, config):
        self.config = config
        self.db_connection = mysql.connector.connect(
            host=self.config['db']['host'],
            user=self.config['db']['user'],
            password=self.config['db']['password'],
            database=self.config['db']['database']
        )
        self.cursor = self.db_connection.cursor()

    def save_log(self, log_message):
        # 로그 메시지를 데이터베이스에 저장
        query = "INSERT INTO logs (message) VALUES (%s)"
        self.cursor.execute(query, (log_message,))
        self.db_connection.commit()

    def close(self):
        # 데이터베이스 연결 종료
        self.cursor.close()
        self.db_connection.close()