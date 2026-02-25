# Como rodar o app ZPL to PDF — passo a passo

Siga um dos métodos abaixo. O **Método 1** é o mais simples (usando o script). O **Método 2** é manual, comando por comando.

---

## Método 1: Usar o script (recomendado)

1. **Abra o Terminal**
   - No Mac: `Cmd + Espaço`, digite **Terminal** e pressione Enter.
   - Ou: Aplicativos → Utilitários → Terminal.

2. **Vá até a pasta do projeto**  
   Cole e execute (a pasta tem espaço no nome, por isso está entre aspas):

   ```bash
   cd "/Users/tiagobasto/Library/CloudStorage/GoogleDrive-cha.usp@gmail.com/Meu Drive/BD/Apps/ZPL to PDF"
   ```

3. **Primeira vez: crie o ambiente virtual e instale as dependências**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

   Depois disso, você pode usar o script `run.sh` (ele ativa o `venv` automaticamente se existir).

4. **Dê permissão ao script e execute**

   ```bash
   chmod +x run.sh
   ./run.sh
   ```

   (Se ainda não criou o `venv`, o script tentará instalar as dependências com `pip`; se der erro de permissão, use o passo 3 acima.)

5. **Abra o navegador**  
   Acesse: **http://127.0.0.1:5000/**

6. **Para parar o servidor**  
   No Terminal, pressione **Ctrl+C**.

---

## Método 2: Comandos manuais (com ambiente virtual — recomendado)

Usar um **ambiente virtual** evita conflitos e erros de permissão ao instalar pacotes.

1. **Abra o Terminal** (como no passo 1 acima).

2. **Vá até a pasta do projeto**

   ```bash
   cd "/Users/tiagobasto/Library/CloudStorage/GoogleDrive-cha.usp@gmail.com/Meu Drive/BD/Apps/ZPL to PDF"
   ```

3. **Verifique se o Python está instalado**

   ```bash
   python3 --version
   ```

   Se aparecer algo como `Python 3.9.x` ou maior, está ok.  
   Se der "comando não encontrado", instale o Python em: https://www.python.org/downloads/

4. **Crie e ative um ambiente virtual**

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

   Depois disso, o prompt deve mostrar algo como `(venv)` no início. Tudo que você instalar ficará só dentro desta pasta.

5. **Instale as dependências**

   ```bash
   pip install -r requirements.txt
   ```

6. **Execute o app**

   ```bash
   python app.py
   ```

7. **Abra no navegador**  
   Acesse: **http://127.0.0.1:5000/**

8. **Para parar**  
   No Terminal: **Ctrl+C**.

   **Para sair do ambiente virtual** (quando terminar): digite `deactivate`.

---

## Método 2b: Sem ambiente virtual

Se preferir não usar venv:

1. Vá até a pasta do projeto (como no Método 2, passo 2).
2. Instale as dependências:
   ```bash
   python3 -m pip install --user -r requirements.txt
   ```
   O `--user` instala na sua pasta de usuário, evitando precisar de permissão de administrador.
3. Execute:
   ```bash
   python3 app.py
   ```
4. Abra **http://127.0.0.1:5000/** no navegador.

---

## Se algo der errado

### "python: command not found" ou "python3: command not found"
- Instale o Python 3 em https://www.python.org/downloads/
- No Mac, você também pode instalar pelo Homebrew: `brew install python3`

### "No module named 'flask'" ou "No module named 'requests'"
- Certifique-se de ter executado o passo de instalar dependências na **mesma** pasta do projeto:
  ```bash
  cd "/Users/tiagobasto/Library/CloudStorage/GoogleDrive-cha.usp@gmail.com/Meu Drive/BD/Apps/ZPL to PDF"
  python3 -m pip install -r requirements.txt
  ```

### "Address already in use" (porta 5000 em uso)
- Outro programa está usando a porta 5000. Feche o outro app ou rode em outra porta:
  ```bash
  python3 app.py
  ```
  E no final do arquivo `app.py`, altere temporariamente para: `app.run(debug=True, port=5001)`  
  Depois acesse: http://127.0.0.1:5001/

### Pasta com acento ou nome diferente
- Se a pasta "Meu Drive" tiver outro nome (ex.: "My Drive"), use o caminho que aparece quando você abre a pasta no Finder e arrasta ela para o Terminal (ele cola o caminho correto).

---

## Resumo rápido

**Primeira vez** (criar ambiente e instalar):

```bash
cd "/Users/tiagobasto/Library/CloudStorage/GoogleDrive-cha.usp@gmail.com/Meu Drive/BD/Apps/ZPL to PDF"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

**Nas próximas vezes** (só rodar):

```bash
cd "/Users/tiagobasto/Library/CloudStorage/GoogleDrive-cha.usp@gmail.com/Meu Drive/BD/Apps/ZPL to PDF"
source venv/bin/activate
python app.py
```

Depois abra **http://127.0.0.1:5000/** no navegador.
