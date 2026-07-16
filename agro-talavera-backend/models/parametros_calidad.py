from sqlalchemy import Column, Integer, String, Float, ForeignKey
from config import Base

class ParametrosCalidad(Base):
    __tablename__ = "parametros_calidad"

    id = Column(Integer, primary_key=True, index=True)
    evento_id = Column(Integer, ForeignKey("eventos_calidad.id"))
    cod_atributo = Column(String)
    descripcion = Column(String)
    nivel_calidad_p = Column(String)
    min = Column(Float)
    max = Column(Float)
