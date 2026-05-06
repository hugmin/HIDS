# HIDS (Host-based Intrusion Detection System)

## 📘 개요
윈도우 시스템 내부의 이상 행위를 정밀 탐지하는 보안 솔루션입니다.\
OSquery와 WMI 등 시스템 전용 라이브러리를 활용하여 침입 징후를 포착하고, 사용자에게 시각화된 보안 정보를 제공합니다.

## 🧩 주요 기능
- psutil, wmi를 활용한 프로세스 및 시스템 자원 상시 모니터링
- OSquery 기반 쿼리로 시스템 구성 변경 및 보안 취약점 탐지
- pywin32 기반 이벤트 로그 분석 및 watchdog을 이용한 파일 무결성 검사
- PyQt5와 matplotlib을 이용한 실시간 보안 지표 시각화
- 이상 발생 시 smtplib을 통한 관리자 이메일 경고 즉시 발송
- pandas로 정제된 대량의 탐지 로그를 SQLite에 체계적으로 기록

## 📦 기술 스택
- **Frontend**: PyQt5, matplotlib
- **Backend**: OSquery, psutil, wmi, pywin32, watchdog, pandas, smtplib
- **DB**: SQLite

## 📝 Developer Notes (참고용)
