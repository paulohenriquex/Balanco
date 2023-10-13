import mysql.connector
import getpass

# Nome do banco de dados
database = 'balanco'

try:
    # Conectar ao MySQL
    connection = mysql.connector.connect(
        host='localhost',
        port='3306',
        user='root',  # Substitua pelo seu nome de usuário.
        password=getpass.getpass("Digite a sua senha: ")
    )

    # Criar um cursor para executar consultas SQL
    cursor = connection.cursor()

    # Criar o banco de dados (se não existir)
    create_database_query = f"CREATE DATABASE IF NOT EXISTS {database}"
    cursor.execute(create_database_query)

    # Usar o banco de dados
    cursor.execute(f"USE {database}")

    # Criar a tabela (se não existir)
    create_table_query = f"""
    CREATE TABLE IF NOT EXISTS {database} (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255),
        valor DECIMAL(10,2)
    )
    """
    cursor.execute(create_table_query)

    def menu(cursor):
        while True:
            print("1 - Cadastrar")
            print("2 - Mostrar")
            print("3 - Sair")
            opção = int(input())
            if opção == 1:
                cadValores(cursor)
            elif opção == 2:
                mostrar(cursor)
            elif opção == 3:
                break

    def cadValores(cursor):
        nome = input("Digite o nome do produto: ")
        valor = input("Digite o valor do produto: ")

        try:
            valor = float(valor)
        except ValueError:
            print("Valor inválido. Digite um valor válido.")
            return

        # Inserir o produto na tabela
        insert_query = f"INSERT INTO {database}(nome, valor) VALUES (%s, %s)"
        cursor.execute(insert_query, (nome, valor))
        connection.commit()
        print("Produto cadastrado com sucesso!")

    def mostrar(cursor):
        # Selecionar e mostrar todos os produtos da tabela
        cursor.execute(f"SELECT nome, valor FROM {database}")
        produtos = cursor.fetchall()
        if not produtos:
            print("Nenhum produto cadastrado.")
        else:
            for produto in produtos:
                print("Nome:", produto[0])
                print("Valor:", produto[1])

    # Chamar a função do menu
    menu(cursor)

except mysql.connector.Error as e:
    print(f"Erro de conexão com o MySQL: {e}")
finally:
    # Fechar o cursor e a conexão, independentemente de ocorrer uma exceção
    cursor.close()
    connection.close()
