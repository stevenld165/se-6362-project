from typing import List
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from sqlalchemy import create_engine

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)

class Website(db.Model):
    __tablename__ = "website"

    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str]
    desc: Mapped[str]
    accesses: Mapped[int]
    sponsorMoney: Mapped[float]

    kwic_entries: Mapped[List["KwicEntry"]] = relationship(back_populates="website", cascade="all, delete-orphan")

    def __repr__(self) -> str:
        return f"Website(id={self.id!r}, url={self.url!r}, desc={self.desc!r}, accesses={self.accesses!r}, sponsorMoney={self.sponsorMoney!r})"

class KwicEntry(db.Model):
    __tablename__ = "kwic"

    id: Mapped[int] = mapped_column(primary_key=True)
    website_id: Mapped[int] = mapped_column(ForeignKey("website.id"))
    first_word: Mapped[str] = mapped_column(index=True)
    first_word_filtered: Mapped[str] = mapped_column(index=True)
    full_circular_shift: Mapped[str]

    website: Mapped["Website"] = relationship(back_populates="kwic_entries")

    def __repr__(self) -> str:
        return f"KwicEntry(id={self.id!r}, website={self.website!r}, first_word={self.first_word!r}, first_word_filtered={self.first_word_filtered!r} full_circular_shift={self.full_circular_shift!r})"

# engine = create_engine("sqlite://", echo=True)

# Base.metadata.create_all(engine)