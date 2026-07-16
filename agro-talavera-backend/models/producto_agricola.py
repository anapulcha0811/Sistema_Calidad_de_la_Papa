from sqlalchemy import Column, Integer, String, ForeignKey
from config import Base

class ProductoAgricola(Base):
    __tablename__ = "producto_agricola"

    id = Column(Integer, primary_key=True, index=True)
    padron_id = Column(Integer, ForeignKey("padron_cultivo.id"))
    codigo = Column(String, index=True)
    cod_atributo = Column(String, index=True)
    descripcion = Column(String)
    cualitativo = Column(String)
    unidad_medida = Column(String)
