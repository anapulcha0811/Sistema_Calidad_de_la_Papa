from sqlalchemy import Column, Integer, String, Float, Date
from config import Base

class PadronCultivo(Base):
    __tablename__ = "padron_cultivo"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String, unique=True, index=True)
    nombre = Column(String, index=True)
    cantidad_lote = Column(Float)
    fecha_ingreso = Column(Date)
    tipo_producto = Column(String)
    cod_inspeccion = Column(String, unique=True, index=True)
