import pandas as pd
import time
import datetime
import redis
from flask import current_app
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import MySQLdb

def import_data_articles(table_name, cur):
    ds = cur.execute('select pmid, abstract from ' +table_name)
    r = cur.fetchall()
    return pd.DataFrame(list(r),columns=['PMID', 'abstract'])

def import_user_articles(userId, cur):
    cur.execute('select pmid, title, abstract from user_articles where user_id=%d'% (userId))
    r = cur.fetchall()
    userdata= pd.DataFrame(list(r),columns=['PMID', 'title', 'abstract'])
    userdata['abstract'] = userdata['title']+'        Abstract:'+userdata['abstract']
    userpool = userdata[['PMID', 'abstract']]
    return userpool

def train(userpool, dailypool, userId, cur, db):
    ds = pd.concat([userpool, dailypool])
    ds.reset_index(drop=True, inplace=True)
    
    #clean up not ASCII chars
    ds['abstract'] = ds["abstract"].apply(lambda x: ''.join([" " if ord(i) < 32 or ord(i) > 126 else i for i in x]))
    
    tf = TfidfVectorizer(analyzer='word',
                             ngram_range=(1, 3),
                             min_df=0,
                             stop_words='english')
    tfidf_matrix = tf.fit_transform(ds['abstract'])
    print tfidf_matrix.shape
    print userpool.shape
    cosine_similarities = linear_kernel(tfidf_matrix[:userpool.shape[0]], tfidf_matrix[userpool.shape[0]:])
    similarities = pd.DataFrame(cosine_similarities)
    
    prediction_matrix = pd.DataFrame(data=userpool.PMID, columns=['PMID'], index=userpool.index)
    similarity_scores = prediction_matrix.copy()
    abstract_matrix = prediction_matrix.copy()
    
    top_n = 12
    if (ds.shape[0] < top_n):
        top_n = ds.shape[0] + 1

    for i in range(1,top_n-1):
        col_name = i
        prediction_matrix[col_name] = None
        similarity_scores[col_name] = -1
        abstract_matrix[col_name] = None

    now = datetime.datetime.now()
    
    for idx in range(userpool.shape[0]):
        print "idx: %s" % idx
        similar_indices = cosine_similarities[idx].argsort()[:-top_n:-1]
        print "similar indices: %s" % similar_indices
        similar_items = [[cosine_similarities[idx][i], ds['PMID'][i], ds['abstract'][i]]for i in similar_indices]
        #print "similar items: \n %s" % similar_items
        for i in range(0,top_n-2): 

            prediction_matrix.ix[idx, i] = similar_items[i][1] # insert into db directly 
            similarity_scores.ix[idx, i] = similar_items[i][0] # insert into a db table with date
            
            print similar_items[i][0]
            print similar_items[i][1]
            print similar_items[i][2]
            titleEnd = similar_items[i][2].index('        Abstract:')
            print i
            similar_items[i][2] = similar_items[i][2][:titleEnd].replace('\"', ' ')

        query = 'insert into recommend_articles (\
        entry_date, user_id, source_pmid,\
        pmid_1, pmid_2, pmid_3, pmid_4, pmid_5, pmid_6, pmid_7, pmid_8, pmid_9,pmid_10, \
        score_1, score_2, score_3,score_4, score_5, score_6, score_7, score_8, score_9, score_10,\
       title_1, title_2, title_3, title_4, title_5, title_6, title_7, title_8, title_9, title_10 ) \
        values \
        ("%s", %d, %d,\
            %d, %d, %d, %d, %d,\
            %d, %d, %d, %d, %d,\
            %.6f,%.6f,%.6f,%.6f,%.6f,\
            %.6f,%.6f,%.6f,%.6f,%.6f,\
            "%s","%s","%s","%s","%s",\
            "%s","%s","%s","%s","%s")'%(now, userId,userpool.ix[idx,'PMID'],\
                                                         similar_items[0][1],similar_items[1][1],similar_items[2][1],\
                                                         similar_items[3][1],similar_items[4][1],similar_items[5][1],\
                                                         similar_items[6][1],similar_items[7][1],similar_items[8][1],\
                                                         similar_items[9][1],\
                                                         similar_items[0][0],similar_items[1][0],similar_items[2][0],\
                                                         similar_items[3][0],similar_items[4][0],similar_items[5][0],\
                                                         similar_items[6][0],similar_items[7][0],similar_items[8][0],\
                                                         similar_items[9][0],\
                                                         similar_items[0][2],similar_items[1][2],similar_items[2][2],\
                                                         similar_items[3][2],similar_items[4][2],similar_items[5][2],\
                                                         similar_items[6][2],similar_items[7][2],similar_items[8][2],\
                                                         similar_items[9][2])
        print query
        cur.execute(query)
        db.commit()
    return 1;


def recommend(db):
    start = time.time()
    cur = db.cursor()
    dailypool = import_data_articles('articles', cur)
    
    cur.execute('select user_id from user_articles')
    userIdlist = list(set(cur.fetchall()))
    
    for id in userIdlist:
        userpool = import_user_articles(id[0], cur)
        print '##################'
        train(userpool, dailypool, id[0], cur, db)
    
    print("Engine trained in %s seconds." % (time.time() - start))


