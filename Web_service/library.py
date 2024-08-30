#!/usr/bin/python3
import subprocess
import sys
import datetime
import pyqrcode
from PIL import Image
import base64

def vers_8bit(c):
    chaine_binaire = bin(ord(c))[2:]
    return "0"*(8-len(chaine_binaire))+chaine_binaire

def modifier_pixel(pixel, bit):# on modifie que la composante rouge
    r_val = pixel[0]
    rep_binaire = bin(r_val)[2:]
    rep_bin_mod = rep_binaire[:-1] + bit
    r_val = int(rep_bin_mod, 2)
    return tuple([r_val] + list(pixel[1:]))

def recuperer_bit_pfaible(pixel):
    r_val = pixel[0]
    return bin(r_val)[-1]

def cacher(image,message):
    dimX,dimY = image.size
    im = image.load()
    message_binaire = ''.join([vers_8bit(c) for c in message])
    posx_pixel = 0
    posy_pixel = 0
    for bit in message_binaire:
        im[posx_pixel,posy_pixel] = modifier_pixel(im[posx_pixel,posy_pixel],bit)
        posx_pixel += 1
        if (posx_pixel == dimX):
            posx_pixel = 0
            posy_pixel += 1
        assert(posy_pixel < dimY)
    return 0

def recuperer(image,taille):
    message = ""
    dimX,dimY = image.size
    im = image.load()
    posx_pixel = 0
    posy_pixel = 0
    for rang_car in range(0,taille):
        rep_binaire = ""
        for rang_bit in range(0,8):
            rep_binaire += recuperer_bit_pfaible(im[posx_pixel,posy_pixel])
            posx_pixel +=1
            if (posx_pixel == dimX):
                posx_pixel = 0
                posy_pixel += 1
        message += chr(int(rep_binaire, 2))
    return message

def comparaison_chaine(msg0,msg1):
    if(len(msg0) == len(msg1)):
        for i in range(0,len(msg0)):
            if (ord(msg0[i]) != ord(msg1[i])):
                return False
            else:
                continue
    else:
        return False
    return True

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
    subprocess.run("rm sign post_txt signature.sig",shell=True)
    return sign

def Qrcode(data):
    qr = pyqrcode.create(data)
    qr.png("qrcode.png", scale=2)
    return 0

def create_image(sign):
     subprocess.run("bash bash_certif image",shell=True)
     Qrcode(sign)
     subprocess.run("bash bash_certif compo",shell=True)
     return 0

def stegano(poster):#ajoute à l'image le poster caché
    nom_fichier = "attestation.png"
    message_a_traiter = poster
    print ("Longueur message : ",len(message_a_traiter))
    with open("message_traiter","w") as f:
        f.write(str(len(message_a_traiter)))
    mon_image = Image.open(nom_fichier)
    cacher(mon_image, message_a_traiter)
    mon_image.save("stegano_"+nom_fichier)
    subprocess.run("bash bash_certif rename",shell=True)
    return 0

def recup_stegano(name_image):
    with open("message_traiter","r") as f:
        message_a_traiter = f.read()
    message_a_traiter = int(message_a_traiter)
    mon_image = Image.open(name_image)
    message_retrouve = recuperer(mon_image, message_a_traiter)
    return message_retrouve

def completion(message):#fait du padding message_0 =: nomprénom|intitulerdelacertif|padding, message_1 =: timestamp
    for i in range(0,len(message)):
        try:
            int(message[i])
            break
        except:continue
    message_0 = message[0:i]
    message_1 = message[i:]
    message_0 = padding(message_0)
    return [message_0,message_1]

def verify(time_stamp):
    date = subprocess.run("openssl ts -reply -in response.tsr -text |grep Time",shell=True,stdout = subprocess.PIPE)
    date = date.stdout.decode()
    date =  date[0:32]
    time = dateTotimestamp(date)
    b = comparaison_chaine(str(time_stamp),str(time))
    if(b == True):
        print("le timestamp n'a pas été modifiée")
    else:
        sys.exit()
    return b

def recupe_QRCODE():
    dgst = subprocess.run("bash bash_certif QR",shell = True,stdout = subprocess.PIPE)
    b64_signature = dgst.stdout.decode()
    with open("recup_b64_sign",'w') as f:
        f.write(b64_signature)
    return 0

def verifi_sign():
    subprocess.run("bash bash_certif recup_sign",shell = True)
    with open("rsult_sign.txt","r") as f:
        recupe_sign = f.read()
    b = comparaison_chaine(recupe_sign,"star platiniumSecuTIC")
    if(b == True ):
        print("la signature est bonne")
    else:
        sys.exit()
    return b
