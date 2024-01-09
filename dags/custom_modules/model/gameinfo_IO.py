import json
from io import BytesIO
class FileIoSupporter():
    @staticmethod
    def make_json_file_object(gameinfo):
        json_bytes = json.dumps(gameinfo, ensure_ascii=False).encode('utf-8')
        json_file_obj = BytesIO(json_bytes)
        return json_file_obj