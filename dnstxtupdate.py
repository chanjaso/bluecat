#!/usr/bin/python

'''

Update existing TXT record

Last updated:   Oct 19, 2020
By:             Jason Chan - ITS

'''
import proteus, sys, socket

def main():
	fqdn	= sys.argv[1]
	rr	= sys.argv[2]
	session = proteus.connect()
        proteus.update(fqdn,rr)
	proteus.logout()

if __name__ == "__main__":
   main()
