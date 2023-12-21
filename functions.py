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
    dictionnaire_prenoms = {
        'Chirac': 'Jacques',
        'Giscard dEstaing': 'Valéry',
        'Hollande': 'François',
        'Macron': 'Emmanuel',
        'Mitterand': 'François',
        'Sarkozy': 'Nicolas'
    }
    # Utiliser le nom complet comme clé dans le dictionnaire
    nom = nom_complet.split('.')[0]  # Exclure l'extension du fichier
    prenom = dictionnaire_prenoms.get(nom, '')

    # Si le prénom est trouvé, retourner le nom complet associé
    if prenom:
        return prenom, nom_complet

    # Gérer manuellement les cas spécifiques
    if "Mitterrand" in nom:
        return "François", nom_complet

    if "Chirac" in nom:
        return "Jacques", nom_complet

    # Si le prénom n'est pas trouvé, retourner simplement le nom complet tel quel
    print("Aucun prénom associé pour :", nom_complet)
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
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            with open(f"{directory}/{filename}", 'r') as input_file:
                contenu = input_file.read()

            contenu_minuscules = "".join([chr(ord(char) + 32) if 'A' <= char <= 'Z' else char for char in contenu])

            with open(f"{output_directory}/{filename}", 'w') as output_file:
                output_file.write(contenu_minuscules)
def supprimer_ponctuation_et_traiter_special(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        with open(file_path, 'r') as file:
            contenu = file.read()

        contenu_traite = ''.join([' ' if char in string.punctuation and char not in ["'", "-"] else char for char in contenu])

        with open(file_path, 'w') as file:
            file.write(contenu_traite)


def calculer_occurrences_mots(texte):
    occ = {}
    mots = texte.split()

    for mot in mots:
        mot = mot.strip(string.punctuation).lower()  # Convert to lowercase
        occ[mot] = occ.get(mot, 0) + 1

    return occ


def calculer_occurrences_fichiers(cleaned_directory, extension):
    occ_globales = {}

    for filename in os.listdir(cleaned_directory):
        if filename.endswith(extension):
            file_path = os.path.join(cleaned_directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                contenu = file.read()

            occ_fichier = calculer_occurrences_mots(contenu)

            for mot, occurrence in occ_fichier.items():
                occ_globales[mot] = occ_globales.get(mot, 0) + occurrence

    return occ_globales

def calculer_score_idf(cleaned_directory, extension):
    nb_documents_contenant_mot = {}
    nb_documents_total = 0

    # Compter le nombre de documents contenant chaque mot
    for filename in os.listdir(cleaned_directory):
        if filename.endswith(extension):
            nb_documents_total += 1

            file_path = os.path.join(cleaned_directory, filename)

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

def calculer_tf_idf_matrix(cleaned_directory, extension):
    # Step 1: Calculer la fréquence du terme (TF) pour chaque mot dans chaque document
    occurrences_globales = calculer_occurrences_fichiers(cleaned_directory, extension)

    # Step 2: Calculer le score IDF pour chaque mot
    score_idf = calculer_score_idf(cleaned_directory, extension)

    # Liste des fichiers dans le répertoire
    files_names = [filename for filename in os.listdir(cleaned_directory) if filename.endswith(extension)]

    # Liste des mots uniques
    mots_uniques = list(occurrences_globales.keys())

    # Step 3: Calculer la matrice TF-IDF
    tf_idf_matrix = []

    for filename in files_names:
        file_path = os.path.join(cleaned_directory, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            contenu = file.read()

        occurrences_fichier = calculer_occurrences_mots(contenu)

        # Calculer le vecteur TF-IDF pour chaque document
        tf_idf_vector = [occurrences_fichier.get(mot, 0) / len(contenu.split()) * score_idf.get(mot, 0)
                         for mot in mots_uniques]

        tf_idf_matrix.append(tf_idf_vector)

    # Step 4: Retourner la matrice TF-IDF
    return tf_idf_matrix

def afficher_mots_non_importants(tf_idf_matrix, mots_uniques):
    mots_occurrences = {word: [doc[i] for doc in tf_idf_matrix] for i, word in enumerate(mots_uniques)}
    mots_non_importants = [word for word, tfidf_list in mots_occurrences.items() if all(tfidf == 0 for tfidf in tfidf_list)]

    return mots_non_importants

def mots_moins_importants(tf_idf_matrix, mots_uniques):
    mots_non_importants = []

    # Parcourez les colonnes de la matrice TF-IDF (chaque document)
    for j in range(len(tf_idf_matrix[0])):
        # Vérifiez si tous les scores TF-IDF pour un mot donné dans tous les documents sont égaux à zéro
        if all(tf_idf_matrix[i][j] == 0 for i in range(len(tf_idf_matrix))):
            mots_non_importants.append(j)

    return mots_non_importants

def mot_max_tf_idf(tf_idf_matrix, mots_uniques):
    max_indices = [max(range(len(tf_idf_matrix)), key=lambda i: tf_idf_matrix[i][j]) for j in range(len(tf_idf_matrix[0]))]
    mots_max_tf_idf = [mots_uniques[i] for i in max_indices]

    return mots_max_tf_idf

def mots_plus_repetes_chirac(tf_idf_matrix, mots_uniques, president_index_chirac):
    occurences = [(tf_idf_matrix[i][president_index_chirac], mots_uniques[i]) for i in range(len(tf_idf_matrix))]
    occurences.sort(reverse=True)
    mots_plus_repetes = [mot for score, mot in occurences if score != 0]

    return mots_plus_repetes


def occurrences_mot_president(tf_idf_matrix, mots_uniques, mot):
    index_mot = mots_uniques.index(mot)
    occurrences = [(tf_idf_matrix[index_mot][j], president_names[j]) for j in range(len(tf_idf_matrix[0]))]
    occurrences.sort(reverse=True)
    return occurrences

def presidents_parlant_climat_ecologie(tf_idf_matrix, mots_uniques, mots_climat_ecologie):
    index_mots = [mots_uniques.index(mot) for mot in mots_climat_ecologie]
    president_scores = {president: sum(tf_idf_matrix[i][j] for i in index_mots) for j, president in enumerate(president_names)}
    sorted_presidents = sorted(president_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_presidents



def tokeniser_question(question):
    # Convertir la question en minuscules
    question = question.lower()

    # Supprimer la ponctuation
    question = ''.join([char if char not in string.punctuation else ' ' for char in question])

    # Tokeniser la question en mots
    mots = question.split()

    return mots

def trouver_termes_dans_corpus(mots_question, mots_corpus):
    termes_communs = set(mots_question).intersection(mots_corpus)
    return list(termes_communs)


def calculer_vecteur_tf_idf_question(mots_question, scores_tf_corpus, scores_idf_corpus, mots_corpus):
    vecteur_tf_idf_question = []

    for mot_corpus in mots_corpus:
        if mot_corpus in mots_question:
            # Calculer le score TF pour le mot dans la question
            tf_question = mots_question.count(mot_corpus)

            # Récupérer le score IDF déjà calculé pour le mot dans le corpus
            idf_corpus = scores_idf_corpus.get(mot_corpus, 0)

            # Calculer le score TF-IDF pour le mot dans la question
            tf_idf_question = tf_question * idf_corpus
            vecteur_tf_idf_question.append(tf_idf_question)
        else:
            # Le mot du corpus n'est pas présent dans la question, mettre 0
            vecteur_tf_idf_question.append(0)

    return vecteur_tf_idf_question