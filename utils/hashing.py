import hashlib

def calculate_hash(file_path):
    # 파일의 SHA-256 해시를 계산하는 함수
    sha256_hash = hashlib.sha256()

    try:
        with open(file_path, "rb") as f:
            # 파일을 4KB씩 읽어 해시 계산
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except FileNotFoundError:
        return None