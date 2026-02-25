# ZPL to PDF

Aplicativo simples em Python para converter arquivos de etiquetas em ZPL (como o arquivo `Envio-...-Etiquetas-de-produtos.txt`) em PDF, usando a API pública do Labelary.

## Como rodar o app (instruções detalhadas)

Se tiver dúvida ou não conseguir rodar, veja o guia passo a passo: **[COMO_RODAR.md](COMO_RODAR.md)**.

**Resumo:** abra o Terminal, vá até a pasta do projeto, instale as dependências e execute o app:

```bash
cd "/Users/tiagobasto/Library/CloudStorage/GoogleDrive-cha.usp@gmail.com/Meu Drive/BD/Apps/ZPL to PDF"
python3 -m pip install -r requirements.txt
python3 app.py
```

Depois acesse **http://127.0.0.1:5000/** no navegador. Para parar o servidor: **Ctrl+C**.

---

## Requisitos

- Python 3.9 ou superior
- Pip para instalar dependências

Instale as dependências:

```bash
pip install -r requirements.txt
```

---

## 1. Uso via linha de comando (já existente)

Supondo que o seu arquivo ZPL está em:

- `/Users/tiagobasto/Downloads/Envio-62280533-Etiquetas-de-produtos.txt`

E você quer gerar o PDF em:

- `/Users/tiagobasto/Downloads/etiquetas.pdf`

Execute:

```bash
python zpl_to_pdf.py \
  --input "/Users/tiagobasto/Downloads/Envio-62280533-Etiquetas-de-produtos.txt" \
  --output "/Users/tiagobasto/Downloads/etiquetas.pdf"
```

### Opções avançadas (CLI)

Você pode ajustar o tamanho da etiqueta e a resolução da impressora:

- `--width`: largura da etiqueta em polegadas (padrão: `4.0`)
- `--height`: altura da etiqueta em polegadas (padrão: `6.0`)
- `--dpmm`: pontos por milímetro (padrão: `8`, equivalente a ~203 dpi)

Exemplo para etiqueta de 4" x 3" em 300 dpi:

```bash
python zpl_to_pdf.py \
  --input "/caminho/para/arquivo.txt" \
  --output "/caminho/para/etiquetas.pdf" \
  --width 4 \
  --height 3 \
  --dpmm 12
```

---

## 2. Aplicação web com frontend

Agora o projeto também inclui uma pequena aplicação web em Flask com interface para:

- Enviar o arquivo ZPL (por exemplo, `Envio-...-Etiquetas-de-produtos.txt`);
- Definir largura/altura da etiqueta;
- Definir a resolução (dpmm);
- Informar o deslocamento da **segunda coluna** de etiquetas em centímetros;
- Baixar o PDF gerado.

### Executar o servidor web

No diretório do projeto (`ZPL to PDF`), rode:

```bash
python app.py
```

Por padrão o app sobe em `http://127.0.0.1:5000/`.

### Usando o frontend

No navegador:

1. Acesse `http://127.0.0.1:5000/`;
2. Faça upload do arquivo ZPL;
3. Ajuste, se quiser:
   - **Largura** e **Altura** em centímetros (cm);
   - **Resolução** em dpmm (8 ≈ 203 dpi, 12 ≈ 300 dpi);
   - **Deslocamento da 2ª coluna** em centímetros (cm):
     - Ex.: `-0,5` → move 0,5 cm para a **esquerda**;
     - Ex.: `+0,5` → move 0,5 cm para a **direita**.
4. Clique em **“Gerar PDF”** e o navegador fará o download do arquivo `etiquetas.pdf`.

### Como funciona o ajuste da 2ª coluna

- O backend converte o tamanho da etiqueta em pontos (dots), usando `width`, `height` e `dpmm`;
- Qualquer comando `^FOx,y` com `x` maior que metade da largura é considerado parte da **segunda coluna**;
- Apenas esses `x` da segunda coluna são ajustados com base no deslocamento informado em centímetros;
- Valor positivo desloca a coluna da direita para a direita; valor negativo, para a esquerda.

## Observações gerais

- A conversão é feita através da API pública do Labelary (`https://labelary.com`), então é necessário ter acesso à internet.
- Um único arquivo ZPL com várias etiquetas será convertido em um PDF com várias páginas (uma etiqueta por página).

