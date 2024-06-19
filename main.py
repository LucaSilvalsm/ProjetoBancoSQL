from sqlalchemy import create_engine, UniqueConstraint
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class Cliente(Base):
    """
    Representa um cliente.
    """
    __tablename__ = "cliente"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(30), nullable=False)
    sobrenome = Column(String(50), nullable=False)
    cpf = Column(String(11), nullable=False, unique=True)
    endereco = Column(String(50), nullable=False)
    contas = relationship("Contas", back_populates="cliente", cascade="all, delete-orphan")
    
    def __repr__(self):
        return (
            f"\nnome='{self.nome}',\n"
            f"sobrenome='{self.sobrenome}',\n"
            f"cpf='{self.cpf}',\n"
            f"endereco='{self.endereco}'"
        )
    
    def nome_completo(self):
        return f"{self.nome} {self.sobrenome}"


class Contas(Base):
    """
    Representa uma conta de cliente.
    """
    __tablename__ = "contas"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    tipo_conta = Column(String(30), nullable=False)
    agencia = Column(String(10), nullable=False, default='0001')
    conta = Column(Integer, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey('cliente.id'), nullable=False)
    cliente = relationship("Cliente", back_populates="contas")
    
    __table_args__ = (
        UniqueConstraint('conta', 'cliente_id', name='uq_conta_cliente'),
    )
    
    def __repr__(self):
        return (
            f"\nConta(id={self.id},\n"
            f"tipo_conta='{self.tipo_conta}',\n"
            f"agencia='{self.agencia}',\n"
            f"conta='{self.conta}' \n)"
        )
    
    def tipo_e_agencia(self):
        return f"Tipo: {self.tipo_conta}, Agência: {self.agencia}"


# Conectando com o banco de dados (usando SQLite em memória)
engine = create_engine("sqlite:///:memory:")

# Criando as tabelas no banco de dados
Base.metadata.create_all(engine)

# Criando uma sessão
Session = sessionmaker(bind=engine)

# Criando dados no banco
with Session() as session:
    # Criando clientes de exemplo
    lucas = Cliente(
        nome='Lucas',
        sobrenome='Moreira',
        cpf='16950453599',
        endereco='Rua Lucio'
    )
    
    sandy = Cliente(
        nome='Sandy',
        sobrenome='Ferreira',
        cpf='16913565987',
        endereco='Rua Professor Roberto'
    )
    
    amanda = Cliente(
        nome='Amanda',
        sobrenome='Oliveira',
        cpf='00513565987',
        endereco='Rua Jose Lopes Cansado'
    )
    
    # Adicionando clientes à sessão
    session.add_all([lucas, sandy, amanda])
    session.commit()
    
    # Criando contas para os clientes
    lucas_conta1 = Contas(tipo_conta='Corrente', cliente=lucas)    
    sandy_conta1 = Contas(tipo_conta='Corrente', cliente=sandy)
    amanda_conta1 = Contas(tipo_conta='Corrente', cliente=amanda)
    
    # Atribuindo manualmente os números de conta
    lucas_conta1.conta = 1
    sandy_conta1.conta = 2
    amanda_conta1.conta = 3
    
    # Adicionando contas à sessão
    session.add_all([lucas_conta1, sandy_conta1, amanda_conta1])
    session.commit()
    
    # Consulta para verificar os clientes e suas contas
    clientes = session.query(Cliente).all()
    for cliente in clientes:
        print(f"\n{cliente}\n")
        for conta in cliente.contas:
            print(f"{conta}\n")
