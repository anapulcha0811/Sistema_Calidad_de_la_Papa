from sqlalchemy import Column, Integer, String, Float, ForeignKey
from config import Base

class InformeCalidad(Base):
    __tablename__ = "informe_calidad"

    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("padron_cultivo.id"))
    cod_inspeccion = Column(String)
    aprobado = Column(String)
    nivel_calidad_m = Column(String)
    tamano_muestra = Column(Integer)
