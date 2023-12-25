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
        # Extract the file name without the extension
        name_without_extension = file_name.split('.')[0]

        # Extract the full name after the first '_'
        parts = name_without_extension.split('_')
        if len(parts) >= 2:
            president_name = parts[1]

            president_name = ''.join([char for char in president_name if not char.isdigit()])
            president_names.add(president_name)

    return list(president_names)

def associate_first_name_to_president(full_name):
    first_names_dictionary = {
        'Chirac': 'Jacques',
        'Giscard dEstaing': 'Valéry',
        'Hollande': 'François',
        'Macron': 'Emmanuel',
        'Mitterand': 'François',
        'Sarkozy': 'Nicolas'
    }
    # Use the full name as the key in the dictionary
    last_name = full_name.split('.')[0]  # Exclude the file extension
    first_name = first_names_dictionary.get(last_name, '')

    # If the first name is found, return the associated full name
    if first_name:
        return first_name, full_name
    # Handle specific cases manually
    if "Mitterrand" in last_name:
        return "François", full_name

    if "Chirac" in last_name:
        return "Jacques", full_name

    # If the first name is not found, simply return the full name as is
    print("No first name associated for:", full_name)
    return full_name

def display_list_of_president_names(file_names):
    president_names = extract_president_names(file_names)
    cleaned_president_names = set()

    for name in president_names:
        # Remove digits at the end of the name
        cleaned_name = ''.join([char for char in name if not char.isdigit()])
        cleaned_president_names.add(cleaned_name)

    unique_president_names = list(cleaned_president_names)

    print("\n\-/ List of president names (without duplicates): \-/\n ")
    print_list(unique_president_names)

def convert_to_lowercase(directory, extension, output_directory):
    for filename in os.listdir(directory):
        if filename.endswith(extension):
            with open(f"{directory}/{filename}", 'r', encoding='utf-8') as input_file:
                content = input_file.read()

            lowercase_content = "".join([chr(ord(char) + 32) if 'A' <= char <= 'Z' else char for char in content])

            with open(f"{output_directory}/{filename}", 'w', encoding='utf-8') as output_file:
                output_file.write(lowercase_content)

def remove_punctuation_and_handle_special(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        treated_content = ''.join([' ' if char in string.punctuation and char not in ["'", "-"] else char for char in content])

        with open(file_path, 'w', encoding='utf-8') as file:
            file.write(treated_content)


def calculate_word_occurrences(text):
    occurrences = {}
    words = text.split()

    for word in words:
        word = word.strip(string.punctuation).lower()  # Convert to lowercase
        occurrences[word] = occurrences.get(word, 0) + 1

    return occurrences


def calculate_file_occurrences(cleaned_directory, extension):
    global_occurrences = {}

    for filename in os.listdir(cleaned_directory):
        if filename.endswith(extension):
            file_path = os.path.join(cleaned_directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            file_occurrences = calculate_word_occurrences(content)

            for word, occurrence in file_occurrences.items():
                global_occurrences[word] = global_occurrences.get(word, 0) + occurrence

    return global_occurrences


def calculate_idf_score(cleaned_directory, extension):
    documents_containing_word_count = {}
    total_documents = 0

    # Count the number of documents containing each word
    for filename in os.listdir(cleaned_directory):
        if filename.endswith(extension):
            total_documents += 1

            file_path = os.path.join(cleaned_directory, filename)

            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()

            unique_words = set(content.split())

            for word in unique_words:
                documents_containing_word_count[word] = documents_containing_word_count.get(word, 0) + 1

    # Calculate IDF score for each word
    idf_score = {}
    for word, documents_containing_count in documents_containing_word_count.items():
        idf_score[word] = round(math.log(total_documents / (1 + documents_containing_count)))  # Rounded to integer

    return idf_score


def calculate_tf_idf_matrix(cleaned_directory, extension):
    # Step 1: Calculate the Term Frequency (TF) for each word in each document
    global_occurrences = calculate_file_occurrences(cleaned_directory, extension)

    # Step 2: Calculate the IDF score for each word
    idf_score = calculate_idf_score(cleaned_directory, extension)

    # List of files in the directory
    files_names = [filename for filename in os.listdir(cleaned_directory) if filename.endswith(extension)]

    # List of unique words
    unique_words = list(global_occurrences.keys())

    # Step 3: Calculate the TF-IDF matrix
    tf_idf_matrix = []

    for filename in files_names:
        file_path = os.path.join(cleaned_directory, filename)

        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()

        if len(content.split()) == 0:
            tf_idf_vector = [0] * len(unique_words)
        else:
            file_occurrences = calculate_word_occurrences(content)

            # Calculate the TF-IDF vector for each document
            tf_idf_vector = [file_occurrences.get(word, 0) / len(content.split()) * idf_score.get(word, 0) for word in unique_words]

        tf_idf_matrix.append(tf_idf_vector)

    # Step 4: Return the TF-IDF matrix
    return tf_idf_matrix

def display_unimportant_words(tf_idf_matrix, unique_words):
    words_occurrences = {word: [doc[i] for doc in tf_idf_matrix] for i, word in enumerate(unique_words)}
    unimportant_words = [word for word, tfidf_list in words_occurrences.items() if all(tfidf == 0 for tfidf in tfidf_list)]

    return unimportant_words

def less_important_words(tf_idf_matrix, unique_words):
    unimportant_words = []

    # Iterate through the columns of the TF-IDF matrix (each document)
    for j in range(len(tf_idf_matrix[0])):
        # Check if all TF-IDF scores for a given word in all documents are equal to zero
        if all(tf_idf_matrix[i][j] == 0 for i in range(len(tf_idf_matrix))):
            unimportant_words.append(j)

    return unimportant_words

def word_with_max_tf_idf(tf_idf_matrix, unique_words):
    max_indices = [max(range(len(tf_idf_matrix)), key=lambda i: tf_idf_matrix[i][j]) for j in range(len(tf_idf_matrix[0]))]
    words_max_tf_idf = [unique_words[i] for i in max_indices]

    return words_max_tf_idf


def most_repeated_words_chirac(tf_idf_matrix, unique_words, president_index_chirac):
    # Ensure president_index_chirac is a valid index
    if not 0 <= president_index_chirac < len(tf_idf_matrix[0]):
        print("Invalid president index.")
        return []

    occurrences = [(tf_idf_matrix[i][president_index_chirac], unique_words[i]) for i in range(len(tf_idf_matrix))]
    occurrences.sort(reverse=True)
    most_repeated_words = [word for score, word in occurrences if score != 0]

    return most_repeated_words


def presidents_speaking_about_nation(tf_idf_matrix, unique_words, president_names):
    if 'nation' not in unique_words:
        return None

    index_nation = unique_words.index('nation')

    occurrences = {}
    for i, president in enumerate(president_names):
        # Check if the index is within the bounds of the matrix
        if index_nation < len(tf_idf_matrix) and i < len(tf_idf_matrix[index_nation]):
            occurrences[president] = tf_idf_matrix[index_nation][i]
        else:
            occurrences[president] = 0

    sorted_presidents = sorted(occurrences.items(), key=lambda x: x[1], reverse=True)
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
