import main
from basemodels import *
import asyncio

async def executar_testes():
    print("Iniciando bateria de testes...\n")

    async def autenticar_usuario(email, senha):
        print("Autenticando usuário...")
        dados_login = UsuarioLogin(email=email, senha=senha)
        resposta = await main.login(dados=dados_login)
        print("Usuário autenticado com sucesso\n")
        return resposta["access_token"]

    async def cadastrar_dados_iniciais():
        print("Cadastrando dados iniciais...")

        # Cadastro de empresa
        empresa = CadastroEmpresa(
            email="empresa@teste.com",
            senha="senha123",
            nome_fantasia="Empresa Teste",
            telefone="123123123",
            cnpj="12345678000100",
            uf="PR",
            cidade="Ourizona",
            bairro="Centro",
            cep="87170000",
            rua="Meio do mato",
            numero="000"
        )

        await main.registrar_empresa(dados=empresa)

        # Cadastro de cliente
        cliente = CadastroCliente(
            email="cliente@teste.com",
            senha="senha123",
            nome_completo="Cliente Teste",
            cpf="12345678900",
            data_nascimento="2000-01-01",
            telefone="99987654"
        )

        await main.registrar_cliente(dados=cliente)

        # Cadastro de veículo
        veiculo = CadastrarVeiculo(
            nome_veiculo="Veículo Teste",
            placa_veiculo="ABC1234",
            custo_por_km=2.0,
            custo_base=200.0,
            cor="Preto",
            ano_fabricacao=2022,
            capacidade=5,
            foto=UploadFile(filename="veiculo.png", file=open("imagens/imagem_veiculo_padrao.png", "rb"))
        )
        token_empresa = await autenticar_usuario(empresa.email, empresa.senha)
        await main.cadastrar_veiculo(dados=veiculo, token=token_empresa)

        print("Dados iniciais cadastrados com sucesso\n")

    async def testar_apagar_usuario(token):
        print("Testando apagar_usuario...")
        await main.apagar_usuario(token=token)
        print("Apagar usuário executado com sucesso\n")

    async def testar_editar_dados_cliente(token):
        print("Testando editar_dados_cliente...")
        dados = AlterarDadosCliente(email="novoemail@teste.com", nome_completo="Nome Atualizado")
        await main.editar_dados_cliente(dados=dados, token=token)
        print("Editar dados do cliente executado com sucesso\n")

    async def testar_editar_dados_empresa(token):
        print("Testando editar_dados_empresa...")
        dados = AlterarDadosEmpresa(email="empresa@teste.com", nome_fantasia="Empresa Atualizada")
        await main.editar_dados_empresa(dados=dados, token=token)
        print("Editar dados da empresa executado com sucesso\n")

    async def testar_buscar_dados_cadastrais_cliente(token):
        print("Testando buscar_dados_cadastrais_cliente...")
        await main.buscar_dados_cadastrais_cliente(token=token)
        print("Buscar dados cadastrais do cliente executado com sucesso\n")

    async def testar_buscar_dados_cadastrais_empresa(token):
        print("Testando buscar_dados_cadastrais_empresa...")
        await main.buscar_dados_cadastrais_empresa(token=token)
        print("Buscar dados cadastrais da empresa executado com sucesso\n")

    async def testar_aceitar_ou_rejeitar_proposta(token):
        print("Testando aceitar_ou_rejeitar_proposta...")
        dados = DadosAcaoProposta(id_proposta=1, opcao=True)
        await main.aceitar_ou_rejeitar_proposta(dados=dados, token=token)
        print("Aceitar ou rejeitar proposta executado com sucesso\n")

    async def testar_buscar_todas_propostas_usuario(token):
        print("Testando buscar_todas_propostas_usuario...")
        await main.buscar_todas_propostas_usuario(token=token)
        print("Buscar todas propostas do usuário executado com sucesso\n")

    async def testar_buscar_dados_proposta(token):
        print("Testando buscar_dados_proposta...")
        dados = IdProposta(id_proposta=1)
        await main.buscar_dados_proposta(dados=dados, token=token)
        print("Buscar dados da proposta executado com sucesso\n")

    async def testar_criar_proposta(token):
        print("Testando criar_proposta...")
        dados = CriarProposta(
            id_empresa=1,
            id_veiculo=1,
            cidade_saida="Cidade A",
            cidade_chegada="Cidade B",
            distancia_extra_km=10.5,
            data_saida=datetime.date(2025, 1, 30),
            data_chegada=datetime.date(2025, 2, 5),
        )
        await main.criar_proposta(dados=dados, token=token)
        print("Criar proposta executado com sucesso\n")

    async def testar_cancelar_proposta(token):
        print("Testando cancelar_proposta...")
        dados = IdProposta(id_proposta=1)
        await main.cancelar_proposta(dados=dados, token=token)
        print("Cancelar proposta executado com sucesso\n")

    async def testar_verificar_custo_proposta(token):
        print("Testando verificar_custo_proposta...")
        dados = CriarProposta(
            id_empresa=1,
            id_veiculo=1,
            cidade_saida="Cidade A",
            cidade_chegada="Cidade B",
            distancia_extra_km=10.5,
            data_saida=datetime.date(2025, 1, 30),
            data_chegada=datetime.date(2025, 2, 5),
        )
        await main.verificar_custo_proposta(dados=dados, token=token)
        print("Verificar custo da proposta executado com sucesso\n")

    async def executar_todos_testes():
        await cadastrar_dados_iniciais()
        token_cliente = await autenticar_usuario(email="cliente@teste.com", senha="senha123")
        token_empresa = await autenticar_usuario(email="empresa@teste.com", senha="senha123")

        await testar_apagar_usuario(token_cliente)
        await testar_editar_dados_cliente(token_cliente)
        await testar_editar_dados_empresa(token_empresa)
        await testar_buscar_dados_cadastrais_cliente(token_cliente)
        await testar_buscar_dados_cadastrais_empresa(token_empresa)
        await testar_aceitar_ou_rejeitar_proposta(token_empresa)
        await testar_buscar_todas_propostas_usuario(token_cliente)
        await testar_buscar_dados_proposta(token_cliente)
        await testar_criar_proposta(token_empresa)
        await testar_cancelar_proposta(token_empresa)
        await testar_verificar_custo_proposta(token_empresa)

    await executar_todos_testes()
