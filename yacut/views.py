from flask import flash, redirect, render_template

from . import app, db
from .forms import URLForm
from .models import URLMap
from .utils import make_short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    custom_id = form.custom_id.data
    if not custom_id:
        custom_id = make_short_link()
    elif URLMap.query.filter_by(short=custom_id).first() is not None:
        flash(f'Имя {custom_id} уже занято!')
        return render_template('index.html', form=form)
    link = URLMap(
        original=form.original_link.data,
        short=custom_id,
    )
    db.session.add(link)
    db.session.commit()
    return render_template('index.html', form=form, link=link)


@app.route('/<short>')
def redirect_short_link(short):
    link = URLMap.query.filter_by(short=short).first_or_404()
    return redirect(link.original)
