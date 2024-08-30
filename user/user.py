#!/usr/bin/python3
from bottle import route, run, template, request, response
import subprocess
who = int(input("student 1) or employer 2) -----> "))
if(who == 1):
    for i in range(0,2):
        data = int(input(" envoies des données 1) reçue de l' image 2) -----> "))
        if(data == 1):
            subprocess.run("curl -X POST -d 'identite=star platinium' -d 'intitule_certif=SecuTIC' \http://localhost:8080/creation",shell = True)
        if(data == 2):
            print("la commande se lance ou pas ?")
            subprocess.run("curl -v -o mon_image.png http://localhost:8080/fond",shell = True)
else:
    for i in range(0,2):
        attest = int(input("vérification de l' image 1) quitter le serveur web 2) -----> "))
        if(attest == 1):
            subprocess.run("mv mon_image.png fond_attestation.png",shell=True)
            try:
                subprocess.run("curl -v -F image=@fond_attestation.png http://localhost:8080/verification",shell=True)
            except:pass
