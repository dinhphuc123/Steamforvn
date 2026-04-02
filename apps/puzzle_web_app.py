"""Flask web app tạo phiếu mảnh ghép toán học.

Chạy app:
    python apps/puzzle_web_app.py
Sau đó mở trình duyệt tại: http://127.0.0.1:5000
"""

from __future__ import annotations

import base64
from dataclasses import dataclass
from io import BytesIO
from textwrap import fill

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from flask import Flask, render_template, request, send_file


@dataclass
class Node:
    title: str
    content: str
    color: str


DEFAULT_NODES = [
    Node("START", "Thu gọn đa thức\nA(x)=3x²+2x-5", "#F7E8E8"),
    Node("Bậc 5", "Xác định bậc\ncủa đa thức", "#EFE8F6"),
    Node("Nghiệm", "Đa thức\nM(x)=-3x+6", "#FFF4B8"),
    Node("Tìm nghiệm", "m(x)=x²-5x+6", "#FFE4CC"),
    Node("Giá trị", "Cho đa thức\nB(x)=x³-2x²+1", "#FFF0C8"),
    Node("Trị đa thức", "D(x)=x²-4x+4", "#E3F2FF"),
    Node("Hệ số cao nhất", "5x⁴+6x²+x⁷-5x+7", "#F7DFF2"),
    Node("Cộng đa thức", "P(x)=2x²+3x+5\nQ(x)=x²-2x+4", "#DFF2FF"),
]

DEFAULT_LABELS = ["2x²-3x", "C(x)=x⁵+3x²+1", "x=2", "7", "x+1", "6", "5", "8x-4"]
DEFAULT_TITLE = "Hành trình giải đa thức"

app = Flask(__name__)


def draw_node(ax, center_x: float, center_y: float, width: float, height: float, node: Node) -> None:
    x = center_x - width / 2
    y = center_y - height / 2

    rect = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.02,rounding_size=0.03",
        linewidth=2,
        edgecolor="#8A8A8A",
        facecolor=node.color,
    )
    ax.add_patch(rect)

    ax.text(center_x, center_y + height * 0.16, node.title, ha="center", va="center", fontsize=11, weight="bold")
    ax.text(center_x, center_y - 0.02, fill(node.content, 24), ha="center", va="center", fontsize=9)


def draw_connector(ax, src: tuple[float, float], dst: tuple[float, float], label: str) -> None:
    ax.annotate("", xy=dst, xytext=src, arrowprops={"arrowstyle": "-|>", "lw": 1.4, "color": "#808080"})

    mid_x = (src[0] + dst[0]) / 2
    mid_y = (src[1] + dst[1]) / 2

    rect = FancyBboxPatch(
        (mid_x - 0.09, mid_y - 0.025),
        0.18,
        0.05,
        boxstyle="round,pad=0.01,rounding_size=0.02",
        linewidth=1,
        edgecolor="#B8B8B8",
        facecolor="white",
        alpha=0.95,
    )
    ax.add_patch(rect)
    ax.text(mid_x, mid_y, fill(label, 20), fontsize=8, ha="center", va="center")


def generate_figure(nodes: list[Node], labels: list[str], title: str):
    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    positions = [
        (0.16, 0.78),
        (0.5, 0.85),
        (0.84, 0.78),
        (0.88, 0.5),
        (0.5, 0.14),
        (0.16, 0.22),
        (0.12, 0.5),
        (0.5, 0.5),
    ]

    center_pos = positions[-1]
    for node, pos in zip(nodes, positions):
        draw_node(ax, pos[0], pos[1], 0.24, 0.16, node)

    for idx, pos in enumerate(positions[:-1]):
        draw_connector(ax, center_pos, pos, labels[idx])

    ax.text(0.5, 0.96, title, ha="center", va="center", fontsize=16, weight="bold")
    fig.tight_layout()
    return fig


def get_payload_from_form(form) -> tuple[str, list[Node], list[str]]:
    title = form.get("sheet_title", DEFAULT_TITLE)
    nodes: list[Node] = []
    labels: list[str] = []

    for i, default_node in enumerate(DEFAULT_NODES):
        nodes.append(
            Node(
                title=form.get(f"title_{i}", default_node.title),
                content=form.get(f"content_{i}", default_node.content),
                color=form.get(f"color_{i}", default_node.color),
            )
        )

    for i, default_label in enumerate(DEFAULT_LABELS):
        labels.append(form.get(f"label_{i}", default_label))

    return title, nodes, labels


def fig_to_base64(fig) -> str:
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=200, bbox_inches="tight")
    buffer.seek(0)
    encoded = base64.b64encode(buffer.read()).decode("utf-8")
    plt.close(fig)
    return encoded


@app.get("/")
def index():
    fig = generate_figure(DEFAULT_NODES, DEFAULT_LABELS, DEFAULT_TITLE)
    image_data = fig_to_base64(fig)
    return render_template(
        "puzzle_form.html",
        default_title=DEFAULT_TITLE,
        nodes=DEFAULT_NODES,
        labels=DEFAULT_LABELS,
        image_data=image_data,
    )


@app.post("/")
def preview():
    title, nodes, labels = get_payload_from_form(request.form)
    fig = generate_figure(nodes, labels, title)
    image_data = fig_to_base64(fig)
    return render_template(
        "puzzle_form.html",
        default_title=title,
        nodes=nodes,
        labels=labels,
        image_data=image_data,
    )


@app.post("/download")
def download_png():
    title, nodes, labels = get_payload_from_form(request.form)
    fig = generate_figure(nodes, labels, title)
    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=250, bbox_inches="tight")
    plt.close(fig)
    buffer.seek(0)
    return send_file(buffer, mimetype="image/png", as_attachment=True, download_name="manh_ghep_toan_hoc.png")


if __name__ == "__main__":
    app.run(debug=True)
