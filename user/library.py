#!/usr/bin/python3
import subprocess
import sys
import datetime

certificate= " Certificate:\nData:\n        Version: 3 (0x2)\n        Serial Number:\n            14:95:d2:2a:f7:0e:86:ac:40:1e:d3:24:7b:bf:54:0a:12:e1:7c:df\n        Signature Algorithm: ecdsa-with-SHA256\n        Issuer: C = FR, L = Limoges, O = CertifPlus, OU = SecuTic, CN = web_service\n        Validity\n            Not Before: Apr 10 09:59:44 2020 GMT\n            Not After : Apr  8 09:59:44 2030 GMT\n        Subject: C = FR, L = Limoges, O = CertifPlus, OU = SecuTic, CN = Student\n        Subject Public Key Info:\n            Public Key Algorithm: id-ecPublicKey\n                Public-Key: (256 bit)\n                pub:\n                    04:5a:66:1b:df:6c:28:64:d5:e8:1a:10:40:61:c5:\n                    0b:02:3f:82:54:33:55:7e:b1:5f:1a:25:8e:5c:82:\n                    16:fa:1e:55:3b:7d:a7:82:ac:0c:a8:99:e7:5c:1f:\n                    05:55:23:79:30:bf:e3:85:c6:21:ab:1e:dc:d5:2a:\n                    63:95:05:6b:84\n                ASN1 OID: prime256v1\n                NIST CURVE: P-256\n        X509v3 extensions:\n            X509v3 Basic Constraints: critical\n                CA:FALSE\n    Signature Algorithm: ecdsa-with-SHA256\n         30:45:02:20:0a:6a:00:8e:d2:da:43:1b:00:47:70:d5:98:4d:\n         1f:e5:02:20:cb:2d:48:e6:d4:10:7f:fc:f4:9e:6b:20:45:dc:\n         02:21:00:ce:34:fe:5e:e1:bf:16:3e:8b:e7:24:30:8e:60:fb:\n         02:48:ea:85:f5:1e:14:17:87:f5:d6:fa:b8:1e:ae:fd:6f\n-----BEGIN CERTIFICATE-----\nMIIBxjCCAWygAwIBAgIUFJXSKvcOhqxAHtMke79UChLhfN8wCgYIKoZIzj0EAwIw\nXDELMAkGA1UEBhMCRlIxEDAOBgNVBAcMB0xpbW9nZXMxEzARBgNVBAoMCkNlcnRp\nZlBsdXMxEDAOBgNVBAsMB1NlY3VUaWMxFDASBgNVBAMMC3dlYl9zZXJ2aWNlMB4X\nDTIwMDQxMDA5NTk0NFoXDTMwMDQwODA5NTk0NFowWDELMAkGA1UEBhMCRlIxEDAO\nBgNVBAcMB0xpbW9nZXMxEzARBgNVBAoMCkNlcnRpZlBsdXMxEDAOBgNVBAsMB1Nl\nY3VUaWMxEDAOBgNVBAMMB1N0dWRlbnQwWTATBgcqhkjOPQIBBggqhkjOPQMBBwNC\nAARaZhvfbChk1egaEEBhxQsCP4JUM1V+sV8aJY5cghb6HlU7faeCrAyomedcHwVV\nI3kwv+OFxiGrHtzVKmO\nVBWuEoxAwDjAMBgNVHRMBAf8EAjAAMAoGCCqGSM49BAMC\nA0gAMEUCIApqAI7S2kMbAEdw1ZhNH+UCIMstSObUEH/89J5rIEXcAiEAzjT+XuG/\nFj6L5yQwjmD7AkjqhfUeFBeH9db6uB6u/W8=\n-----END CERTIFICATE-----"


def IFAscii(msg):
    k = 0
    for i in msg:
        x = i.encode()
        if( x <= "~".encode() ):
            k = k + 1
    if( k == len(msg) ):
        return 1
    else:
        sys.exit(1)


def padding(msg):
    try:
        if(IFAscii(msg) == 1):
             while(len(msg) < 64):
                  msg = msg + "0"
    except Exception as e:
        print(e.args)
    return msg
def dateTotimestamp(date):
    dico = {"Jan": "01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    date = date[12:]
    month = date[0:3]
    Days = date[4:6]
    H_M_S = date[7:15]
    Year = date[16:20]
    if(Days[0:1] == " "):
        Days = "0" + Days[1:2]
    Month = dico.get(month)
    Date = Year + "-" + Month + "-" + Days + " " + H_M_S
    timestamp = int(datetime.datetime.strptime(Date, '%Y-%m-%d %H:%M:%S').strftime("%s"))
    return timestamp


def poster(id,at_certif):
    try:
        File = open("time_stamp","w")#contient nom_prenom||intitulé_de_la_certif
        File.write(id + at_certif)
        File.close()
    except Exception as e:
        print(e.args)
    subprocess.run("bash bash_certif -h y",shell = True)
    date = subprocess.run("openssl ts -reply -in response.tsr -text |grep Time",shell = True, stdout = subprocess.PIPE)
    date  = date.stdout.decode()
    date =  date[0:32]
    timestamp = dateTotimestamp(date)
    for i in id:
        if(i == " "):
            id = id.replace(" ","")
    post = id + at_certif + str(timestamp)
    return post

def sign(post):
    with open("post_txt","w") as post_txt:
        post_txt.write(post)
    subprocess.run("bash bash_certif -s RSA",shell=True)
    with open("sign","r") as f_sign:
        sign = f_sign.read()
    return sign
