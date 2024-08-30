#!/usr/bin/python3
from bottle import route, run, template, request, response
import subprocess
import library as lib
import sys

@route('/creation', method='POST')
def creation_attestation():
    contenu_identité = request.forms.get('identite')
    contenu_intitulé_certification = request.forms.get('intitule_certif')
    print('nom prénom :', contenu_identité, ' intitulé de la certification :',contenu_intitulé_certification)
    response.set_header('Content-type', 'text/plain')
    poster = lib.poster(contenu_identité,contenu_intitulé_certification)#id|intitulé_certif|timestamp(à dissimuler par stegano)
    info = contenu_identité + contenu_intitulé_certification
    print(info)
    sign = lib.sign(info)
    lib.create_image(sign)
    lib.stegano(poster)
    return "ok!"

@route('/verification', method='POST')
def verification_attestation():
    contenu_image = request.files.get('image')
    contenu_image.save('attestation_a_verifier.png',overwrite=True)
    response.set_header('Content-type', 'text/plain')
    poster = lib.recup_stegano("attestation_a_verifier.png")
    info_timestamp = lib.completion(poster)
    lib.verify(info_timestamp[1])
    bool0 = lib.recupe_QRCODE()
    bool1 = lib.verifi_sign() #le résultat du déchiffrement de la signature est dans rsult_sign.txt
    print(bool0)
    print(bool1)
    if(bool0 == 0):
        if(bool1 == True):
            return "ok!"
        else:
            return "not a good attestation"
    else:
        return "not a good attestation"

@route('/fond')
def recuperer_fond():
    response.set_header('Content-type', 'image/png')
    descripteur_fichier = open('fond_attestation.png','rb')
    contenu_fichier = descripteur_fichier.read()
    descripteur_fichier.close()
    return contenu_fichier
run(host='0.0.0.0',port=8080,debug=True)
