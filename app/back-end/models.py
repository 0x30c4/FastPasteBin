from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func
from sqlalchemy import Column, \
                DateTime, Integer, \
                String, Boolean, Text

Base = declarative_base()


class Bindata(Base):
    __tablename__ = "bindata"
    id = Column(Integer, primary_key=True, index=True)
    uuid = Column(String, nullable=False)
    meta_data = Column(Text, nullable=True)
    is_tmp = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deleted_at = Column(DateTime(timezone=True), nullable=True)

    def __repr__(self):
        return 'id: {}'.format(self.id)
