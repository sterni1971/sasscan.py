#!/usr/bin/python
# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
#
# sasscan script
# Determine the drive bay slot numbering of disks connected to LSI sas controllers
#
# Requires sas3ircu utility obtained from LSI website

import os
import subprocess

def getVDEV():
	devHash={}
	path="/dev/disk/by-vdev/"
	files=os.listdir(path)
	for f in files:
		link=os.readlink(path+f).split('/')[-1]
		devHash[link]=f

	return(devHash)
	
	

if __name__ == "__main__":


	prc=subprocess.Popen(['/root/sas3ircu','0','DISPLAY'],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	(sout,serr)=prc.communicate()

	vdev=getVDEV()

	ishdd=False
	for line in sout.splitlines():
		sline=line.strip()

		if sline.startswith("Device"):
			if sline=='Device is a Hard disk':
				ishdd=True
        			encl=-1
        			slot=-1
				guid=-1

			else:
				ishdd=False

		if sline.startswith("Enclosure #"):
			encl=int(sline[sline.find(':')+2:])

		if sline.startswith("Slot #") and ishdd:
			slot=int(sline[sline.find(':')+2:])

		if sline.startswith("GUID") and ishdd:
			guid=sline[sline.find(':')+2:]
    			file="/dev/disk/by-id/wwn-0x{}".format(guid)
			disk=os.readlink(file).split('/')[-1]
        		print("{:02d}:{:02d} {:38} {:4} {:3}".format(encl,slot,file,disk,vdev[disk]))

