# app/user/views.py

from flask import flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from . import user
from forms import UserArticleForm
from .. import db
from ..models import UserArticle

# User Views

@user.route('/userarticles', methods=['GET', 'POST'])
@login_required
def list_userarticles():
    """
    List articles entered by a user
    """
    try:
        userarticles = UserArticle.query.filter_by(user_id = current_user.id )
        db.session.commit()
    except:
        db.session.rollback()
        userarticles = UserArticle.query.filter_by(user_id = current_user.id )
        db.session.commit()

    return render_template('user/userarticles/userarticles.html',
                           userarticles=userarticles, title="User Articles")

@user.route('/userarticles/add', methods=['GET', 'POST'])
@login_required
def add_userarticle():
    """
    Add a userarticle to the database
    """
    add_userarticle = True

    form = UserArticleForm()
    if form.validate_on_submit():
        userarticle = UserArticle(pmid=form.pmid.data,
                                title=form.title.data,
                                abstract=form.abstract.data,
                                user_id=current_user.id)
        try:
            # add userarticle to the database
            db.session.add(userarticle)
            db.session.commit()
            flash('You have successfully added a new article.')
        except:
            # in case userarticle id already exists
            flash('Error: article already exists or text is too long')

        # redirect to userarticles page
        return redirect(url_for('user.list_userarticles'))

    # load userarticle template
    return render_template('user/userarticles/userarticle.html', action="Add",
                           add_userarticle=add_userarticle, form=form,
                           title="Add UserArticle")

@user.route('/userarticles/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_userarticle(id):
    """
    Edit a userarticle
    """
    add_userarticle = False

    try:
        userarticle = UserArticle.query.get_or_404(id)
    except:
        userarticle = UserArticle.query.get_or_404(id)
    form = UserArticleForm(obj=userarticle)
    if form.validate_on_submit():
        userarticle.pmid = form.pmid.data
        userarticle.title = form.title.data
        userarticle.abstract = form.abstract.data
        userarticle.user_id = current_user.id
        db.session.commit()
        flash('You have successfully edited the article.')

        # redirect to the userarticles page
        return redirect(url_for('user.list_userarticles'))

    form.pmid.data = userarticle.pmid
    form.title.data = userarticle.title
    form.abstract.data = userarticle.abstract
    return render_template('user/userarticles/userarticle.html', action="Edit",
                           add_userarticle=add_userarticle, form=form,
                           userarticle=userarticle, title="Edit UserArticle")

@user.route('/userarticles/delete/<int:id>', methods=['GET', 'POST'])
@login_required
def delete_userarticle(id):
    """
    Delete a userarticle from the database
    """
    try:
        userarticle = UserArticle.query.get_or_404(id)
    except:
        userarticle = UserArticle.query.get_or_404(id)
    db.session.delete(userarticle)
    db.session.commit()
    flash('You have successfully deleted the article.')

    # redirect to the userarticles page
    return redirect(url_for('user.list_userarticles'))

    return render_template(title="Delete UserArticle")