"""Валидаторы."""
from opinions_app.models import Opinion


def validate_opinion_text_unique(text: str):
    """Возвращает False, если в БД есть запись с таким же текстом мнения."""
    return not bool(Opinion.query.filter_by(text=text).first())
