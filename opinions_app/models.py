"""Модели приложения opinion_app."""

from datetime import datetime
from random import randrange
from typing import TypeVar, Type

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.orm import validates

from flask import abort

from opinions_app import db
from opinions_app.error_handlers import InvalidAPIUsage

Exc = TypeVar("Exc", bound=Exception)


class Opinion(db.Model):
    """Модель мнения."""
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    text = Column(Text, unique=True, nullable=False)
    source = Column(String(256))
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    added_by = Column(String(64))

    def __init__(self, data: dict = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if data:
            self.from_dict(data)

    def to_dict(self):
        """Возвращает объект в виде словаря."""
        return dict(
            id=self.id,
            title=self.title,
            text=self.text,
            source=self.source,
            timestamp=self.timestamp,
            added_by=self.added_by
        )

    def from_dict(self, data: dict):
        for field in ['title', 'text', 'source', 'added_by']:
            if field in data:
                setattr(self, field, data[field])

    @classmethod
    def random_opinion(cls):
        count = cls.query.count()
        if count:
            offset = randrange(count)
            opinion = cls.query.offset(offset).first()
            return opinion
        return None

    @classmethod
    def get_opinion_for_api(cls, id: int, message: str = None):
        opinion = cls.query.get(id)
        message = message or f'Мнение с id=={id} не найдено.'
        if not opinion:
            raise InvalidAPIUsage(message, 404)
        return opinion

