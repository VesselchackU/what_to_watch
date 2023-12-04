from datetime import datetime
from flask import Flask, render_template, redirect, url_for, flash, abort
from flask_sqlalchemy import SQLAlchemy
from random import randrange
from sqlalchemy import Column, Integer, String, DateTime, Text
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, Length, Optional
from flask_migrate import Migrate
import click
import csv

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = ';lkajdfmskoqpoiupjfq2wpij98(*;lkjasdfjjh!!a'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Opinion(db.Model):
    """Модель мнения."""
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    text = Column(Text, unique=True, nullable=False)
    source = Column(String(256))
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    added_by = Column(String(64))

class OpinionForm(FlaskForm):
    title = StringField(
        'Введите название фильма',
        validators=[
            DataRequired(message='Обязательное поле'),
            Length(1, 128)
        ],
    )
    text = TextAreaField(
        'Напишите мнение',
        validators=[DataRequired(message='Обязательное поле')]
    )
    source = URLField(
        'Добавьте ссылку на подробный обзор фильма',
        validators=[Length(1, 256), Optional()]
    )
    submit = SubmitField('Добавить')


@app.cli.command('load_opinions')
def load_opinions_command():
    """Функция загрузки мнений в БД."""
    with open('opinions.csv', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        counter = 0
        for row in reader:
            opinion = Opinion(**row)
            db.session.add(opinion)
            db.session.commit()
            counter += 1
    click.echo(f'Загружено {counter} мнений.')


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    render_template('500.html'), 500


@app.route('/')
def index_view():
    quantity = Opinion.query.count()
    if not quantity:
        abort(404)
    offset_val = randrange(quantity)
    opinion = Opinion.query.offset(offset_val).first()
    return render_template('opinion.html', opinion=opinion)


@app.route('/add', methods=['GET', 'POST'])
def add_opinion_view():
    form = OpinionForm()
    if form.validate_on_submit():
        text = form.text.data
        if Opinion.query.filter_by(text=text).first is not None:
            flash('Есть такое мнение, причем не только Ваше.')
            return render_template('add_opinion.html', form=form)
        opinion = Opinion(
            title=form.title.data,
            text=form.text.data,
            source=form.source.data
        )
        db.session.add(opinion)
        db.session.commit()
        return redirect(url_for('opinion_view', id=opinion.id))
    return render_template('add_opinion.html', form=form)


@app.route('/opinions/<int:id>')
def opinion_view(id: int):
    opinion = Opinion.query.get_or_404(id)
    return render_template('opinion.html', opinion=opinion)


if __name__ == '__main__':
    app.run()
