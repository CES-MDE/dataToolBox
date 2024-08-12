import pandas as pd

from utils.logger import duration_logging


@duration_logging
def prune_df(df: pd.DataFrame) -> None:
    df = df.copy()
    # Define columns where NaN or 0 values should be checked
    columns_to_check = [
        "surface_habitable",
        "Total_power",
    ]  # Add your specific column names here
    # Boolean mask to filter rows
    mask = (
        df[columns_to_check].notna().all(axis=1)
    )  # Filter out rows where any of the specified columns have NaN
    mask &= (df[columns_to_check] != 0).all(
        axis=1
    )  # Filter out rows where any of the specified columns are 0
    mask &= (
        df["surface_habitable"] >= 20
    )  # Si c'est inférieur, on fait l'hypothèse que ça ne nous interesse pas
    # Apply the mask to prune the DataFrame
    df = df[mask]
    return df


@duration_logging
def get_DPE_value(df: pd.DataFrame) -> None:
    df = df.copy()
    df["Consommation annuelle (en MWh/an)"] = df["Total_power"] / 1000
    df["Consommation par m² par an (en kWh/m².an)"] = (
        df["Total_power"] / df["surface_habitable"]
    ) / 1000
    return df


def get_tertiary_data(df: pd.DataFrame) -> None:
    # Define columns where NaN or 0 values should be checked
    df = df[(df["USAGE1"] != "Résidentiel") & (df["USAGE1"] != "Indifférencié")]
    return df


def remove_row_without_adress(df: pd.DataFrame) -> None:
    df = df.dropna(subset=["NOM_VOIE"])
    return df


def get_dle_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtre les données du DataFrame pour conserver les lignes où il y a consommation
    d'électricité, de gaz ou de réseaux, et calcule la consommation totale en MWh/an.

    Parameters:
    df (pd.DataFrame): Le DataFrame original contenant les données de consommation.

    Returns:
    pd.DataFrame: Un nouveau DataFrame avec les lignes filtrées et une colonne
                  additionnelle pour la consommation totale.
    """
    df = df.copy()
    # Filtrer les lignes où il y a consommation d'électricité, de gaz ou de réseaux
    df_filtered = df[
        (df["consommation_dle_elec"] != 0)
        | (df["consommation_dle_gaz"] != 0)
        | (df["consommation_dle_reseaux"] != 0)
    ]

    # Calculer la consommation totale en MWh/an
    df_filtered["Donnée mesurée (en MWh/an)"] = (
        df_filtered["consommation_dle_elec"]
        + df_filtered["consommation_dle_gaz"]
        + df_filtered["consommation_dle_reseaux"]
    )

    return df_filtered
