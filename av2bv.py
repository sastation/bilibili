#!/bin/env python3

table='fZodR9XQDSUm21yCkr6zBqiveYah8bt4xsWpHnJE7jL5VG3guMTKNPAwcF'
tr={}
for i in range(58):
	tr[table[i]]=i
s=[11,10,3,8,4,6]
xor=177451812
add=8728348608

def dec(x):
	r=0
	for i in range(6):
		r+=tr[x[s[i]]]*58**i
	return (r-add)^xor

def enc(x):
	x=(x^xor)+add
	r=list('BV1  4 1 7  ')
	for i in range(6):
		r[s[i]]=table[x//58**i%58]
	return ''.join(r)

print(dec("BV1fb411P71i"))
print(enc(34646692))

import sys
sys.exit(0)


# Update db: vc.bbvc02
import sqlite3
conn = sqlite3.connect("vc.db")
curs = conn.execute("select avnum from bbvc02;")
lines = curs.fetchall()

for item in lines:
    aid = item[0]
    bvid = enc(int(aid.lstrip("av")))
    print("%s, %s" % (aid, bvid))

    conn.execute("update bbvc02 set bvid=? where avnum=?;", (bvid, aid))



conn.commit()
conn.close()

