import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplcursors
from pathlib import Path

BASE_DIR = Path(__file__).parent


def select():
    dt = pd.read_csv(
        BASE_DIR / "select.csv",
        sep=";"
    )

    dt.columns = dt.columns.str.replace('"', '').str.strip()

    dt["DT_CRIA"] = pd.to_datetime(dt["DT_CRIA"])
    dt["ANO"] = pd.to_numeric(dt["ANO"])
    dt["MES"] = pd.to_numeric(dt["MES"])
    dt["TOTAL"] = pd.to_numeric(dt["TOTAL"])

    return dt


def select2():
    return pd.read_csv(
        BASE_DIR / "select2.csv",
        sep=";"
    )


def select3():
    return pd.read_csv(
        BASE_DIR / "select3.csv",
        sep=";"
    )


def view():

    dt = select()

    mensal = (
        dt.groupby(
            ["GER", "ANO", "MES"],
            as_index=False
        )["TOTAL"]
        .sum()
    )

    mensal["DATA"] = pd.to_datetime(
        mensal["ANO"].astype(str)
        + "-"
        + mensal["MES"].astype(int).astype(str).str.zfill(2)
        + "-01"
    )

    fig, ax = plt.subplots(figsize=(14, 5))

    cores = {
        "NORTE": "#78BE20",
        "OESTE": "#F2A900",
        "SUL": "#009CDE"
    }

    for ger in sorted(mensal["GER"].unique()):

        dados = (
            mensal[mensal["GER"] == ger]
            .sort_values("DATA")
        )

        cor = cores.get(ger, "#666666")

        ax.plot(
            dados["DATA"],
            dados["TOTAL"],
            color=cor,
            linewidth=2.5,
            marker="o",
            markersize=6,
            label=ger
        )

        for _, row in dados.iterrows():

            ax.text(
                row["DATA"],
                row["TOTAL"] + 0.3,
                str(int(row["TOTAL"])),
                fontsize=8,
                fontweight="bold",
                ha="center",
                color=cor
            )

    ax.set_title(
        "Evolução de Medidas Eliminadas por Região",
        fontsize=18,
        fontweight="bold"
    )

    ax.set_xlabel("Mês")
    ax.set_ylabel("Quantidade")

    ax.xaxis.set_major_locator(
        mdates.MonthLocator()
    )

    ax.xaxis.set_major_formatter(
        mdates.DateFormatter("%b/%y")
    )

    ax.legend()
    ax.grid(axis="y", linestyle="--", alpha=0.2)

    cursor = mplcursors.cursor(
        ax.lines,
        hover=True
    )

    @cursor.connect("add")
    def on_add(sel):

        linha = sel.artist

        ger = linha.get_label()

        data = pd.to_datetime(
            linha.get_xdata()[sel.index]
        )

        detalhe = dt[
            (dt["GER"] == ger)
            & (dt["MES"] == data.month)
            & (dt["ANO"] == data.year)
        ]

        total = detalhe["TOTAL"].sum()

        uteps = (
            detalhe.groupby("UTEP")["TOTAL"]
            .sum()
            .sort_values(ascending=False)
        )

        texto = "\n".join(
            f"{u}: {q}"
            for u, q in uteps.items()
        )

        sel.annotation.set_text(
            f"Região: {ger}\n"
            f"Período: {data.strftime('%m/%Y')}\n"
            f"Quantidade: {total}\n\n"
            f"{texto}"
        )

    plt.tight_layout()

    return fig


if __name__ == "__main__":
    fig = view()
    plt.show()