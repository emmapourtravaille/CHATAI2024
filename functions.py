import os
import string
import math
def list_of_files(directory, extension):
    files_names = [] # Initialisation d'une liste vide pour les noms de fichiers
    for filename in os.listdir(directory): # Parcours des fichiers dans le répertoire spécifié
        if filename.endswith(extension): # Vérification de l'extension du fichier
            files_names.append(filename)
    return files_names

def print_list(file_list):
    for file_name in file_list:
        print(file_name)  # Affiche chaque élément de la liste sur une nouvelle ligne

def extract_president_names(file_names):
    president_names = set() # Initialise un ensemble pour stocker les noms des présidents uniques
    for file_name in file_names: # Parcours de chaque nom de fichier dans la liste
        name_without_extension = file_name.split('.')[0] # Extrait le nom de fichier sans l'extension
        parts = name_without_extension.split('_') # Extrait le nom complet après le premier '_'
        if len(parts) >= 2:
            president_name = parts[1]
            president_name = ''.join([char for char in president_name if not char.isdigit()]) # Récupère le nom du président (élimine les chiffres s'il y en a)
            president_names.add(president_name) # Ajoute le nom du président à l'ensemble

    return list(president_names) # Convertit l'ensemble en liste et la retourne

def associate_first_name_to_president(full_name):
    first_names_dictionary = {
        'Chirac': 'Jacques',
        'Giscard dEstaing': 'Valéry',
        'Hollande': 'François',
        'Macron': 'Emmanuel',
        'Mitterand': 'François',
        'Sarkozy': 'Nicolas'
    }

    last_name = full_name.split('.')[0]  # Exclut l'extension du fichier
    first_name = first_names_dictionary.get(last_name, '')

    if first_name:
        return first_name, full_name
    elif "Mitterrand" in last_name:
        return "François", full_name
    elif "Chirac" in last_name:
        return "Jacques", full_name
    else:
        print("No first name associated for:", full_name)
        return "", ""  # Retourne une chaîne vide dans les cas où aucun prénom n'est associé

def display_list_of_president_names(file_names):
    president_names = extract_president_names(file_names) # Extraire les noms des présidents à partir des noms de fichiers
    cleaned_president_names = set() # Initialiser un ensemble pour stocker les noms de présidents uniques

    for name in president_names:  # Parcourir chaque nom de président
        cleaned_name = ''.join([char for char in name if not char.isdigit()])   # Supprimer les chiffres à la fin du nom
        cleaned_president_names.add(cleaned_name)

    unique_president_names = list(cleaned_president_names)   # Convertir l'ensemble en liste pour afficher

    print("\n\-/ List of president names (without duplicates): \-/\n ")   # Afficher la liste des noms de présidents sans doublons
    print_list(unique_president_names)

def convert_to_lowercase(directory, extension, output_directory):
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            with open(f"{directory}/{filename}", 'r', encoding='utf-8') as input_file:
                content = input_file.read()

            lowercase_content = "".join([chr(ord(char) + 32) if 'A' <= char <= 'Z' else char for char in content])  # Convertir le contenu en minuscules

            with open(f"{output_directory}/{filename}", 'w', encoding='utf-8') as output_file:   # Écrire le contenu converti dans un nouveau fichier dans le répertoire de sortie
                output_file.write(lowercase_content)

def remove_punctuation_and_handle_special(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        treated_content = ''.join([' ' if char in string.punctuation and char not in ["'", "-"] else char for char in content])   # Supprimer la ponctuation, en conservant les apostrophes et les tirets

        with open(file_path, 'w', encoding='utf-8') as file:   # Réécrire le contenu traité dans le même fichier
            file.write(treated_content)


def calculate_word_occurrences(text):
    occurrences = {}   # Initialiser un dictionnaire pour stocker les occurrences des mots
    words = text.split()  # Diviser le texte en mots

    for word in words:  # Parcourir chaque mot dans la liste de mots
        word = word.strip(string.punctuation).lower()  # Supprimer la ponctuation et convertir en minuscules
        occurrences[word] = occurrences.get(word, 0) + 1  # Mettre à jour le compteur d'occurrences pour le mot actuel
    return occurrences


def calculate_file_occurrences(cleaned_directory, extension):
    global_occurrences = {}

    for filename in os.listdir(cleaned_directory):
        if filename.endswith(extension):
            file_path = os.path.join(cleaned_directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            file_occurrences = calculate_word_occurrences(content)   # Calculer les occurrences des mots dans le fichier actuel

            for word, occurrence in file_occurrences.items():   # Mettre à jour les occurrences globales en tenant compte du fichier actuel
                global_occurrences[word] = global_occurrences.get(word, 0) + occurrence

    return global_occurrences


def calculate_idf_score(cleaned_directory, extension):
    documents_containing_word_count = {}  # Initialiser un dictionnaire pour compter le nombre de documents contenant chaque mot
    total_documents = 0

    # Compter le nombre de documents contenant chaque mot
    for filename in os.listdir(cleaned_directory):
        if filename.endswith(extension):
            total_documents += 1

            file_path = os.path.join(cleaned_directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            unique_words = set(content.split())

            for word in unique_words: # Mettre à jour le compteur pour chaque mot dans le dictionnaire global
                documents_containing_word_count[word] = documents_containing_word_count.get(word, 0) + 1

    # Calculer le score IDF pour chaque mot
    idf_score = {}
    for word, documents_containing_count in documents_containing_word_count.items():
        idf_score[word] = round(math.log(total_documents / (1 + documents_containing_count)))  # Arrondi à l'entier

    return idf_score


def calculate_tf_idf_matrix(cleaned_directory, extension):
    global_occurrences = calculate_file_occurrences(cleaned_directory, extension) # Étape 1 : Calculer la Fréquence des Termes (TF) pour chaque mot dans chaque document
    idf_score = calculate_idf_score(cleaned_directory, extension)   # Étape 2 : Calculer le score IDF pour chaque mot
    files_names = [filename for filename in os.listdir(cleaned_directory) if filename.endswith(extension)]  # Liste des fichiers dans le répertoire
    unique_words = list(global_occurrences.keys())  # Liste des mots uniques
    tf_idf_matrix = []  # Étape 3 : Calculer la matrice TF-IDF

    for filename in files_names:
        file_path = os.path.join(cleaned_directory, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if len(content.split()) == 0:
            tf_idf_vector = [0] * len(unique_words)
        else:
            file_occurrences = calculate_word_occurrences(content)

            # Calculer le vecteur TF-IDF pour chaque document
            tf_idf_vector = [file_occurrences.get(word, 0) / len(content.split()) * idf_score.get(word, 0) for word in unique_words]

        tf_idf_matrix.append(tf_idf_vector)

    # Step 4: Return the TF-IDF matrix
    return tf_idf_matrix


def display_unimportant_words(tf_idf_matrix, unique_words):
    num_unique_words = len(unique_words)

    # Utiliser une liste pour stocker les indices des mots moins importants
    unimportant_words = []

    for i in range(num_unique_words):
        # Vérifier la longueur de chaque document avant d'accéder à l'indice
        if all(len(doc) > i for doc in tf_idf_matrix):
            # Si tous les documents ont une longueur supérieure à l'indice i, ajouter l'indice aux mots non importants
            unimportant_words.append(i)

    # Afficher les mots non importants
    print("Indices des mots non importants :", unimportant_words)

    # Utiliser ces indices pour obtenir les mots non importants
    words_occurrences = {word: [doc[i] for doc in tf_idf_matrix if len(doc) > i] for i, word in enumerate(unique_words)
                         if i in unimportant_words}

    # Afficher les occurrences des mots non importants
    for word, occurrences in words_occurrences.items():
        print(f"Le mot '{word}' a des occurrences dans les documents non importants :", occurrences)


def less_important_words(tf_idf_matrix, unique_words):
    unimportant_words = []  # Initialiser une liste pour stocker les indices des mots moins importants
    for j in range(len(tf_idf_matrix[0])):  # Itérer à travers les colonnes de la matrice TF-IDF (chaque document)
        if all(tf_idf_matrix[i][j] == 0 for i in range(len(tf_idf_matrix))):  # Vérifier si tous les scores TF-IDF pour un mot donné dans tous les documents sont égaux à zéro
            unimportant_words.append(j)

    return unimportant_words

def word_with_max_tf_idf(tf_idf_matrix, unique_words):
    max_indices = [max(range(len(tf_idf_matrix)), key=lambda i: tf_idf_matrix[i][j]) for j in range(len(tf_idf_matrix[0]))] # Trouver les indices des documents avec les scores TF-IDF max pour chaque mot
    words_max_tf_idf = [unique_words[i] for i in max_indices]   # Obtenir les mots correspondant aux indices trouvés

    return words_max_tf_idf


def most_repeated_words_chirac(tf_idf_matrix, unique_words, president_index_chirac):
    if not 0 <= president_index_chirac < len(
            tf_idf_matrix[0]):  # Assurer que president_index_chirac est un index valide
        print("Invalid president index.")
        return []

    occurrences = [(tf_idf_matrix[i][president_index_chirac], unique_words[i]) for i in range(len(tf_idf_matrix))]
    occurrences.sort(reverse=True)

    # Retourner uniquement le mot le plus répété
    most_repeated_words = [word for score, word in occurrences if score != 0][:1]

    return most_repeated_words


def presidents_speaking_about_nation(tf_idf_matrix, unique_words, president_names):
    if 'nation' not in unique_words:
        return None

    index_nation = unique_words.index('nation')

    occurrences = {}
    for i, president in enumerate(president_names):
        if index_nation < len(tf_idf_matrix) and i < len(tf_idf_matrix[index_nation]):  # Vérifier si l'index est dans les limites de la matrice
            occurrences[president] = tf_idf_matrix[index_nation][i]
        else:
            occurrences[president] = 0

    sorted_presidents = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)  # Trier les présidents en fonction du score TF-IDF pour le mot 'nation'
    return sorted_presidents
def presidents_talking_about_climate_ecology(tf_idf_matrix, unique_words, climate_ecology_words, president_names):
    index_words = []
    for word in climate_ecology_words:
        if word in unique_words:
            index_words.append(unique_words.index(word))
    president_scores = {president: sum(tf_idf_matrix[i][j] for i in index_words) for j, president in enumerate(president_names)}
    sorted_presidents = sorted(president_scores.items(), key=lambda x: x[1], reverse=True)
    return sorted_presidents
def analyze_question(question):
    # Convert the question to lowercase
    question = question.lower()

    # Remove punctuation
    question = ''.join([char if char not in string.punctuation else ' ' for char in question])

    # Tokenize the question into words
    question_tokens = question.split()

    return question_tokens

def find_relevant_terms(tokenized_question, unique_words_corpus):
    """
    Finds and returns the terms in the question that are also present in the corpus.
    """
    relevant_terms = set(tokenized_question).intersection(unique_words_corpus)
    return list(relevant_terms)

def calculate_vector_tf_idf_question(tokenized_question, idf_score_corpus, unique_words_corpus):
    """
    Calculates the TF-IDF vector for the question based on the IDF scores of the corpus.
    """
    tf_idf_vector_question = []
    for word in unique_words_corpus:
        tf = tokenized_question.count(word)
        idf = idf_score_corpus.get(word, 0)
        tf_idf_vector_question.append(tf * idf)
    return tf_idf_vector_question

def dot_product(A, B):
    """
    Calculates and returns the dot product between two vectors A and B.
    """
    if len(A) != len(B):
        raise ValueError("Vectors must have the same dimension.")

    return sum(a * b for a, b in zip(A, B))

def vector_norm(A):
    """
    Calculates and returns the norm of a vector A.
    """
    return math.sqrt(sum(a ** 2 for a in A))

def cosine_similarity(A, B):
    """
    Calculates and returns the cosine similarity between two vectors A and B.
    """
    product = dot_product(A, B)
    norm_A = vector_norm(A)
    norm_B = vector_norm(B)

    if norm_A == 0 or norm_B == 0:
        return 0

    return product / (norm_A * norm_B)

# Example of usage:

# Example vectors
vector_A = [1, 2, 3]
vector_B = [4, 5, 6]

# Calculating cosine similarity
cosine_similarity_result = cosine_similarity(vector_A, vector_B)
print("Cosine similarity:", cosine_similarity_result)

def generate_response(document_index, documents):
    """
    Generates a response based on the most relevant document found.
    """
    return documents[document_index]
