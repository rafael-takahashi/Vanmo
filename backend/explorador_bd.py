import sqlite3

if __name__ == "__main__":

    conexao = sqlite3.connect("app.db")

    cursor = conexao.cursor()

    print("USUARIO")

    resultados = cursor.execute("SELECT * FROM Usuario;").fetchall()
    
    for resultado in resultados:
        print(f"> {resultado}")

    print("CLIENTE")
    
    resultados = cursor.execute("SELECT * FROM Cliente;").fetchall()

    for resultado in resultados:
        print(f"> {resultado}")

    print("EMPRESA")
    
    resultados = cursor.execute("SELECT * FROM Empresa;").fetchall()

    for resultado in resultados:
        print(f"> {resultado}")

    print("ENDERECO")
    
    resultados = cursor.execute("SELECT * FROM Endereco;").fetchall()

    for resultado in resultados:
        print(f"> {resultado}")

    print("LOCAL")
    
    resultados = cursor.execute("SELECT * FROM Local;").fetchall()

    for resultado in resultados:
        print(f"> {resultado}")

    print("ALUGUEL")
    
    resultados = cursor.execute("SELECT * FROM Aluguel;").fetchall()

    for resultado in resultados:
        print(f"> {resultado}")

    print("CALENDARIO")
    
    resultados = cursor.execute("SELECT * FROM Calendario;").fetchall()

    for resultado in resultados:
        print(f"> {resultado}")

    print("VEICULO")
    
    resultados = cursor.execute("SELECT * FROM Veiculo;").fetchall()

    for resultado in resultados:
        print(f"> {resultado}")

    print("REGISTROS")
    
    resultados = cursor.execute("SELECT * FROM RegistrosLocacao;").fetchall()

    for resultado in resultados:
        print(f"> {resultado}")

    print("AVALIACOES")

    resultados = cursor.execute("SELECT * FROM Avaliacao;").fetchall()

    for resultado in resultados:
        print(f"> {resultado}")
