import os
import pandas as pd
import geopandas as gpd
import logging
import time
import csv

try:
    from dataToolBox.pickelify import *
except:
    from pickelify import *
from tkinter import Tk, filedialog

# Configurer le niveau de journalisation global (DEBUG, INFO, WARNING, ERROR, CRITICAL)
logging.basicConfig(level=logging.INFO)
logging.getLogger("matplotlib").setLevel(logging.WARNING)


# Get Input and do stuff
def load_dataframe(file_path=None) -> pd.DataFrame | gpd.GeoDataFrame:
    """
    Interagit avec l'utilisateur pour extraire des données à partir d'un fichier pickle existant
    ou les lire depuis un fichier csv ou shp et les sauvegarder en format pickle.

    Returns:
    - pd.DataFrame: DataFrame extrait ou créé.
    """
    if file_path == None:
        root = Tk()
        root.withdraw()  # Hide the main window
        print("Sélectionnez le fichier à charger")
        file_path = filedialog.askopenfilename(title="Sélectionnez un fichier à lire")
        logging.info(f"File selected :{file_path}")
    file_format = detect_file_format(file_path)
    if file_format == "pkl":
        # Utilisation load_pickle sinon
        data = load_pkl_file(file_path)
    else:
        # Utilisation de la fonction Read&Saveçcsv si vous n'avez pas déjà un fichier pickle
        data = read(file_path)
        save_in_pkl(data)
    return data


# TODO : une class Read
def read(file_path: str) -> pd.DataFrame | gpd.GeoDataFrame:
    """
    Read a file and return its contents as either a pandas DataFrame or a geopandas GeoDataFrame.

    Parameters:
    file_path (str): The path to the file to be read.

    Returns:
    pd.DataFrame or gpd.GeoDataFrame: The loaded data.
    """
    file_format = detect_file_format(file_path)
    logging.debug(f"Detected file format: {file_format}")

    if file_format in ["csv", "xlsx", "xls"]:
        data = read_csv(file_path, file_format)
        logging.info(f"File {file_path} loaded as a DataFrame.")
    elif file_format in ["shp", "shx", "dbf", "gpkg"]:
        data = read_geofile(file_path)
        logging.info(f"File {file_path} loaded as a GeoDataFrame.")
    else:
        logging.error("Unsupported file format by SmartE")
        raise ValueError("Format de fichier non soutenu par SmartE")

    return data


def read_csv(file_path: str, file_format) -> pd.DataFrame:
    """
    Reads a CSV file into a Pandas DataFrame.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - pd.DataFrame: The DataFrame containing the CSV data.
    """
    # Lecture du fichier CSV
    logging.info("Start reading csv file")
    start = time.time()

    # Détection du séparateur
    if file_format == "csv":
        separator = detect_separator(file_path)
        data = pd.read_csv(file_path, sep=separator, encoding="latin1", dtype=str)
    else:
        data = pd.read_excel(file_path)

    elapsed_time = time.time() - start
    logging.info(f"File successfully read in {elapsed_time:.2f} sec")
    return data


def read_geofile(file_path: str) -> gpd.GeoDataFrame:
    """
    Reads a geospatial file (e.g., shapefile) into a GeoPandas GeoDataFrame.

    Parameters:
    - file_path (str): The path to the geospatial file.

    Returns:
    - gpd.GeoDataFrame: The GeoDataFrame containing the geospatial data.
    """
    # Lecture du fichier géospatial
    logging.info("Start reading geospatial file")
    start = time.time()

    # Lecture du fichier géospatial avec GeoPandas
    data = gpd.read_file(file_path)

    elapsed_time = time.time() - start
    logging.info(f"File successfully read in {elapsed_time:.2f} sec")
    return data


# TODO : une class Detect
def detect_file_format(file_path: str) -> str:
    """
    Detects the file format based on the file extension.

    Parameters:
    - file_path (str): The path to the file.

    Returns:
    - file_format (str): The detected file format (lowercase), or 'unknown' if not recognized.
    """

    _, file_extension = os.path.splitext(file_path)
    file_format = file_extension[
        1:
    ].lower()  # Exclude the dot (.) and convert to lowercase
    return file_format


def detect_separator(file_path: str) -> str:
    """
    Detects the delimiter used in a CSV file by analyzing its content.

    Parameters:
    - file_path (str): The path to the CSV file.

    Returns:
    - separator (str): The detected separator, or ',' (comma) if not recognized.
    """
    separators = [",", ";", "\t", "|"]  # Liste des séparateurs potentiels

    with open(file_path, "r", encoding="utf-8") as file:
        print(file)
        content = file.read(4096)  # Lire les premiers 4096 octets du fichier

        for separator in separators:
            try:
                # Utiliser Sniffer pour détecter automatiquement le séparateur
                dialect = csv.Sniffer().sniff(content, delimiters=separator)
                return dialect.delimiter  # Retourne le séparateur détecté
            except csv.Error:
                pass

    # Si toutes les tentatives échouent, utilisez la virgule par défaut
    return ";"  # Dernier bastion de l'humanité. Si les sniffer sont au fraise, il faut le faire à la main.
