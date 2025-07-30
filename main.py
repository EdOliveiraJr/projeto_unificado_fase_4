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
            *                 Equipe: Serpentes Tech 🐍🧑🏽‍💻                 *
            ****************************************************************
        """
    )

def exibir_menu():
    print(
        """
            ====== 📊 MENU DE ANÁLISE DE ENGAJAMENTO ======
            1. 🔌↕️ Criar conexão com o SGBD
            2. 🏦🎲 Criar banco e tabelas
            3. 📃⚡ Carregar dados CSV -> Banco de Dados
            4. 🔝👀 Top conteúdos mais consumidos
            5. 🔝💬 Top conteúdos mais comentados
            6. 🔝👍🏽 Top plataformas com maior engajamento
            7. 🚪🏃🏽‍➡️ Sair
            ============================================
        """
    )

def main():
    exibir_infos_projeto()

    while True:
        exibir_menu()
        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
          print("\n*** Criar Conexão com o SGBD 🔌↕️ ***\n")
        
          sistema.create_connection()
        
        elif opcao == "2":
          print("\n*** Criar Banco de Dados e Tabelas 🏦🎲 *** \n")
        
          sistema.create_db()
        
        elif opcao == "3":
          print("\n*** Carregar dados CSV -> Banco de Dados 📃⚡ ***\n")
        
          path = input('Insira o nome do arquivo CSV: ')
        
          sistema.insert_data_csv(path)
        
        elif opcao == "4":
          print("\n*** Top Conteúdos Mais Consumidos: 🔝👀 ***\n")

          try:             
            rank = int(input('Insira o tamanho do rank top que deseja visualizar: '))
            print()
            for id, cont, ttl in sistema.conteudos_mais_consumidos(rank):
                print(f' Id: {id:02} - Conteúdo: {cont[:25]:<30} -  Tempo total de consumo: {sistema.converter_segundos_para_horas(ttl)} ⏳👀')
          except:
            print('\nEntrada inválida. Insira um número. ❌\n')
        
        elif opcao == "5":
          print("\n*** Top Conteúdos Mais Comentados 🔝💬 ***\n")

          try:
            rank = int(input('Insira o tamanho do rank top que deseja visualizar: '))
            print()

            for id, cont, ttl in sistema.conteudos_mais_comentados(rank):
                print(f'Id: {id:02} - Conteúdo: {cont[:25]:<30} - Total comentários: {ttl:02} 🗣️💬')
          except:  
            print('\nEntrada inválida. Insira um número. ❌\n')

        
        elif opcao == "6":
          print("\n*** Top Plataformas com Maior Engajamento 🔝👍🏽 ***\n")
        
          try:
            rank = int(input('Insira o tamanho do rank top que deseja visualizar: '))
            print()
            for id, plat, ttl in sistema.plataforma_maior_engajamento(rank):
              print(f'Id: {id:02} - Plataforma: {plat[:25]:<30} - Total engajamento: {ttl:02} ❤️👍🏽')
          except:  
            print('\nEntrada inválida. Insira um número. ❌\n')

        
        elif opcao == "7":
            print()
            sistema.close_connection()
            
            print("\n           --- FIM ---\n")
            
            sys.exit(0)
        else:
            print("\n Opção inválida. Tente novamente. ❌\n")

if __name__ == "__main__":
    main()