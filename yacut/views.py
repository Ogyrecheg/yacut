from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLForm
from .models import URLMap
from .utils import make_short_link


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    if not form.custom_id.data:
        form.custom_id.data = make_short_link()
    elif URLMap.check_short_link_exists(form.custom_id.data):
        flash(f'Имя {form.custom_id.data} уже занято!')
        return render_template('index.html', form=form)

    link = URLMap.create_link_and_add_in_db(
        form.original_link.data,
        form.custom_id.data,
    )
    return render_template('index.html', form=form, link=link)


@app.route('/<short>')
def redirect_short_link(short):
    link = URLMap.get_link_by_short_id(short)
    if not link:
        abort(404)
    return redirect(link.original)
