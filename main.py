import sys
import pandas as pd
import sistema

def exibir_infos_projeto():
    print(
        """
            ****************************************************************
            *                                                              *
            *                 Projeto Unificado - Fase 4                   *
            *           Persistência e Análise de Engajamento              *
            *                com Banco de Dados Relacional                 *
            *   Módulo Foco: DS-PY-004 (Bancos de Dados SQL e NoSQL)       *
            *                                                              *
            *   Turma: 1372                Professor: Flávio Crispin       *
            *   Data: 30/07/2025                                           *
            *                                                              *
            *   Alunos:                                                    *
            *     Edvaldo Oliveira                                         *
            *     Malu Fazendo                                             *
            *     Lucas Sandes                                             *
            *     Danilo Pinho                                             *
            *                                                              *
            *                 Equipe: Serpentes Tech                       *
            ****************************************************************
        """
    )

def exibir_menu():
    print(
        """
            ====== MENU DE ANÁLISE DE ENGAJAMENTO ======
            1. Criar conexão com o SGBD
            2. Criar banco e tabelas
            3. Carregar dados CSV -> Banco de Dados
            4. Top conteúdos mais consumidos
            5. Top conteúdos mais comentados
            6. Top plataformas com maior engajamento
            7. Sair
            ============================================
        """
    )

def main():
    exibir_infos_projeto()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
          print("Criar Conexão com o SGBD")
        
          sistema.create_connection()
        
        elif opcao == "2":
          print("Criar Banco de Dados e Tabelas")
        
          sistema.create_db()
        
        elif opcao == "3":
          print("Carregar dados CSV -> Banco de Dados ")
        
          path = input('Insira o nome do arquivo CSV: ')
        
          sistema.insert_data_csv(path)
        
        elif opcao == "4":
          print("\nTop Conteúdos Mais Consumidos: ")

          rank = int(input('Insira o tamanho do rank top que deseja visualizar: '))
          
          for id, cont, ttl in sistema.conteudos_mais_consumidos(rank):
              print(f'Id: {id} - Conteúdo: {cont} - Tempo total de consumo: {ttl}')
        
        elif opcao == "5":
          print("\nTop Conteúdos Mais Comentados: ")

          rank = int(input('Insira o tamanho do rank top que deseja visualizar: '))

          for id, cont, ttl in sistema.conteudos_mais_comentados(rank):
              print(f'Id: {id} - Conteúdo: {cont} - Total comentários: {ttl}')
        
        elif opcao == "6":
          print("\nTop Plataformas com Maior Engajamento: ")
        
          rank = int(input('Insira o tamanho do rank top que deseja visualizar: '))
        
          for id, plat, ttl in sistema.plataforma_maior_engajamento(rank):
            print(f'Id: {id} - Plataforma: {plat} - Total engajamento: {ttl}')
        
        elif opcao == "7":
            sistema.close_connection()
            
            print("\n           --- FIM ---\n")
            
            sys.exit(0)
        else:
            print("Opção inválida. Tente novamente.\n")

if __name__ == "__main__":
    main()