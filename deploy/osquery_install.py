import os
import subprocess
import getpass
import urllib.request

# 경로 설정
OSQUERY_INSTALL_PATH = "C:\\Program Files\\osquery"
OSQUERY_EXE = os.path.join(OSQUERY_INSTALL_PATH, "osqueryd", "osqueryd.exe")
OSQUERY_CONF_TEMPLATE = os.path.join(os.path.dirname(__file__), "osquery_template.conf")
OSQUERY_CONF_PATH = "C:\\ProgramData\\osquery\\osquery.conf"
LOG_DIR = "C:\\ProgramData\\osquery\\log"

# 최신 깃허브 릴리즈 MSI URL
OSQUERY_MSI_URL = "https://github.com/osquery/osquery/releases/download/5.17.0/osquery-5.17.0.msi"

def is_osquery_installed() -> bool:
    """osqueryd.exe 존재 여부 확인"""
    return os.path.isfile(OSQUERY_EXE)

def download_and_install_osquery():
    """osquery msi 다운로드 및 설치"""
    msi_path = os.path.join(os.getenv("TEMP"), "osquery-setup.msi")

    if not os.path.isfile(msi_path):
        print("Downloading osquery installer...")
        try:
            req = urllib.request.Request(
                OSQUERY_MSI_URL,
                headers={'User-Agent': 'Mozilla/5.0'}
            )
            with urllib.request.urlopen(req) as response, open(msi_path, 'wb') as out_file:
                out_file.write(response.read())
            print(f"Downloaded to {msi_path}")
        except Exception as e:
            print(f"Failed to download osquery MSI: {e}")
            raise

    print("Installing osquery...")
    try:
        subprocess.run(["msiexec", "/i", msi_path, "/quiet", "/norestart"], check=True)
        print("osquery installed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"osquery installation failed: {e}")
        raise

def generate_osquery_config():
    """템플릿 기반 osquery.conf 생성 및 username 치환"""
    if not os.path.isfile(OSQUERY_CONF_TEMPLATE):
        raise FileNotFoundError(f"Config template not found: {OSQUERY_CONF_TEMPLATE}")

    with open(OSQUERY_CONF_TEMPLATE, "r", encoding="utf-8") as f:
        conf_text = f.read()

    username = getpass.getuser()
    conf_text = conf_text.replace("{{username}}", username)

    os.makedirs(os.path.dirname(OSQUERY_CONF_PATH), exist_ok=True)

    with open(OSQUERY_CONF_PATH, "w", encoding="utf-8") as f:
        f.write(conf_text)

    print(f"osquery config generated at {OSQUERY_CONF_PATH}")

def ensure_log_dir():
    """로그 폴더 생성 및 권한 부여"""
    if not os.path.isdir(LOG_DIR):
        os.makedirs(LOG_DIR)
        print(f"Log directory created at {LOG_DIR}")
    else:
        print(f"Log directory exists: {LOG_DIR}")

    # Everyone에게 로그 폴더에 대한 전체 권한 부여 (관리자 권한 필요)
    cmd = f'icacls "{LOG_DIR}" /grant Everyone:(OI)(CI)F /T /C'
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        print(f"Permissions set successfully on {LOG_DIR}")
    else:
        print(f"Failed to set permissions on {LOG_DIR}: {result.stderr}")

def install_osquery():
    """osquery 설치 및 설정파일, 로그 폴더 준비"""
    if is_osquery_installed():
        print("osquery is already installed.")
    else:
        download_and_install_osquery()

    generate_osquery_config()
    ensure_log_dir()

if __name__ == "__main__":
    install_osquery()
