from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class MetricasCalidad(Base):
    __tablename__ = "metricas_calidad"

    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("padron_cultivo.id"))
    peso_muestra = Column(Float)
    porcentaje_almidon = Column(Float)
    estado = Column(String) # "APROBADO" o "DESAPROBADO"

    lote = relationship("PadronCultivo")
