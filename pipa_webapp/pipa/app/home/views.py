# app/home/views.py

from flask import render_template
from flask_login import current_user, login_required
import operator
from datetime import datetime, timedelta

from . import home
from .. import db
from ..models import RecommendArticle, UserArticle

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
    try:
        rows = RecommendArticle.query.filter_by(user_id = current_user.id)
        userarticles = UserArticle.query.filter_by(user_id = current_user.id)
        db.session.commit()
    except:
        db.session.rollback()
        rows = RecommendArticle.query.filter_by(user_id = current_user.id)
        userarticles = UserArticle.query.filter_by(user_id = current_user.id)
        db.session.commit()
    userarticle_pmids = []
    for userarticle in userarticles:
        userarticle_pmids.append(int(userarticle.pmid))
    userarticle_pmids = list(set(userarticle_pmids))

    dt = datetime.now()
    dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
    # sort out 10 articles with the highest scores and with scores above a threshold value
    all_articles = []
    recommendarticles = []
    score_threshold = 0.05
    article_count_limit = 10
    for row in rows:
        if (row.entry_date >= dt - timedelta(days=7)):
            entries = [
                tuple((row.pmid_1, row.title_1, row.score_1, row.entry_date.date())),
                tuple((row.pmid_2, row.title_2, row.score_2, row.entry_date.date())),
                tuple((row.pmid_3, row.title_3, row.score_3, row.entry_date.date())),
                tuple((row.pmid_4, row.title_4, row.score_4, row.entry_date.date())),
                tuple((row.pmid_5, row.title_5, row.score_5, row.entry_date.date())),
                tuple((row.pmid_6, row.title_6, row.score_6, row.entry_date.date())),
                tuple((row.pmid_7, row.title_7, row.score_7, row.entry_date.date())),
                tuple((row.pmid_8, row.title_8, row.score_8, row.entry_date.date())),
                tuple((row.pmid_9, row.title_9, row.score_9, row.entry_date.date())),
                tuple((row.pmid_10, row.title_10, row.score_10, row.entry_date.date()))
            ]
            all_articles += entries

    sorted_articles = sorted(all_articles, key=operator.itemgetter(2), reverse=True)
    unique_articles = []
    for article in sorted_articles:
        if (len(unique_articles) == 0 or (article[0] != unique_articles[-1][0])):
            if (article[2] > score_threshold and article[0] > 100):
                unique_articles.append(article)
    unique_articles = sorted(unique_articles, key=operator.itemgetter(3), reverse=True)

    if (len(unique_articles) > article_count_limit):
        recommendarticles = unique_articles[:article_count_limit]
    else:
        recommendarticles = unique_articles

    return render_template('home/recommendarticles.html',
    						recommendarticles=recommendarticles,
    						title="Articles you may like")

