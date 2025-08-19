import urllib.parse
import requests
import urllib
import os
import shutil
import time
import subprocess
url = "http://file-exchange/file-gateway-webapi/sharings/"
token = "user-token=4c45dbe0f9c64ef6b4c4621c242141ed"
headers = {
    "Cookie": "user-token=4c45dbe0f9c64ef6b4c4621c242141ed",  # 直接设置 Cookie
}

def join(base:str, params:list):
    res = base
    for param in params:
        res = urllib.parse.urljoin(res, str(param))
        if not res.endswith("/"):
            res += "/"
    if res.endswith("/"):
        res = res[:-1]
    return res

def get_sharing():
    response = requests.get(
        url,    
        headers=headers,    
        verify=False
    )
    info = response.json()['info']
    rows = info['rows']
    res_url = url
    filename = ""
    print(f"code state: {response.status_code}")
    if len(rows) > 0:
        request = rows[0]
        key = str(request['key'])
        files = request['files'][0]
        filename = files['fileName']
        fileId = files['fileId']
        params = (key, "files", fileId)
        res_url = join(url, params=params)
        print(request)
    return res_url, filename

def get_Apk(url, name):
    # curl -b "user-token=4c45dbe0f9c64ef6b4c4621c242141ed"  --insecure   -o "app.apk"  "http://file-exchange/file-gateway-webapi/sharings/851543/files/1971848"
    print(url)
    res = requests.get (
        url=url,
        headers=headers,
        verify=False,
        stream=True
    )
    if res.status_code == 200:
        with open(name, 'wb') as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"download {name} succeed!!!!")
        return name
    else:
        print(f'get failed. code: {res.status_code}')
        return ""
def move_apk(name:str):
    if name == "":
        print('none apk...')
        return
    base = "D:\\DailyWork\\"
    path = os.path.join(base, time.strftime('%m\\%d'))
    print(path)
    if os.path.exists(path):
        dst = os.path.join(path, name)
        shutil.move(name, dst)
        print(f"move {name} to {dst}")
        return dst
    else:
        print(f"path not exists: {path}")
        return ""
    # print(f'{time.strftime("%m\\%d")}')

def excute(name, path):
    if name == "":
        return
    elif not os.path.exists(path):
        print("not found apk")
        return
    path = "D:\\BasicSetting\\CustomBat"
    batName = ""
    if name == "VehicleLogicService.apk":
        batName = os.path.join(path, "pushService.bat")
    elif name == "VehicleSetting.apk":
        batName = os.path.join(path, "pushSetting.bat")
    if batName == "":
        print("wrong apk name")
    process = subprocess.Popen(
        [batName, name],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        shell=True,
        encoding="gbk"
    )
    # 等待执行完成并获取输出
    stdout, stderr = process.communicate()

    print(stdout)

if __name__ == "__main__":
    base,name = get_sharing()
    name = get_Apk(base, name=name)
    dst = move_apk(name)
    excute(name, dst)