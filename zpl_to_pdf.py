import argparse
from pathlib import Path
import io
import re

import requests
from pypdf import PdfWriter


LABELARY_BASE_URL = "http://api.labelary.com/v1/printers/{dpmm}dpmm/labels/{width}x{height}/"


def _format_dimension(value: float) -> str:
    """
    Formata largura/altura para o formato aceito pela API (ex.: 4, 6, 3.5).
    """
    if isinstance(value, float):
        text = f"{value}".rstrip("0").rstrip(".")
    else:
        text = str(value)
    return text or "1"


def _labelary_request(
    zpl_chunk: bytes,
    *,
    dpmm: int,
    width_in: float,
    height_in: float,
) -> bytes:
    """
    Envia um único bloco de ZPL para a API do Labelary e retorna um PDF.
    """
    width_str = _format_dimension(width_in)
    height_str = _format_dimension(height_in)

    url = LABELARY_BASE_URL.format(
        dpmm=dpmm,
        width=width_str,
        height=height_str,
    )

    headers = {
        "Accept": "application/pdf",
    }

    response = requests.post(url, headers=headers, data=zpl_chunk, timeout=30)

    if response.status_code != 200:
        raise RuntimeError(
            f"Falha ao converter ZPL em PDF (HTTP {response.status_code}): {response.text}"
        )

    return response.content


def _split_labels(zpl_text: str) -> list[str]:
    """
    Divide o conteúdo ZPL em uma lista de etiquetas individuais (^XA ... ^XZ).
    Cada elemento da lista é um bloco completo de etiqueta.
    """
    pattern = re.compile(r"(?mi)^\s*\^XA")
    matches = list(pattern.finditer(zpl_text))

    if not matches:
        return []

    labels: list[str] = []
    for idx, match in enumerate(matches):
        start = match.start()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(zpl_text)
        segment = zpl_text[start:end].strip()
        if segment:
            labels.append(segment)

    return labels


def convert_zpl_to_pdf(
    zpl_content: bytes,
    *,
    dpmm: int = 8,
    width_in: float = 4.0,
    height_in: float = 6.0,
) -> bytes:
    """
    Converte conteúdo ZPL em PDF usando a API pública do Labelary.

    - dpmm: pontos por milímetro (8 ≈ 203 dpi, 12 ≈ 300 dpi)
    - width_in / height_in: tamanho da etiqueta em polegadas

    Se o arquivo tiver mais do que 50 etiquetas (^XA...^XZ), divide em lotes
    de até 50 etiquetas, converte cada lote separadamente e junta todos os
    PDFs em um único arquivo.
    """
    # tenta dividir o ZPL em etiquetas individuais
    zpl_text = zpl_content.decode("utf-8", errors="ignore")
    labels = _split_labels(zpl_text)

    # se não conseguiu detectar etiquetas, ou está abaixo do limite, envia tudo de uma vez
    if not labels or len(labels) <= 50:
        return _labelary_request(
            zpl_chunk=zpl_content,
            dpmm=dpmm,
            width_in=width_in,
            height_in=height_in,
        )

    # acima de 50 etiquetas: processa em lotes e une os PDFs
    writer = PdfWriter()

    for start in range(0, len(labels), 50):
        batch = labels[start : start + 50]
        batch_text = "\n".join(batch) + "\n"
        batch_bytes = batch_text.encode("utf-8")

        pdf_chunk = _labelary_request(
            zpl_chunk=batch_bytes,
            dpmm=dpmm,
            width_in=width_in,
            height_in=height_in,
        )

        writer.append(io.BytesIO(pdf_chunk))

    output = io.BytesIO()
    writer.write(output)
    writer.close()

    return output.getvalue()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Converte um arquivo de etiquetas ZPL (texto) em PDF, "
            "usando a API pública do Labelary."
        )
    )

    parser.add_argument(
        "--input",
        "-i",
        required=True,
        type=Path,
        help="Caminho do arquivo de entrada com comandos ZPL (por exemplo, .txt).",
    )
    parser.add_argument(
        "--output",
        "-o",
        required=True,
        type=Path,
        help="Caminho do arquivo PDF de saída.",
    )
    parser.add_argument(
        "--dpmm",
        type=int,
        default=8,
        help="Resolução da impressora em pontos por milímetro (padrão: 8 ≈ 203 dpi).",
    )
    parser.add_argument(
        "--width",
        type=float,
        default=4.0,
        help="Largura da etiqueta em polegadas (padrão: 4.0).",
    )
    parser.add_argument(
        "--height",
        type=float,
        default=6.0,
        help="Altura da etiqueta em polegadas (padrão: 6.0).",
    )

    return parser.parse_args()


def main() -> None:
    args = parse_args()

    if not args.input.is_file():
        raise SystemExit(f"Arquivo de entrada não encontrado: {args.input}")

    zpl_content = args.input.read_bytes()

    try:
        pdf_bytes = convert_zpl_to_pdf(
            zpl_content,
            dpmm=args.dpmm,
            width_in=args.width,
            height_in=args.height,
        )
    except Exception as exc:
        raise SystemExit(f"Erro na conversão: {exc}") from exc

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(pdf_bytes)

    print(f"PDF gerado com sucesso em: {args.output}")


if __name__ == "__main__":
    main()

