#Python Certificate Authority Application
#Author: Marvin Johnson
#Created: 2020-02-29
#Description: CA server application is utilized to add, create and check 
#CA information within the sqlite database. 

import sqlite3

#Creates CA database entry for hostname/public key pari
def create_CA(conn, certificateAuthority):
    sql = "INSERT INTO certificateAuthority(hostname,key) VALUES (?,?)"
    cur = conn.cursor()
    cur.execute(sql, certificateAuthority)
    return cur.lastrowid

def addCAInfo(hostname,key):
    conn = sqlite3.connect('CA.db')
    with conn:
        certificateAuthority = (hostname,key)
        newCert = create_CA(conn,certificateAuthority)
    conn.commit()
    conn.close()

def checkCAInfo(hostname):
    conn = sqlite3.connect('CA.db')
    c = conn.cursor()
    c.execute("SELECT key FROM certificateAuthority WHERE hostname = '"+hostname+"'")
    return (c.fetchone())
    conn.commit()
    conn.close()
