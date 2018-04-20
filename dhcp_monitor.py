#!/usr/bin/python

from scapy.all import *
import smtplib
import sys


LEG_IP = "192.168.56.100"
LEG_MAC = "08:00:27:d1:dd:aa"

# search in lst val for fld
def getval(lst,fld):
    for p in lst:
	if type(p) is tuple:
	    if p[0]==fld: return p[1]
    return None

# err and exit
def exterr(msg):
    print (msgcd) 
    sys.exit(1)              


#main
#check args
if len(sys.argv) != 2:
    exterr("Usage: " + sys.argv[0] + " <iface>")
myif=sys.argv[1]

#mk pktboot
conf.checkIPaddr = False
fam,hw = get_if_raw_hwaddr(myif)
pktboot = Ether(src=hw, dst="ff:ff:ff:ff:ff:ff")/IP(src="0.0.0.0", dst="255.255.255.255")/UDP(sport=68, dport=67)/BOOTP(chaddr=hw)

#mk discovery
dhdisc = DHCP(options=[("message-type","discover"),"end"])

ans, uanspktask = srp(pktboot/dhdisc, timeout=2,iface=myif, multi=True)
message = ''
for p in ans: 
	print p[1][Ether].src, p[1][IP].src
	if p[1][IP].src == LEG_IP:
		message = message + "leg_ip "
	else:
		message = message + "neleg_ip "
	message = message + str(p[1][IP].src) + "\n"
	

sender = "sender_mail@gmail.com"
psw = "qwerty123"
recipient = ["recepient_mail@gmail.com"]
mes = message

#sending ip-addresses to mail
def sendToEmail(sender, psw, recipient, message):

    server = smtplib.SMTP("smtp.gmail.com", 587)

    try:
        server.starttls()
        server.login(sender, psw)
        server.sendmail(sender, recipient, message)
	#print mes
        return True
    except Exception as e:
        print("The message was not sent")
        print(e)
    finally:
        server.quit()

    return False

sendToEmail(sender, psw, recipient, mes)
