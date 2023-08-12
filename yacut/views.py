from flask import abort, flash, redirect, render_template

from . import app
from .exceptions import ShortLinkExists, ShortURLNotFound
from .forms import URLForm
from .services import URLMapCreator


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        URLMapCreator.short_link_exists(form.custom_id.data)
    except ShortLinkExists:
        flash(f'Имя {form.custom_id.data} уже занято!')
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        form=form,
        link=URLMapCreator.create_link_and_add_in_db_new(
            form.data,
            form_data_exists=True
        )
    )


@app.route('/<short>')
def redirect_short_link(short):
    try:
        link = URLMapCreator.get_link_by_short_id(short)
        return redirect(link.original)
    except ShortURLNotFound:
        abort(404)
