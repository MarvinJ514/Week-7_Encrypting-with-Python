#Python CA database Creator
#Author: Marvin Johnson
#Created: 2020-02-29
#Description: Creates CA Authority Database needed to store data ceritifcate
#data for application server.
import sqlite3

conn = sqlite3.connect('CA.db')
c = conn.cursor()
c.execute("""CREATE TABLE certificateAuthority (
        hostname text,
        key text
        )""")

conn.commit()
conn.close()