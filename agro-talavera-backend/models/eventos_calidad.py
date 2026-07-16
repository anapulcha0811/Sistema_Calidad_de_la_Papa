# pyrefly: ignore [missing-import]
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from config import Base

class EventosCalidad(Base):
    __tablename__ = "eventos_calidad"

    id = Column(Integer, primary_key=True, index=True)
    producto_id = Column(Integer, ForeignKey("producto_agricola.id"))
    cod_atributo = Column(String, index=True)
    descripcion = Column(String)
    unidad_medida = Column(String)
    estandar = Column(String)
    nivel_calidad_p = Column(String)
    min = Column(Float)
    max = Column(Float)
    tipo_producto = Column(String)
