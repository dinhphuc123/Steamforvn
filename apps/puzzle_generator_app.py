"""Streamlit app tạo phiếu mảnh ghép dạng sơ đồ tư duy toán học.

Chạy app:
    streamlit run apps/puzzle_generator_app.py
"""

from __future__ import annotations

from dataclasses import dataclass
from io import BytesIO
from textwrap import fill

import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
import streamlit as st


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


def draw_node(ax, center_x: float, center_y: float, width: float, height: float, node: Node) -> None:
    """Vẽ một ô thông tin bo góc."""
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

    ax.text(
        center_x,
        center_y + height * 0.16,
        node.title,
        ha="center",
        va="center",
        fontsize=11,
        weight="bold",
    )
    ax.text(
        center_x,
        center_y - 0.02,
        fill(node.content, 24),
        ha="center",
        va="center",
        fontsize=9,
    )


def draw_connector(ax, src: tuple[float, float], dst: tuple[float, float], label: str) -> None:
    """Vẽ đường nối có mũi tên và nhãn ở giữa."""
    ax.annotate(
        "",
        xy=dst,
        xytext=src,
        arrowprops={"arrowstyle": "-|>", "lw": 1.4, "color": "#808080"},
    )
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
    """Tạo figure sơ đồ mảnh ghép theo bố cục 8 ô xung quanh 1 ô trung tâm."""
    fig, ax = plt.subplots(figsize=(12, 8), dpi=150)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")

    positions = [
        (0.16, 0.78),  # top-left
        (0.5, 0.85),  # top
        (0.84, 0.78),  # top-right
        (0.88, 0.5),  # right
        (0.5, 0.14),  # bottom
        (0.16, 0.22),  # bottom-left
        (0.12, 0.5),  # left
        (0.5, 0.5),  # center
    ]

    center_pos = positions[-1]
    for node, pos in zip(nodes, positions):
        draw_node(ax, pos[0], pos[1], 0.24, 0.16, node)

    for idx, pos in enumerate(positions[:-1]):
        draw_connector(ax, center_pos, pos, labels[idx])

    ax.text(0.5, 0.96, title, ha="center", va="center", fontsize=16, weight="bold")
    fig.tight_layout()
    return fig


def main() -> None:
    st.set_page_config(page_title="Tạo mảnh ghép toán học", layout="wide")
    st.title("🧩 App tạo mảnh ghép bài tập toán")
    st.write(
        "Nhập nội dung cho 8 ô (7 ô xung quanh + 1 ô trung tâm), "
        "app sẽ tạo sơ đồ mảnh ghép tương tự mẫu bạn gửi."
    )

    title = st.text_input("Tiêu đề phiếu", "Hành trình giải đa thức")

    edited_nodes: list[Node] = []
    cols = st.columns(2)
    for i, default_node in enumerate(DEFAULT_NODES):
        with cols[i % 2].expander(f"Ô số {i + 1}: {default_node.title}", expanded=i < 2):
            edited_nodes.append(
                Node(
                    title=st.text_input(f"Tiêu đề ô {i + 1}", default_node.title, key=f"title_{i}"),
                    content=st.text_area(f"Nội dung ô {i + 1}", default_node.content, key=f"content_{i}"),
                    color=st.color_picker(f"Màu nền ô {i + 1}", default_node.color, key=f"color_{i}"),
                )
            )

    st.subheader("Nhãn đường nối")
    edited_labels: list[str] = []
    label_cols = st.columns(4)
    for i, label in enumerate(DEFAULT_LABELS):
        with label_cols[i % 4]:
            edited_labels.append(st.text_input(f"Nhãn {i + 1}", label, key=f"label_{i}"))

    fig = generate_figure(edited_nodes, edited_labels, title)
    st.pyplot(fig, use_container_width=True)

    buffer = BytesIO()
    fig.savefig(buffer, format="png", dpi=200, bbox_inches="tight")
    buffer.seek(0)

    st.download_button(
        label="⬇️ Tải ảnh PNG",
        data=buffer,
        file_name="manh_ghep_toan_hoc.png",
        mime="image/png",
    )


if __name__ == "__main__":
    main()
