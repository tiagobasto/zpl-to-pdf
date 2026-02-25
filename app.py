import io
import re
from pathlib import Path
from typing import Optional

from flask import (
    Flask,
    render_template,
    request,
    send_file,
    redirect,
    url_for,
    flash,
)

from zpl_to_pdf import convert_zpl_to_pdf


app = Flask(__name__)
app.secret_key = "change-this-secret-key"


def _decode_zpl(content: bytes) -> str:
    """
    Tenta decodificar o ZPL de forma robusta.
    ^CI28 indica normalmente UTF-8.
    """
    try:
        return content.decode("utf-8")
    except UnicodeDecodeError:
        return content.decode("latin-1", errors="ignore")


def _encode_zpl(content: str) -> bytes:
    return content.encode("utf-8")


def adjust_second_column(
    zpl_text: str,
    *,
    dpmm: int,
    width_in: float,
    offset_cm: float,
) -> str:
    """
    Ajusta a posição X da segunda coluna de etiquetas.

    - offset_cm > 0: move para a direita
    - offset_cm < 0: move para a esquerda

    A detecção da segunda coluna é baseada na largura da etiqueta:
    qualquer ^FO com X maior que metade da largura é considerado
    pertencente à segunda coluna.
    """
    if offset_cm == 0:
        return zpl_text

    # largura total em dots
    label_width_mm = width_in * 25.4
    label_width_dots = dpmm * label_width_mm
    mid_x = label_width_dots / 2.0

    # deslocamento em dots (1 cm = 10 mm)
    delta_mm = offset_cm * 10.0
    delta_dots = int(round(dpmm * delta_mm))

    fo_pattern = re.compile(r"(\^FO)(-?\d+),(-?\d+)")

    def _replace(match: re.Match) -> str:
        prefix, x_str, y_str = match.groups()
        x = int(x_str)
        y = int(y_str)

        # só altera a "segunda coluna" (x depois da metade da largura)
        if x > mid_x:
            x = x + delta_dots

        return f"{prefix}{x},{y}"

    return fo_pattern.sub(_replace, zpl_text)


def parse_offset_cm(raw: Optional[str]) -> float:
    if not raw:
        return 0.0
    raw = raw.strip()
    if not raw:
        return 0.0
    # aceita vírgula como separador decimal
    raw = raw.replace(",", ".")
    try:
        return float(raw)
    except ValueError:
        return 0.0


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template(
            "index.html",
            default_width="10",
            default_height="15",
            default_dpmm="8",
            default_offset="0",
        )

    # POST
    file = request.files.get("zpl_file")
    if not file or file.filename == "":
        flash("Selecione um arquivo ZPL.", "error")
        return redirect(url_for("index"))

    try:
        width_cm = float(request.form.get("width_cm", "10").replace(",", "."))
        height_cm = float(request.form.get("height_cm", "15").replace(",", "."))
        dpmm = int(request.form.get("dpmm", "8"))
    except ValueError:
        flash("Parâmetros de tamanho ou resolução inválidos.", "error")
        return redirect(url_for("index"))

    # Converte cm para polegadas (API Labelary usa polegadas)
    width_in = width_cm / 2.54
    height_in = height_cm / 2.54

    offset_cm = parse_offset_cm(request.form.get("offset_cm", "0"))

    raw_bytes = file.read()
    zpl_text = _decode_zpl(raw_bytes)

    adjusted_zpl = adjust_second_column(
        zpl_text,
        dpmm=dpmm,
        width_in=width_in,
        offset_cm=offset_cm,
    )

    zpl_bytes = _encode_zpl(adjusted_zpl)

    try:
        pdf_bytes = convert_zpl_to_pdf(
            zpl_bytes,
            dpmm=dpmm,
            width_in=width_in,
            height_in=height_in,
        )
    except Exception as exc:
        flash(f"Erro ao converter ZPL em PDF: {exc}", "error")
        return redirect(url_for("index"))

    return send_file(
        io.BytesIO(pdf_bytes),
        mimetype="application/pdf",
        as_attachment=True,
        download_name="etiquetas.pdf",
    )


if __name__ == "__main__":
    # Executa em modo desenvolvimento
    app.run(debug=True)

