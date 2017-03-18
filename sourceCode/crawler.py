import urllib3
from bs4 import BeautifulSoup
import requests
import certifi
import time
import datetime
import MySQLdb
from recEngine import recommend

def crawl():
	db = MySQLdb.connect(host="localhost",    # your host, usually localhost
                     user="root",         # your username
                     #passwd="xpx",  # your password
                     db="xudatabase")        # name of the data base
	cur = db.cursor()

	dailyMax = 1000
	batchNum = 20
	sleeptimeforPubmed =5
	backstep =20

	cur.execute('select pmid from last_pmid')
	endingPMID = max(cur.fetchall())
	startingPMID=endingPMID[0] -backstep #
	cur.execute('truncate articles')
	for i in range (startingPMID, startingPMID+dailyMax, batchNum):
	    PMIDs = ""
	    
	    for j in range (batchNum):
	        PMIDs = PMIDs + str(i + j ) +","
        
	    url = "https://www.ncbi.nlm.nih.gov/pubmed/"+ PMIDs +"?report=medline&format=text" 
	    
	    #time.sleep(sleeptimeforPubmed)
	    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
	    r = http.request('GET', url)
	    soup = BeautifulSoup(r.data, "lxml")
	       
	    allInfo = unicode(soup.pre.string)
	    
	    if allInfo.find('PMID- ')<0:
	        print url
	        print 'bad end'        
	        break
	    
	    while allInfo.find('AB  -')>0:
	        IdIndexStart = allInfo.index('PMID- ')+6
	        IdIndexEnd = allInfo.index('\n', IdIndexStart)
	        PMID = allInfo[IdIndexStart:IdIndexEnd]
	    
	        abIndexStart = allInfo.index('AB  -')+6
	        abIndexEnd = allInfo.index('\n', abIndexStart)
	        ab = allInfo[abIndexStart:abIndexEnd]
	    
	        query = "insert into articles values ("+ PMID +", '"+ ab + "')"
	        endingPMID = int(PMID)
	        if (endingPMID%10==0):
	            print endingPMID

	        try:
	            cur.execute(query)
	            db.commit()

	        except:
	            db.rollback()
	           
	        allInfo = allInfo[abIndexEnd:]
	        
	now = datetime.datetime.now()       
	query = 'insert into last_pmid values ("%s", %d)'%(now, endingPMID)
	cur.execute(query)
	db.commit()
	db.close() 


if __name__ == "__main__":
    #crawl()
    recommend()