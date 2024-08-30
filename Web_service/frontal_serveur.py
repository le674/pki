import subprocess
import library as lib
certif = int(input(" 0. construire un nouveau certificat 1. ne pas construire un nouveau certificat -----> "))
if(certif == 0):
    subprocess.run("bash bash_certif -c ECC",shell=True)
subprocess.run("bash bash_certif -link",shell=True)
