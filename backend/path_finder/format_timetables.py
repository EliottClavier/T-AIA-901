import os
import pandas as pd
import unicodedata


class FormatTimetables:

    TIME_TABLE_PATH = os.path.join(os.path.dirname(__file__), "data/timetables.csv")
    TIME_TABLE_FORMATTED_PATH = os.path.join(os.path.dirname(__file__), "data/timetables_formatted.csv")
    TRAIN_STATIONS_PATH = os.path.join(os.path.dirname(__file__), "data/train_stations.csv")

    df = []

    SPECIAL_CASES = {
        "La-Rochelle-Pt-Dauphine": "La-Rochelle-Porte-Dauphine",
        "St-Gervais-L-B-Le-Fayet": "St-Gervais-les-Bains-Le Fayet",
        "Lyon-Perrache-Gare-Rout": "Lyon-Perrache",
        "Grenoble-Gare-Routière": "Grenoble",
        "Lyon-St-Paul-la-Feuillée": "Lyon-St-Paul",
        "Lyon-St-Paul-Quai-Bondy": "Lyon-St-Paul",
        "Lyon-Part-Dieu-Gare-Rou": "Lyon-Part-Dieu",
        "Saint-Etienne-Chtx GR": "St-Étienne-Châteaucreux",
        "Cernay-(Lycée)": "Cernay",
        "Sewen-(Eglise)": "Sewen",
        "Bussang (Gare SNCF)": "Bussang",
        "Saint-Léonard Centre": "Saint-Léonard",
        "Ambérieu-en-Bugey": "Ambérieu",
        "Issoudun-Place-de-la-G.": "Issoudun",
        "Pont-Audemer-Gare-SNCF": "Pont-Audemer",
        "Bois-d'Oingt-Centre": "Bois-d'Oingt-Légny",
        "Bitche-Quartier-Driant": "Bitche",
        "Biganos-Facture": "Facture-Biganos",
        "Saint-Claude": "St-Claude",
        "Dole-Ville": "Dole",
        "Sarrebourg-Abri-Phalsbo": "Sarrebourg",
        "Bellegarde-s-V. Gare": "Bellegarde",
        "Belfort-Ville": "Belfort-Montbéliard-TGV",
        "Beauvais-Gare-SNCF": "Beauvais",
        "Basel-SBB": "Basel",
        "Bar-sur-Aube": "Bar-sur-Seine",
        "Montpellier-Saint-Roch": "Montpellier-St-Roch",
        "Aubrais-(les)": "Les Aubrais-Orléans",
        "Aubenas-Pl.-de-la-Paix": "Aubenas",
        "Aix-les-Bains-le-Revard": "Aix-les-Bains-Le Revard",
        "Aix-Gare-Routière": "Aix-en-Provence-TGV",
        "Valence-Gare-Routière": "Valence",
        "Montélimar-G-Routière": "Montélimar",
        "Privas-Cours-du-Palais": "Privas",
        "Annonay-Gare-Route": "Annonay",
        "St-Martin-d'Hères": "Saint-Martin-d'Hères",
        "Chamberry-Jacob": "Chambéry",
        "Aiton-Salle-Polyvalente": "Aiton",
        "Communay-Stade": "Communay",
        "Clelles-Mairie": "Clelles-Mens",
        "Givors-Ville": "Givors-Canal",
        "Felletin-Gare": "Felletin",
        "Châteaubriant-TT": "Châteaubriant Tram-Train",
        "Mulhouse-Gare-Centrale": "Mulhouse-Ville",
        "Roanne-Gare-Routière": "Roanne",
        "La-Rochelle-Porte-Dauphine": "La Rochelle-Porte-Dauphine",
        "Luzy(Nièvre)": "Luzy",
        "Champagnole-PE-Victor": "Champagnole",
        "Ancizes-St-Georges-Bour": "Les Ancizes-St-Georges",
        "Massiac-Blesle": "Massiac",
        "St-Flour-les-Allées": "St-Flour-Chaudes-Aigues",
        "Lapeyrouse(Puy-de-Dôme)": "Manthes-Lapeyrouse",
        "Chauffailles-Gambetta": "Chauffailles",
        "Romorantin-Blanc-Argent": "Romorantin (Voie étroite)",
        "Berthelming-Mairie": "Berthelming",
    }

    def __init__(self) -> None:
        if not os.path.exists(FormatTimetables.TIME_TABLE_PATH):
            raise FileNotFoundError("timetables.csv is missing")

        if not os.path.exists(FormatTimetables.TRAIN_STATIONS_PATH):
            raise FileNotFoundError("train_stations.csv is missing")

        if not os.path.exists(FormatTimetables.TIME_TABLE_FORMATTED_PATH):
            self.format_timetables()

    def set_columns(self) -> None:
        # Create two new columns "gare_a" and "gare_b"
        cols = ["gare_a", "gare_b"]
        for col in cols:
            self.df[col] = ""

        # Split the "trajet" column into two columns "gare_a" and "gare_b"
        for index, row in self.df.iterrows():
            sp = row["trajet"].split(" - ")
            if len(sp) > 2:
                sp = [sp[0], sp[-1]]
            self.df.at[index, "gare_a"] = sp[0]
            self.df.at[index, "gare_b"] = sp[1]

        # Remove "Gare de " from the station names
        for col in cols:
            self.df[col] = self.df[col].str.replace("Gare de ", "")

    def match_train_stations_cities(self) -> None:
        df_train_stations = pd.read_csv(FormatTimetables.TRAIN_STATIONS_PATH, sep=";", encoding="utf-8")
        df_train_stations = df_train_stations[["LIBELLE", "COMMUNE"]]

        # in self.df, replace gare_a and gare_b if it is in SPECIAL_CASES
        for index, row in self.df.iterrows():
            for gare in ["gare_a", "gare_b"]:
                if row[gare] in FormatTimetables.SPECIAL_CASES.keys():
                    self.df.at[index, gare] = FormatTimetables.SPECIAL_CASES[row[gare]]

        for col in ["gare_a_city", "gare_b_city"]:
            self.df[col] = ""

        for col in ["gare_a_matched", "gare_b_matched"]:
            self.df[col] = 0

        for index, row in self.df.iterrows():
            for gare in ["gare_a", "gare_b"]:

                to_check = [
                    row[gare],
                ]

                if not row[gare].startswith(("Le ", "La ", "Les ", "L'", "St")):
                    to_check += [
                        row[gare].split(" ")[0],
                        row[gare].split(".")[0]
                    ]

                to_check = list(set(to_check))

                # Normalize each string in the DataFrame column for comparison without accents
                normalized_column = df_train_stations["LIBELLE"].apply(lambda x: unicodedata.normalize('NFD', x).encode('ascii', 'ignore').decode('utf-8'))

                for check in to_check:
                    normalized_check = unicodedata.normalize('NFD', check).encode('ascii', 'ignore').decode('utf-8')

                    try:
                        if normalized_column.str.contains(normalized_check).any():
                            city = df_train_stations[normalized_column.str.contains(normalized_check)]["COMMUNE"].values[0]
                            self.df.at[index, gare + "_city"] = city
                            self.df.at[index, gare + "_matched"] = 1
                            break
                    except Exception:
                        continue

                if self.df.at[index, gare + "_city"] == "":
                    self.df.at[index, gare + "_city"] = row[gare].upper()

    def format_timetables(self) -> None:
        self.df = pd.read_csv(FormatTimetables.TIME_TABLE_PATH, sep="\t", encoding="utf-8")
        self.set_columns()
        self.match_train_stations_cities()
        self.df.to_csv(FormatTimetables.TIME_TABLE_FORMATTED_PATH, sep="\t", encoding="utf-8", index=False)
        print("timetables_formatted.csv created")


if __name__ == "__main__":
    FormatTimetables()
