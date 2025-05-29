import psutil
import time

class SystemMonitor:
    def __init__(self):
        try:
            self.last_update = 0
            self.cache_duration = 2
            self.cached_data = {}
        except Exception as e:
            print(f"[SystemMonitor] 초기화 실패: {e}")
            import traceback
            traceback.print_exc()
            raise

    def get_stats(self):
        try:
            now = time.time()
            if now - self.last_update > self.cache_duration:
                cpu = psutil.cpu_percent(interval=0.2)
                mem = psutil.virtual_memory().percent
                disk = psutil.disk_usage('/').percent
                self.cached_data = {
                    "cpu": cpu,
                    "memory": mem,
                    "disk": disk
                }
                self.last_update = now
            return self.cached_data
        except Exception as e:
            print(f"[SystemMonitor] ❌ 시스템 정보 조회 실패: {e}")
            import traceback
            traceback.print_exc()
            return {
                "cpu": 0.0,
                "memory": 0.0,
                "disk": 0.0
            }
