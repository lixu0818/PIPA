import urllib3
from bs4 import BeautifulSoup
import certifi
import time
import datetime
import MySQLdb
from recEngine import recommend

def crawl(db):
    """
    Extract articles from PubMed, parse the data, and then load into MySQL db.

    :type db: MySQL db connector
    :rtype: void
    """
    cur = db.cursor()

    dailyMax = 3000
    batchNum = 20
    sleeptimeforPubmed = 5
    backstep = 20

    cur.execute('select pmid from articles order by pmid desc')
    startingPMID = cur.fetchall()[backstep][0]

	################
	# for testing
    # startingPMID=28315500

    cur.execute('truncate table articles')
    for i in range (startingPMID, startingPMID+dailyMax, batchNum):
        PMIDs = ""

        for j in range (batchNum):
            PMIDs = PMIDs + str(i + j ) +","

        url = "https://www.ncbi.nlm.nih.gov/pubmed/"+ PMIDs +"?report=medline&format=text"

        time.sleep(sleeptimeforPubmed)
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED',ca_certs=certifi.where())
        r = http.request('GET', url)
        soup = BeautifulSoup(r.data, "lxml")

        allInfo = unicode(soup.pre.string)

        if allInfo.find('PMID- ')<0:
            print url
            print 'extraction complete'
            break

        while (allInfo.find('AB  -')>0 and allInfo.find('TI  -')>0):
            IdIndexStart = allInfo.index('PMID- ')+6
            IdIndexEnd = allInfo.index('\n', IdIndexStart)
            PMID = allInfo[IdIndexStart:IdIndexEnd]

            try:
                tiIndexStart = allInfo.index('TI  -')+6

                if allInfo.find(  'PG  -', tiIndexStart)>0:
                    tiIndexEnd =   allInfo.index('PG  -', tiIndexStart)-1
                elif allInfo.find('LID -', tiIndexStart)>0:
                    tiIndexEnd =   allInfo.index('LID -', tiIndexStart)-1
                else:
                    tiIndexEnd =   allInfo.index('AB  -', tiIndexStart)-1
                ti = allInfo[tiIndexStart:tiIndexEnd]

            except:
                ti =""

            abIndexStart = allInfo.index('AB  -')+6
            try:
                abIndexEnd =   allInfo.index('FAU -', abIndexStart)-1
            except:
                abIndexEnd = abIndexStart + 1000
            ab = ti+"        Abstract:"+allInfo[abIndexStart:abIndexEnd]

            query = "insert into articles (pmid, abstract) values ("+ PMID +", '"+ ab + "')"
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
        query = 'insert into last_pmid (record_date, pmid) values ("%s", %d)'%(now, endingPMID)
        cur.execute(query)
        db.commit()

if __name__ == "__main__":
    db = MySQLdb.connect(host="pipa.mysql.pythonanywhere-services.com",
                         user="pipa",
                         passwd="piparoot",
                         db="pipa$pipa_db")
    crawl(db)
    recommend(db)
    db.close()
