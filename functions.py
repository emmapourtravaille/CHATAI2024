import os
import string
import math
def list_of_files(directory, extension):
    files_names = []
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            files_names.append(filename)
    return files_names

def print_list(file_list):
    for file_name in file_list:
        print(file_name)

dictionnaire_prenoms = {
    'Chirac1': 'Jacques',
    'Giscard dEstaing': 'Valéry',
    'Hollande': 'François',
    'Macron': 'Emmanuel',
    'Mitterand': 'François',
    'Sarkozy': 'Nicolas'
}


def extract_president_names(file_names):
    president_names = set()
    for file_name in file_names:
        # Extraire le nom du fichier sans l'extension
        name_without_extension = file_name.split('.')[0]

        # Extraire le nom complet après le premier '_'
        parts = name_without_extension.split('_')
        if len(parts) >= 2:
            president_name = parts[1]
            president_names.add(president_name)
    return list(president_names)

def associer_prenom_president(nom_complet):
    # Utiliser le nom complet comme clé dans le dictionnaire
    nom = nom_complet.split('.')[0]  # Exclure l'extension du fichier
    prenom = dictionnaire_prenoms.get(nom, '')

    # Si le prénom est trouvé, retournez le nom complet associé
    if prenom:
        return f"{prenom} {nom_complet}"

    # Gérer manuellement les cas spécifiques
    if "Mitterrand" in nom:
        return f"François", {nom_complet}

    if "Chirac" in nom:
        return f"Jacques", {nom_complet}

    # Si le prénom n'est pas trouvé, retournez simplement le nom complet tel quel
    print("Aucun prénom associé pour :", {nom_complet})
    return nom_complet

def afficher_liste_noms_presidents(file_names):
    president_names = extract_president_names(file_names)
    cleaned_president_names = set()

    for name in president_names:
        # Retirer les chiffres à la fin du nom
        cleaned_name = ''.join([char for char in name if not char.isdigit()])
        cleaned_president_names.add(cleaned_name)

    unique_president_names = list(cleaned_president_names)

    print("\n\-/    Liste des noms des présidents (sans doublons) :   \-/\n ")
    print_list(unique_president_names)

def convertir_texte_minuscules(directory, extension, output_directory):
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    for filename in os.listdir(directory):
        if filename.endswith(extension):
            input_filepath = os.path.join(directory, filename)
            output_filepath = os.path.join(output_directory, filename)

            with open(input_filepath, 'r', encoding='utf-8') as input_file:
                contenu = input_file.read()

            contenu_minuscules = contenu.lower()

            with open(output_filepath, 'w', encoding='utf-8') as output_file:
                output_file.write(contenu_minuscules)

def supprimer_ponctuation_et_traiter_special(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        # Lire le contenu du fichier
        with open(file_path, 'r', encoding='utf-8') as file:
            contenu = file.read()

        # Supprimer la ponctuation en traitant les cas spéciaux
        contenu_traite = ''
        for char in contenu:
            if char in string.punctuation and char not in ["'", "-"]:
                contenu_traite += ' '
            else:
                contenu_traite += char

        # Enregistrez le contenu traité dans le même fichier
        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(contenu_traite)

def calculer_occurrences_mots(texte):
    occ = {}
    mots = texte.split()

    for mot in mots:
        mot = mot.strip(string.punctuation).lower()
        occ[mot] = occ.get(mot, 0) + 1

    return occ

def calculer_occurrences_fichiers(directory, extension):
    occ_globales = {}

    for filename in os.listdir(directory):
        if filename.endswith(extension):
            file_path = os.path.join(directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                contenu = file.read()

            occ_fichier = calculer_occurrences_mots(contenu)

            for mot, occurrence in occ_fichier.items():
                occ_globales[mot] = occ_globales.get(mot, 0) + occurrence

    return occ_globales

def calculer_score_idf(directory, extension):
    nb_documents_contenant_mot = {}
    nb_documents_total = 0

    # Compter le nombre de documents contenant chaque mot
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            nb_documents_total += 1

            file_path = os.path.join(directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                contenu = file.read()

            mots_uniques = set(contenu.split())

            for mot in mots_uniques:
                nb_documents_contenant_mot[mot] = nb_documents_contenant_mot.get(mot, 0) + 1

    # Calculer le score IDF pour chaque mot
    score_idf = {}
    for mot, nb_documents_contenant in nb_documents_contenant_mot.items():
        score_idf[mot] = round(math.log(nb_documents_total / (1 + nb_documents_contenant)))  # Arrondi en entier

    return score_idf

