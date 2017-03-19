# app/home/views.py

from flask import render_template
from flask_login import current_user, login_required
import operator

from . import home
from .. import db
from ..models import RecommendArticle

@home.route('/')
def homepage():
    """
    Render the homepage template on the / route
    """
    return render_template('home/index.html', title="Welcome")

@home.route('/recommendarticles')
@login_required
def recommendarticles():
    """
    Render the recommendarticles template on the /recommendarticles route
    """

    rows = RecommendArticle.query.filter_by(user_id = current_user.id)
    
    # sort out 10 articles with the highest scores and with scores above a threshold value   
    all_articles = []
    recommendarticles = []
    score_threshold = 0.01
    article_count_limit = 10
    for row in rows:
        entries = [
            tuple((row.pmid_1, row.title_1, row.score_1)),
            tuple((row.pmid_2, row.title_2, row.score_2)),
            tuple((row.pmid_3, row.title_3, row.score_3)),
            tuple((row.pmid_4, row.title_4, row.score_4)),
            tuple((row.pmid_5, row.title_5, row.score_5)),
            tuple((row.pmid_6, row.title_6, row.score_6)),
            tuple((row.pmid_7, row.title_7, row.score_7)),
            tuple((row.pmid_8, row.title_8, row.score_8)),
            tuple((row.pmid_9, row.title_9, row.score_9)),
            tuple((row.pmid_10, row.title_10, row.score_10))
        ]
        all_articles += entries

    sorted_articles = sorted(all_articles, key=operator.itemgetter(2), reverse=True)

    if (len(sorted_articles) > article_count_limit):
        recommendarticles = sorted_articles[:article_count_limit]
    else:
        recommendarticles = sorted_articles

    return render_template('home/recommendarticles.html', 
    						recommendarticles=recommendarticles, 
    						title="Articles you may like")

