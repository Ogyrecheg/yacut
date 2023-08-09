from flask import flash, redirect, render_template

from . import app
from .forms import URLForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = URLForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    elif URLMap.short_link_exists(form.custom_id.data):
        flash(f'Имя {form.custom_id.data} уже занято!')
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        form=form,
        link=URLMap.create_link_and_add_in_db_new(
            form.data,
            form_data_exists=True
        )
    )


@app.route('/<short>')
def redirect_short_link(short):
    link = URLMap.get_link_by_short_id(short)
    return redirect(link.original)
