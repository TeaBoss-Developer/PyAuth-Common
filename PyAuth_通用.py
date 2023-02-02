from flask import *
import os
import requests
from Method import Method
import time
import hashlib
se = requests.session()
app = Flask(__name__)
debug = False
app_ver = ""
update_url = ""
app_staut = True
DKey=input("请输入被操作动态生成秘钥:")
AuthKey=input("请输入心跳校验秘钥:")#校验秘钥
@app.route("/", methods=["GET"])
def home():
    if __name__ == "__main__":
        global debug
        global DKey
        global AuthKey
        global app_ver
        global update_url
        global app_staut
        mode = request.args.get("mode",default="heartbeat")
        ver = request.args.get("ver",default="")
        url = request.args.get("update",default="")
        ctrl = request.args.get("ctrl",default="")
        key = request.args.get("key",default="")
        if(mode == "getkey"):
            if(debug):
                return(Get_Key())
            else:
                return("ERROR")
        if(mode == "checkupdate"):
            if(ver != app_ver):
                return jsonify({"code":202,"msg":"app's ver is old.please update.","url":update_url})
            if(ver == ""):
                return jsonify({"code":500,"msg":"ERROR,please check the &ver="})
            else:
                return jsonify({"code":200,"msg":"normal"})
        if(mode == "init"):
            if(app_staut == False):
                return jsonify({"code":200,"msg":"normal","AuthKey":"00000000"})
            if(app_staut == True):
                return jsonify({"code":202,"msg":"except","AuthKey":Get_Auth_Key()})
        if(mode == "update"):
            if(key == Get_Key()):
                update_url = url;
                app_ver = ver
                return jsonify({"code":200,"msg":"success"})
            if(key != Get_Key()):
                return jsonify({"code":403,"msg":"bad auth"})
            if(ver == "" or url == ""):
                return jsonify({"code":500,"msg":"ERROR,please check the &ver= and &update="})
        if(mode == "ctrl"):
            if(key == Get_Key()):
                if(ctrl == "1"):
                    app_staut = True
                if(ctrl == "0"):
                    app_staut = False
                return jsonify({"code":200,"msg":"success"})
            if(key != Get_Key()):
                return jsonify({"code":403,"msg":"bad auth"})
            if(ctrl):
                return jsonify({"code":500,"msg":"ERROR,please check the &ctrl="})
def Write_File(file_path,text):
    e = open(file_path,'a')
    e.write(text)
    e.close()

def Get_Auth_Key():
    timec = time.time()
    text = str(str(timec).split(".")[0])[0:8]+AuthKey
    MD5s = hashlib.md5(text.encode())
    return(str(MD5s.hexdigest()))
def Get_Key():
    timec = time.time()
    text = str(str(timec).split(".")[0])[0:8]+DKey
    MD5s = hashlib.md5(text.encode())
    return(str(MD5s.hexdigest()))
def Get_File(file_path):
    files = open(file_path,'r')
    m = files.read()
    files.close()
    return(m)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port="2023")
