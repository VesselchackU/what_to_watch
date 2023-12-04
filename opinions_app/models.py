"""Модели приложения opinion_app."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime

from opinions_app import db


class Opinion(db.Model):
    """Модель мнения."""
    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False)
    text = Column(Text, unique=True, nullable=False)
    source = Column(String(256))
    timestamp = Column(DateTime, index=True, default=datetime.utcnow)
    added_by = Column(String(64))

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
