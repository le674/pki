import qrtools
from PIL import Image
import sys

attestation = Image.open("attestation_a_verifier.png")
qrImage = attestation.crop((1418,934,1418+210,934+210))
qrImage.save("qrcoderecupere.png", "PNG")
qr = qrtools.QR()
qr.decode("qrcoderecupere.png")
data = qr.data
sys.stdout.write(data)
