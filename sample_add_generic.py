#!/usr/bin/python

'''
J.Chan - Enterprise Infrastructure Services, University of Toronto

Sample script to add a single generic DNS record

Usages: python sample_add_generic.py "abc.test.utoronto.ca" "A" "192.168.100.1" "3600"

  - fqdn		DNS name
  - record_type		A,TXT,AAAA
  - rdata		Target data
  - TTL			Time-to-live in second

'''
import proteus,sys

def main():
        fqdn        = sys.argv[1]
        record_type = sys.argv[2]
        rdata       = sys.argv[3]
        ttl         = sys.argv[4]
        session = proteus.connect()
        proteus.add_generic(fqdn,record_type,rdata,ttl)
        proteus.logout()

if __name__ == "__main__":
   main()
