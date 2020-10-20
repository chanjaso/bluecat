#!/usr/bin/python

'''
Bluecat Main API class to update TXT records

Last updated:   Oct 19, 2020
By:             Jason Chan - ITS

'''

from zeep import Client
import re, time

# Bluecat Parameters
BAMAddress="PROTEUS_ADDRESS"
url="https://"+BAMAddress+"/Services/API?wsdl"
account="YOUR_API_USERNAME"
account_password="YOUR_API_PASSWORD"
config_name="CONFIG_NAME"
view_name="VIEW"
session = Client(url)
verbose = True

def connect():
	session.service.login(account,account_password)
	return session

def logout():
	session.service.logout()

def get_viewinfo():
	configinfo = session.service.getEntityByName(0,config_name,"Configuration")
	viewinfo = session.service.getEntityByName(configinfo.id,view_name,"View")
	return viewinfo

def get_next_object(parent,name):
	object_types = ['Zone','GenericRecord','HostRecord','TXTRecord']
	for object_type in object_types:
		new = session.service.getEntityByName(parent.id, name, object_type)
		if new.id != 0L:
			return new
	if new.id == 0L:
		return 0

def update(fqdn,rdata):
	if verbose:
		print "Process update: " + fqdn
	domain	= fqdn
	fqdn	= fqdn.split(".")
	parent	= get_viewinfo()
	while fqdn:
		name    = fqdn.pop()
		new     = get_next_object(parent, name)
		if new:
			if new.type == 'Zone':
				parent = new
			else:
                            if new.type == 'TXTRecord':
                                nprop  = "|absoluteName=" + domain + "|txt=" + rdata +"|"
                                new.properties = nprop
                                session.service.update(new)
                                return 1
	return 0
