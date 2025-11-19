#!/usr/bin/python

'''

J.Chan - Enterprise Infrastructure Services, University of Toronto

Proteus API module

'''

from zeep import Client

### Bluecat Parameters ###
BAMAddress="FQDN OF THE SERVER"
account="USERNAME"
account_password="PASSWORD"
config_name="Production"
view_name="Public"
##########################

url="https://"+BAMAddress+"/Services/API?wsdl"
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
	object_types = ['Zone','GenericRecord','HostRecord','TXTRecord','AliasRecord']
	for object_type in object_types:
		new = session.service.getEntityByName(parent.id, name, object_type)
		if new.id != 0L:
			return new
	if new.id == 0L:
		return 0

def search(search_string,object_type):
	searchresults = session.service.searchByObjectTypes(search_string,object_type, 0, 1)
	return searchresults


def delete(fqdn):
        if verbose:
                print "BAM: Process del for: " + fqdn
	fqdn    = fqdn.split(".")
	parent	= get_viewinfo()
	while fqdn:
		name	= fqdn.pop()
		new 	= get_next_object(parent, name)
		if new:
			if new.type == 'Zone':
				parent = new
			else:
				session.service.delete(new.id)
				return 1
	return 0

def delete_lamp_site(domain):
	hosts   = ['www','ftp','m','webmail','admin','mail','','']

        for host in hosts:
                fqdn    = (host + '.' + domain)
                delete(fqdn)

def add_host(fqdn,rdata,ttl):
        parent = get_viewinfo()
        if verbose:
                print "BAM: Process add for: " + fqdn
        try:
                session.service.addHostRecord(parent.id,fqdn,rdata,ttl,"")
        except:
                print "Error"
                return 0
        else:
                return 1

def add_zone(fqdn):
        fqdn    = fqdn.split(".")
        parent  = get_viewinfo()
        while fqdn:
                name    = fqdn.pop()
                new     = get_next_object(parent, name)
                if new:
                        if new.type == 'Zone':
                                parent = new
                        else:
                                session.service.addZone(new.id)
                                return 1
	return 0

def add_ipv4_address(ip,mac,fqdn,state):
        configinfo = session.service.getEntityByName(0,config_name,"Configuration")
        parent = get_viewinfo()
        if state == "static":
            targetState = "MAKE_STATIC"
        elif state == "dhcp":
            targetState = "MAKE_DHCP_RESERVED"
        if fqdn == "0" or not fqdn:
            hostInfo = ""
        else:
            hostInfo = "{},{},{},{}".format(fqdn, parent.id, "true", "false")
        if verbose:
            print "BAM: Process add for: " + ip + " " + mac + " " + fqdn
        try:
            session.service.assignIP4Address(configinfo.id,ip,mac,hostInfo,targetState,"")
        except:
            print "Error"
            return 0
        else:
            print "Added"
            return 1

def add_generic(fqdn,record_type,rdata,ttl):
	parent = get_viewinfo()
	if verbose:
		print "BAM: Process add for: " + fqdn
	try:
		session.service.addGenericRecord(parent.id,fqdn,record_type,rdata,ttl,"")
	except:
		return 0
	else:
		return 1

def add_AliasRecord(fqdn,rdata,ttl):
	parent = get_viewinfo()
        if verbose:
                print "BAM: Process CNAME add for: " + fqdn
        try:
                session.service.addAliasRecord(parent.id,fqdn,rdata,ttl,"")
        except:
                return 0
        else:
                return 1

def add_txt(fqdn,rdata,ttl):
	parent = get_viewinfo()
        if verbose:
                print "BAM: Process add for: " + fqdn
	try:
		session.service.addTXTRecord(parent.id,fqdn,rdata,ttl,"")
	except:
		return 0
	else:
		return 1
