import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
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

    fig, ax = plt.subplots(figsize=(12, 5))

    cores = {
        "NORTE": "#78BE20",
        "OESTE": "#F2A900",
        "SUL": "#009CDE"
    }

    for ger in sorted(mensal["GER"].unique()):

        dados = (
            mensal[
                mensal["GER"] == ger
            ]
            .sort_values("DATA")
        )

        cor = cores.get(
            ger,
            "#666666"
        )

        ax.plot(
            dados["DATA"],
            dados["TOTAL"],
            marker="o",
            linewidth=2.5,
            color=cor,
            label=ger
        )

        ax.fill_between(
            dados["DATA"],
            dados["TOTAL"],
            0,
            color=cor,
            alpha=0.08
        )

        for _, row in dados.iterrows():

            ax.text(
                row["DATA"],
                row["TOTAL"] + 0.2,
                str(int(row["TOTAL"])),
                fontsize=8,
                ha="center",
                color=cor
            )

    ax.set_title(
        "Evolução de Medidas Eliminadas por Região",
        fontsize=16,
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

    ax.grid(
        axis="y",
        linestyle="--",
        alpha=0.3
    )

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    
    ax.margins(
        x=0.02,
        y=0.10
    )


    ax.legend()

    plt.xticks(rotation=45)
    plt.tight_layout()

    return fig
