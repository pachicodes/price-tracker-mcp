# 🧺 Price Tracker MCP Server

Servidor MCP que permite ao Claude buscar **máquinas lava e seca** pelos menores preços.

## 🛒 Onde busca?

Busca em **4 grandes lojas brasileiras**:

- 🛍️ **Mercado Livre** - Maior marketplace da América Latina
- 🏬 **Magazine Luiza** - Grande rede varejista brasileira  
- 🏠 **Casas Bahia** - Tradicional loja de eletrodomésticos
- 📦 **Amazon Brasil** - Gigante mundial do e-commerce

Os resultados são combinados e ordenados por menor preço, independente da loja!

## 💡 O que é isso?

Este é um **servidor MCP (Model Context Protocol)** - uma extensão que dá ao Claude a capacidade de buscar preços de produtos em tempo real. Com ele instalado, você pode pedir ao Claude coisas como:

- *"Me mostre as máquinas lava e seca mais baratas"*
- *"Quais são as opções da Samsung de 11kg?"*
- *"Busque lava e seca da Brastemp até R$ 3000"*

## ✨ Recursos

- 🔍 Busca automática em 4 lojas brasileiras
- 💰 Ordenação por menor preço
- 🏷️ Filtros por marca e capacidade
- 🔗 Links diretos para compra
- ⚡ Resultados em tempo real
- 🏆 Compara preços entre lojas automaticamente

## 📋 Pré-requisitos

### 1. Python 3.10 ou superior

Verifique se você tem Python instalado:

```bash
python3 --version
```

Se não tiver, instale:

- **macOS**: `brew install python3` (requer [Homebrew](https://brew.sh/))
- **Windows**: Baixe em [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt install python3` (Ubuntu/Debian) ou `sudo dnf install python3` (Fedora)

### 2. Claude Desktop App

Baixe e instale o Claude Desktop:

- **Site oficial**: [claude.ai/download](https://claude.ai/download)
- Disponível para macOS e Windows
- Crie uma conta gratuita se ainda não tiver

### 3. Git (opcional, mas recomendado)

Para clonar o repositório facilmente:

- **macOS**: Já vem instalado ou `brew install git`
- **Windows**: Baixe em [git-scm.com](https://git-scm.com/)
- **Linux**: `sudo apt install git` ou `sudo dnf install git`

## 🚀 Instalação

### Passo 1: Clone ou baixe este repositório

```bash
cd /Users/SEU_USUARIO/Documents
git clone [url-do-repositorio]
cd price-tracker-mcp
```

### Passo 2: Instale as dependências

```bash
python3 -m pip install -e .
```

### Passo 3: Configure o Claude Desktop

O Claude Desktop precisa saber onde encontrar seu servidor MCP. Para isso, você vai editar (ou criar) um arquivo de configuração.

#### 3.1. Localize ou crie o arquivo de configuração

   **macOS:**
   
   O arquivo fica em: `~/Library/Application Support/Claude/claude_desktop_config.json`
   
   ```bash
   # Opção 1: Tentar abrir o arquivo (se já existir)
   open -a TextEdit ~/Library/Application\ Support/Claude/claude_desktop_config.json
   
   # Opção 2: Se o comando acima der erro, crie a pasta e o arquivo:
   mkdir -p ~/Library/Application\ Support/Claude
   touch ~/Library/Application\ Support/Claude/claude_desktop_config.json
   open -a TextEdit ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```
   
   **Windows:**
   
   O arquivo fica em: `%APPDATA%\Claude\claude_desktop_config.json`
   
   ```cmd
   # Opção 1: Tentar abrir o arquivo (se já existir)
   notepad %APPDATA%\Claude\claude_desktop_config.json
   
   # Opção 2: Se o comando acima der erro, crie a pasta e o arquivo:
   # Abra o PowerShell e execute:
   ```
   
   ```powershell
   New-Item -ItemType Directory -Force -Path "$env:APPDATA\Claude"
   New-Item -ItemType File -Path "$env:APPDATA\Claude\claude_desktop_config.json"
   notepad "$env:APPDATA\Claude\claude_desktop_config.json"
   ```
   
   **💡 Método alternativo (qualquer sistema):**
   
   1. Abra o Finder (macOS) ou Explorer (Windows)
   2. **macOS**: Pressione `Cmd + Shift + G` e cole: `~/Library/Application Support/Claude/`
   3. **Windows**: Cole na barra de endereços: `%APPDATA%\Claude`
   4. Se a pasta não existir, crie-a
   5. Crie um arquivo novo chamado `claude_desktop_config.json` (use um editor de texto)

#### 3.2. Edite o arquivo

   Copie e cole **exatamente** este conteúdo no arquivo:

```json
{
  "mcpServers": {
    "price-tracker": {
      "command": "python3",
      "args": [
        "-m",
        "price_tracker_mcp.server"
      ]
    }
  }
}
```

### Passo 4: Reinicie o Claude Desktop

**Reinicie o Claude Desktop completamente** (feche e abra novamente)

### Passo 5: Verifique se funcionou

Abra o Claude Desktop e pergunte:

> *"Você tem acesso à ferramenta de busca de máquinas lava e seca?"*

Se o Claude responder que sim, está tudo funcionando! 🎉

## 🎯 Como Usar

Agora você pode conversar naturalmente com o Claude:

**Exemplos de perguntas:**

```text
"Busque máquinas lava e seca"

"Me mostre as 5 máquinas lava e seca mais baratas"

"Quais são as opções da marca Electrolux?"

"Busque lava e seca LG com capacidade de 11kg"

"Me mostre máquinas Samsung de até 12kg"
```

O Claude vai usar a ferramenta automaticamente e te mostrar:

- Nome do produto
- Preço
- Link para compra
- Loja

## 🛠️ Ferramenta Disponível

### `search_washer_dryer`

Busca máquinas lava e seca pelos menores preços

**Parâmetros (todos opcionais):**

- `brand`: Marca específica (ex: "Brastemp", "Electrolux", "LG", "Samsung")
- `capacity`: Capacidade em kg (ex: "10kg", "11kg", "12kg")
- `max_results`: Quantidade de resultados (padrão: 15)

## 🧪 Testando Localmente

Se quiser testar o servidor antes de conectar ao Claude:

```bash
python3 -m price_tracker_mcp.server
```

O servidor vai iniciar e aguardar comandos via stdin/stdout.

## ❓ Solução de Problemas

### O Claude não vê a ferramenta

- Certifique-se de ter reiniciado o Claude Desktop completamente
- Verifique se o caminho do `python3` está correto no seu sistema
- Confirme que a instalação foi feita com sucesso

### Erros de instalação

```bash
# Tente criar um ambiente virtual primeiro
python3 -m venv venv
source venv/bin/activate  # No Windows: venv\Scripts\activate
pip install -e .
```

### O servidor não inicia

- Verifique sua versão do Python: `python3 --version` (precisa ser 3.10+)
- Reinstale as dependências: `pip install -r requirements.txt`

## 📝 Notas

- Os preços são buscados em tempo real em **4 lojas brasileiras**
- Busca simultânea: Mercado Livre + Magazine Luiza + Casas Bahia + Amazon
- A busca é feita por web scraping (não usa APIs oficiais)
- Os resultados são combinados e ordenados por menor preço
- Timeout de 10 segundos por loja
- Retorna até 15 produtos por padrão (configurável)
- Cada loja contribui com até 4 produtos para a busca

## 🤝 Contribuindo

Sinta-se livre para abrir issues ou pull requests para melhorias!

## 📄 Licença

MIT
