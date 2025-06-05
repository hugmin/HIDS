import sqlite3
from datetime import datetime
from typing import Optional, List, Tuple


class Database:
    def __init__(self, db_name: str = 'events.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name, check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self) -> None:
        query = '''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            alert_type TEXT NOT NULL,
            eventid TEXT NOT NULL,
            action TEXT NOT NULL,
            username TEXT NOT NULL,
            details TEXT
        );
        '''
        self.cursor.execute(query)
        self.conn.commit()

    def insert_event(
        self,
        alert_type: str,
        eventid: str,
        action: str,
        username: str,
        details: str,
        timestamp: Optional[str] = None
    ) -> None:
        if not timestamp:
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        query = '''
        INSERT INTO events (timestamp, alert_type, eventid, action, username, details)
        VALUES (?, ?, ?, ?, ?, ?);
        '''
        self.cursor.execute(query, (timestamp, alert_type, eventid, action, username, details))
        self.conn.commit()

    def get_events(self, limit: int = 100) -> List[Tuple]:
        """가장 최근 이벤트 조회"""
        query = '''
        SELECT * FROM events ORDER BY timestamp DESC LIMIT ?;
        '''
        self.cursor.execute(query, (limit,))
        return self.cursor.fetchall()

    def close(self) -> None:
        self.conn.close()
