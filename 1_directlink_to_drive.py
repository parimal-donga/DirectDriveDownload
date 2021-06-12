
import os
from google.colab import drive
drive.mount('/content/drive')
path = '/content/drive/My Drive/Download2'
if not os.path.exists(path):
  os.mkdir(path)
os.chdir(path)
linkz = input("paste your link here")
print(type(linkz))
!wget -c $linkz --no-check-certificate

