# API de Gestão de Estoque — Almoxarifado

API REST desenvolvida em Python com FastAPI e PostgreSQL para controle de **material de consumo** em almoxarifados, modelada a partir de rotinas reais de controle de estoque, requisições por setor e auditoria de movimentações.

## Regras de Negócio (Escopo V1)

- **Foco em material de consumo:** itens que entram por reposição/compra e saem definitivamente mediante entrega (escritório, elétrica, alvenaria, hidráulica, higiene).
- **Prevenção de duplicidade e auditoria (Soft Delete):** cada material possui um código único (SKU) padronizado. Materiais já movimentados não são apagados fisicamente (`DELETE`), mas inativados (`ativo = False`) para preservar o histórico contábil.
- **Fluxo de solicitações com aprovação parcial:** setores registram pedidos especificando a `quantidade_solicitada`. O administrador pode aprovar total ou parcialmente (`quantidade_aprovada`), seguindo os estados:
  `PENDENTE` → `APROVADA` / `REJEITADA` → `ENTREGUE`.
- **Movimentação como extrato imutável:** toda entrada, saída ou ajuste gera um registro permanente com data, quantidade e responsável. O saldo nunca pode ficar negativo (controle garantido por transação no banco).
- **Fora de escopo na V1:** cautela/empréstimo de ferramentas, controle financeiro/preço médio, notas fiscais e gestão de fornecedores.

## Stack Técnica

- **Linguagem:** Python 3.10+
- **Framework Web:** FastAPI + Pydantic (validação de dados e documentação Swagger)
- **Banco de Dados:** PostgreSQL (SQL puro com foco em integridade, `JOIN`s e transações)
- **Qualidade e Versionamento:** Pytest, Git, GitHub Actions

## Arquitetura em Camadas

```text
app/
├── routers/       # Rotas HTTP (recebe requisição, devolve resposta e status code)
├── schemas/       # Contratos de entrada/saída e validações (Pydantic / Regex)
├── services/      # Regras de negócio do almoxarifado
├── repositories/  # Consultas SQL e controle de transações no PostgreSQL
└── main.py        # Ponto de entrada da aplicação FastAPI
```

## Roadmap (Desenvolvimento Incremental)

### Incremento 1 — Núcleo do Estoque
- [ ] Configuração do ambiente (PostgreSQL, `.env`, estrutura de camadas)
- [ ] Modelagem e criação das tabelas `categorias`, `materiais` e `movimentacoes`
- [ ] CRUD de categorias e materiais (SKU único + Soft Delete)
- [ ] Registro de `ENTRADA` e `SAIDA` com transação e bloqueio contra saldo negativo

### Incremento 2 — Fluxo de Solicitações por Setor
- [ ] Criação das tabelas `secoes`, `solicitacoes` e `itens_solicitacao`
- [ ] Abertura de pedidos com múltiplos itens por seção
- [ ] Aprovação total/parcial e rejeição de solicitações
- [ ] Confirmação de entrega com baixa automática de estoque e registro no histórico

### Incremento 3 — Segurança, Testes e Automação
- [ ] Cadastro de `usuarios` com perfis (`SOLICITANTE`, `ADMIN`, `ALMOXARIFE`) e senha com hash
- [ ] Autenticação e bloqueio de permissões por perfil
- [ ] Relatório SQL de consumo por seção e período
- [ ] Testes automatizados das regras críticas (Pytest) e pipeline no GitHub Actions

## Como Executar Localmente

> Em construção — instruções serão adicionadas ao final do Incremento 1.

# OBSERVAÇÕES
  - Adicionar uma função na criação de lotes para editar as informações que foram recusadas, após a verificação de dados repetidos dentro do próprio lote e da verificação de o dado existe dentro do banco de dados.


