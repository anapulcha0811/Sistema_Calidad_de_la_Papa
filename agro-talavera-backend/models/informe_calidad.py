from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from config import Base

class InformeCalidad(Base):
    __tablename__ = "informe_calidad"

    id = Column(Integer, primary_key=True, index=True)
    lote_id = Column(Integer, ForeignKey("padron_cultivo.id"))
    fecha_informe = Column(Date)
    dictamen_final = Column(String)
    
    lote = relationship("PadronCultivo")
