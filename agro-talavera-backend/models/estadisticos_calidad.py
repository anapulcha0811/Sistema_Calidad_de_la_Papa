from sqlalchemy import Column, Integer, String, ForeignKey
from config import Base

class EstadisticosCalidad(Base):
    __tablename__ = "estadisticos_calidad"

    id = Column(Integer, primary_key=True, index=True)
    informe_id = Column(Integer, ForeignKey("informe_calidad.id"))
    cod_atributo = Column(String)
    descripcion = Column(String)
    nivel_calidad_m = Column(String)
