from datetime import datetime

def current_time(format="%Y-%m-%d %H:%M:%S"):
    # 현재 시간을 지정된 포맷으로 반환하는 함수
    return datetime.now().strftime(format)

def convert_to_timestamp(date_string, format="%Y-%m-%d %H:%M:%S"):
    # 날짜 문자열을 타임스탬프로 변환하는 함수
    return datetime.strptime(date_string, format).timestamp()