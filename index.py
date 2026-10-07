from sqlite3 import IntegrityError

from dotenv import load_dotenv
from sqlalchemy import create_engine, String, Text, Integer, Float, ForeignKey, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session, relationship
from typing import List, Optional
import os

class Base(DeclarativeBase):
    pass

class Empresa(Base):
    __tablename__ = "tabela_empresa"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(250))
    local: Mapped[str] = mapped_column(Text)
    email: Mapped[str] = mapped_column(String(250))

    jogos: Mapped[List["Jogo"]] = relationship(
        back_populates="empresa"
    )


class Jogo(Base):
    __tablename__ = "tabela_jogo"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(250))
    tempo_jogo: Mapped[float] = mapped_column(Float)
    faixa_etaria: Mapped[int] = mapped_column(Integer)

    empresa_id: Mapped[int] = mapped_column(
        ForeignKey("tabela_empresa.id")
    )

    empresa: Mapped["Empresa"] = relationship(
        back_populates="jogos"
    )

def conectar_banco():
    print("\n--- SELEÇÃO DE BANCO DE DADOS ---")
    print("1- MySQL")
    print("2- SQLite")
    opcao_db = int(input("Escolha o banco de dados: "))

    if opcao_db == 1:
        load_dotenv()
        MYSQL_USER = os.getenv("MYSQL_USER")
        MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
        MYSQL_HOST = os.getenv("MYSQL_HOST")
        MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
        MYSQL_DATABASE = os.getenv("MYSQL_DATABASE")

        engine = create_engine(
            f"mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}"
        )
        print("Conectado ao MySQL!")
    else:
        # SQLite cria um arquivo local automaticamente se não existir
        engine = create_engine("sqlite:///banco_dados.db")
        print("Conectado ao SQLite!")

    # Garante que as tabelas existam no banco selecionado
    Base.metadata.create_all(engine)
    return engine

# Inicialização da primeira conexão
engine = conectar_banco()

while True:
    while True:

        print("\n \nEscolha uma opcao: \n")
        print("1- Empresa")
        print("2- Jogo")
        print("3- Alterar Banco de Dados (MySQL / SQLite)")
        print("0- Sair")
        opcao1 = int(input())
        if opcao1 == 0:
                print("Saindo do sistema...")
                break
        
        elif opcao1 == 3:
            engine = conectar_banco()
            continue
        elif opcao1 == 1 or opcao1 == 2:
            print("O que deseja fazer?")
            print("1- Inserir")
            print("2- Listar")
            print("3- Excluir")
            escolha = int(input())
            break

    with Session(engine) as session:
        if opcao1 == 1:
            if escolha == 1:
                nome_empresa = str(input("Digite o nome da empresa:\n")) 
                local_empresa = str(input("Digite o local da empresa:\n"))
                email_empresa = str(input("Digite o email da empresa:\n"))


                nome_empresa = Empresa(
                    nome = nome_empresa,
                    local = local_empresa,
                    email = email_empresa)
                session.add(nome_empresa)
                session.commit()

            elif escolha == 2:
                with Session(engine) as session:
                    empresas = session.scalars(select(Empresa)).all()

                    print("Lista de Empresas:")

                    for empresa in empresas:
                        print(f"ID: {empresa.id}")
                        print(f"Nome: {empresa.nome}")
                        print(f"Local: {empresa.local}")
                        print(f"Email: {empresa.email}")
                        print("-" * 30)

            elif escolha == 3:
                try:
                    with Session(engine) as session:
                        nome_excluir = input("Digite o nome da empresa a ser excluída:\n")
                        
                        empresa = session.scalars(
                            select(Empresa).where(Empresa.nome == nome_excluir)
                        ).first()

                        if empresa:
                            if empresa.jogos:  # (ou a lista de jogos relacionada)
                                print("Erro: Esta empresa possui jogos cadastrados e não pode ser excluída.")
                            else:
                                session.delete(empresa)
                                session.commit()
                                print("Empresa excluída com sucesso!")
                        else:
                            print("Empresa não encontrada.")

                except Exception as e:
                    print(f"Ocorreu um erro ao excluir: {e}")
                                
                                            

        if opcao1 == 2:
            if escolha == 1:
                nome_jogo = str(input("Digite o nome do jogo:\n")) 
                tempo_jogo = str(input("Digite o tempo de jogo:\n"))
                faixa_etaria  = str(input("Digite a faixa etaria do jogo:\n"))
                id_empresa  = str(input("Digite o id da empresa que criou o jogo:\n"))
            


                nome_jogo = Jogo(
                    nome = nome_jogo,
                    tempo_jogo = tempo_jogo,
                    faixa_etaria =  faixa_etaria,
                    empresa_id = id_empresa )
                session.add(nome_jogo)
                session.commit()
            elif escolha == 2:
                    with Session(engine) as session:
                        jogos = session.scalars(select(Jogo)).all()
            
                        print("Lista de Jogos:")
            
                        for jogo in jogos:
                            
                            print(f"ID: {jogo.id}")
                            print(f"Nome: {jogo.nome}")
                            print(f"Tempo de jogo: {jogo.tempo_jogo}")
                            print(f"Faixa etaria: {jogo.faixa_etaria}")
                            print(f"ID Empresa: {jogo.empresa_id}")
                            print("-" * 30)

            elif escolha == 3:
                    with Session(engine) as session:
            
                        nome_excluir_jogo = input("Digite o nome do jogo a ser excluído:\n")
                            
                        jogo = session.scalars(
                            select(Jogo).where(Jogo.nome == nome_excluir_jogo)
                            ).first()
            
                        if jogo:
                                session.delete(jogo)
                                session.commit()
                                print("Jogo excluído com sucesso!")
                        else:
                                print("Jogo não encontrado.")
                    
    if opcao1 == 0:
         break


