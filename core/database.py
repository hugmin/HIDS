import pymysql
import traceback

class DatabaseManager:
    def __init__(self, db_config):
        self.config = db_config
        self.conn = None
        self.connect()

    def connect(self):
        try:
            print("[DatabaseManager] DB 연결 시도 중...")
            safe_config = self.config.copy()
            safe_config['password'] = '****'
            print(f"[DatabaseManager] 접속 정보: {safe_config}")

            print("[DatabaseManager] pymysql.connect 호출 전")

            self.conn = pymysql.connect(
                host=self.config['host'],
                port=int(self.config['port']),
                user=self.config['user'],
                password=self.config['password'],
                database=self.config['database'],
                connect_timeout=10,
                charset='utf8mb4',
                cursorclass=pymysql.cursors.DictCursor
            )

            print("[DatabaseManager] DB 연결 성공")
        except Exception:
            print("[DatabaseManager] ❌ DB 연결 실패:")
            traceback.print_exc()
            raise
        finally:
            print("[DatabaseManager] connect() 메서드 종료")

    def ensure_connection(self):
        try:
            if not self.conn or not self.conn.open:
                print("[DatabaseManager] 연결이 없거나 끊어져서 재연결 시도 중...")
                self.connect()
            else:
                print("[DatabaseManager] 기존 DB 연결 유지 중")
        except Exception:
            print("[DatabaseManager] ❌ 연결 확인 중 오류:")
            traceback.print_exc()
            self.connect()

    def insert_log(self, log_data):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    INSERT INTO logs (timestamp, level, source, message)
                    VALUES (%s, %s, %s, %s)
                """
                val = (
                    log_data["timestamp"],
                    log_data["level"],
                    log_data["source"],
                    log_data["message"]
                )
                cursor.execute(sql, val)
            self.conn.commit()
            print("[DatabaseManager] 로그 삽입 성공")
        except Exception:
            print("[DatabaseManager] ❌ 로그 삽입 실패:")
            traceback.print_exc()

    def get_hash_for_file(self, filepath):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = "SELECT hash FROM file_hashes WHERE filepath = %s"
                cursor.execute(sql, (filepath,))
                result = cursor.fetchone()
                print(f"[DatabaseManager] 해시 조회 결과: {result}")
                return result['hash'] if result else None
        except Exception:
            print("[DatabaseManager] ❌ 해시 조회 실패:")
            traceback.print_exc()
            return None

    def insert_or_update_file_hash(self, filepath, hash_value):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                sql = """
                    INSERT INTO file_hashes (filepath, hash)
                    VALUES (%s, %s)
                    ON DUPLICATE KEY UPDATE hash = VALUES(hash)
                """
                cursor.execute(sql, (filepath, hash_value))
            self.conn.commit()
            print("[DatabaseManager] 해시 삽입/업데이트 성공")
        except Exception:
            print("[DatabaseManager] ❌ 해시 삽입/업데이트 실패:")
            traceback.print_exc()
