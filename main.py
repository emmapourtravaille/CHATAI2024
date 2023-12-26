from functions import*


directory = "./speeches-20231109"
extension = "txt"
cleaned_directory = "./cleaned"
output_directory = "./cleaned"

# List of files in the directory
files_names = list_of_files(directory, extension)

# Display the list of files in the directory
print("\n\-/ List of files in the directory: \-/\n")
print_list(files_names)

# Extract the names of presidents from the file names
president_names = extract_president_names(files_names)

# Display the list of president names
print("\n\-/ List of president names: \-/\n")
print_list(president_names)

# Associate first names with president names
president_names_with_first_names = [associate_first_name_to_president(name) for name in president_names]

# Display names with associated first names
print("\n\-/ Names with associated first names: \-/\n")
print_list(president_names_with_first_names)

# Display the list of president names per file
display_list_of_president_names(files_names)

# Convert the text to lowercase and remove punctuation
convert_to_lowercase(directory, extension, output_directory)
remove_punctuation_and_handle_special(cleaned_directory)

# Calculate global occurrences of words in all files
global_occurrences = calculate_file_occurrences(cleaned_directory, extension)
print("\nGlobal occurrences of words in all files:\n", global_occurrences)

# Calculate IDF score for each word
idf_score_result = calculate_idf_score(cleaned_directory, extension)
print("\nIDF score for each word:\n", idf_score_result)
print()

# Calculate TF-IDF matrix
tf_idf_matrix = calculate_tf_idf_matrix(cleaned_directory, extension)
print("\nTF-IDF Matrix:\n")
for row in tf_idf_matrix:
    formatted_row = [round(value, 2) for value in row]
    print(formatted_row)


# Get the list of unique words
unique_words = list(global_occurrences.keys())

# Find the least important words
non_important_words = less_important_words(tf_idf_matrix, unique_words)
print("\nLeast important words (TF-IDF = 0 in all files):\n")
for index in non_important_words:
    print(unique_words[index])

# Find the word with the highest TF-IDF score
max_tf_idf_word = word_with_max_tf_idf(tf_idf_matrix, unique_words)
print("\nWord(s) with the highest TF-IDF score:\n")
print(max_tf_idf_word)

# Find President Chirac and the most repeated words by him
index_chirac = list(president_names).index('Chirac')
most_repeated_words = most_repeated_words_chirac(tf_idf_matrix, unique_words, index_chirac)
print("\nMost repeated words by Chirac:\n", most_repeated_words)

# Find the president who talked the most about the word 'nation'
presidents_nation = presidents_speaking_about_nation(tf_idf_matrix, unique_words, president_names)
if presidents_nation:
    print("\nPresident(s) who spoke about 'nation':\n")
    for president, occurrences in presidents_nation:
        print(f"{president}: {occurrences}")
else:
    print("No data on 'nation' in the speeches.")

# Define words related to climate and ecology
climate_ecology_words = ['climate', 'ecology']
presidents_climate_ecology = presidents_talking_about_climate_ecology(tf_idf_matrix, unique_words,climate_ecology_words, president_names)

if presidents_climate_ecology:
    print("\nPresident(s) talking about climate and/or ecology:\n")
    for president, score in presidents_climate_ecology:
        print(f"{president}: {score}")
else:
    print("No data on 'climate' or 'ecology' in the speeches.")
# Example of using the analyze_question function
question = "Which presidents have talked about the Nation?"
question_words = analyze_question(question)

# Example of using the find_relevant_terms function
relevant_terms = find_relevant_terms(question_words, unique_words)
print(f"\nRelevant terms in the question: {relevant_terms}")

# Now call calculate_vector_tf_idf_question with the correct parameters
resultat_score_idf = calculate_vector_tf_idf_question(cleaned_directory, extension)
tf_idf_vector_question = calculate_vector_tf_idf_question(question_words, resultat_score_idf, unique_words)
print(f"\nTF-IDF vector of the question: {tf_idf_vector_question}")

# Example of using the cosine_similarity function
cosine_similarity_result = cosine_similarity(tf_idf_vector_question, tf_idf_matrix[0])
print(f"\nCosine similarity with the first document: {cosine_similarity_result}")

# You can add other functionalities based on your needs

def display_menu():
    print("\nMenu:")
    print("1. Display the list of least important words")
    print("2. Display the word(s) with the highest TD-IDF score")
    print("3. Show the word(s) most repeated by President Chirac")
    print("4. Show the name(s) of the president(s) who spoke about the 'Nation'")
    print("5. Show the name(s) of the president(s) who spoke about climate and/or ecology")
    print("0. Quit")

t
