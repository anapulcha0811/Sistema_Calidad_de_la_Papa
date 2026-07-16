from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class MetricasCalidad(Base):
    __tablename__ = "metricas_calidad"

    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("padron_cultivo.id"))
    evento_id = Column(Integer, ForeignKey("eventos_calidad.id"))
    cod_inspeccion = Column(String)
    cod_muestra = Column(String)
    fecha_control = Column(String)
    cod_atributo = Column(String)
    descripcion = Column(String)
    resultado = Column(Float)
    simbolo = Column(String)
    nivel_calidad_m = Column(String)
    tamano_muestra = Column(Float)
    estado = Column(String) # Aprobado/Desaprobado
    
    lote = relationship("PadronCultivo")
