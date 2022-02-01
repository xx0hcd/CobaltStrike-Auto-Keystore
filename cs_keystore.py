#!/usr/bin/python3
#create custom Cobalt Strike ssl keystore using certbot standalone mode on Debian/Ubuntu.
#drawing heavily on this idea https://github.com/killswitch-GUI/CobaltStrike-ToolKit/blob/master/HTTPsC2DoneRight.sh
#xx0hcd

import subprocess
import sys
import os
import shutil

domain  = input("Enter the FQDN of the domain:  ")
path	= input("Enter the path of the Cobalt Strike install:  ")
path 	+= "/"
passwd	= input("Enter the password to use for keytool:  ")

try:
  if not os.geteuid() == 0:
      sys.exit("\nScript must be run as root/sudo.\n")
except:
    print("")

def required_check():
    keytool = 'keytool'
    certbot = 'certbot'
    find_key = shutil.which(keytool)
    if keytool not in str(find_key):
        print("[-] Keytool not found, is java installed?")
        print("apt-get install openjdk-11-jdk")
    find_cert = shutil.which(certbot)
    if certbot not in str(find_cert):
        print("[-] Certbot not found, is it installed?")
        print("apt-get install certbot")

def certbot():
    #run certbot in standalone mode
    cmd = ["certbot", "certonly", "--standalone", "-d", domain, "--register-unsafely-without-email", "--agree-tos"]
    subprocess.run(cmd)
    #todo check if file exists before continue?
    
def cs_store():
    #change to the letsencrypt dir
    dir1 = "/etc/letsencrypt/live/" + domain
    os.chdir(dir1)
    
    #create the .p12 file
    print("\n[+] Creating .p12 file.\n")
    p12_file = domain + ".p12"
    p12_pass = "pass:" + passwd
    p12_cmd = ["openssl", "pkcs12", "-export", "-in", "fullchain.pem", "-inkey", "privkey.pem", "-out", p12_file, "-name", domain, "-passout", p12_pass]
    subprocess.run(p12_cmd)
    print("\n[+] Finished creating .p12 file.\n")    

    #create the .store file
    print("\n[+] Creating .store file.\n")
    store_file = domain + ".store"
    store_cmd = ["keytool", "-importkeystore", "-deststorepass", passwd, "-destkeypass", passwd, "-destkeystore", store_file, "-srckeystore", p12_file, "-srcstoretype", "PKCS12", "-srcstorepass", passwd, "-alias", domain]
    subprocess.run(store_cmd)
    print("[+] Finished creating .store file.\n")    

    #copy .store to cs install dir
    shutil.copy(store_file, path)
    
    
    print("Copy/Paste to Malleable C2 Profile:\n")
    output = """
    https-certificate {
        set keystore "%s";
        set password "%s";
    }"""%(store_file,passwd)
    print(output)
    
    
def main():
    required_check()
    certbot()
    cs_store()

if __name__ == "__main__":
    try:       
        main()
        print("\n[+] Finished.")
    except IOError as e:
        print(e)

    except KeyboardInterrupt:
        print("[+] Aborted by user.")
        sys.exit(3)    
