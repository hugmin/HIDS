import json

def load_detection_rules(config_path):
    # 설정 파일에서 탐지 룰을 로드하는 함수
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            return config.get('detection_rules', [])
    except FileNotFoundError:
        print("Rule file not found!")
        return []

def match_pattern(log_message, patterns):
    # 로그 메시지가 패턴에 맞는지 확인하는 함수
    for pattern in patterns:
        if pattern in log_message:
            return True
    return False