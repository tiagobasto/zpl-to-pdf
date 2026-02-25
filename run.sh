#!/bin/bash
# Script para rodar o app ZPL to PDF (macOS / Linux)

# Pasta onde está este script (e o app)
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$DIR"

echo "Pasta do projeto: $DIR"
echo ""

# Usar python3 se existir, senão python
if command -v python3 &>/dev/null; then
    PY=python3
elif command -v python &>/dev/null; then
    PY=python
else
    echo "Erro: Python não encontrado. Instale Python 3 em https://www.python.org"
    exit 1
fi

# Se existir ambiente virtual, usar
if [ -d "venv" ] && [ -f "venv/bin/activate" ]; then
    echo "Ativando ambiente virtual (venv)..."
    source venv/bin/activate
    PY=python
fi

echo "Usando: $PY"
$PY --version
echo ""

# Instalar dependências se faltar algo
echo "Verificando dependências..."
$PY -c "import flask, requests" 2>/dev/null || {
    echo "Instalando dependências (pip install -r requirements.txt)..."
    $PY -m pip install -r requirements.txt
}
echo ""

echo "Iniciando o servidor em http://127.0.0.1:5000/"
echo "Abra esse endereço no navegador. Para parar: Ctrl+C"
echo ""

$PY app.py
