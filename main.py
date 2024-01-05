import os
from functions import *

print("\t\tWelcome to the main program!")
while True:
    print("\n\t\t\t\t\t\tMenu")
    print("1. Display file names")
    print("2. Extract presidents' names")
    print("3. Clean up files")
    print("4. Display term frequency")
    print("5. Display the inverse frequency of the document")
    print("6. Display TF-IDF matrix")
    print("7. Display the least important words")
    print("8. Display words with the highest TF-IDF score")
    print("9. Display Chirac's most repeated word(s)")
    print("10. Display the presidents who mentioned the 'Nation' and the one who mentioned it most frequently.")
    print("11. Display the presidents who mentioned 'Nation' and the one who repeated it most often.")
    print("12. Display presidents talking about 'Ecologie'")
    print("13. Ask a question")
    print("0. Leave")

    choice = input("Please select an option (0-13): ")

    if choice == "1":
        print("//*** Displaying file names ***//")
        file_list = list_of_files("./speeches-20231109", ".txt")
        print_list(file_list)

    elif choice == "2":
        print("//*** Extracting presidents' names ***//")
        file_list = list_of_files("./speeches-20231109", ".txt")
        president_names = extract_president_names(file_list)
        print("Presidents' names:")
        print(president_names)

    elif choice == "3":
        print("//*** Cleaning up files ***//")
        cleaned_directory = "./cleaned"
        os.makedirs(cleaned_directory, exist_ok=True)
        convert_to_lowercase("./speeches-20231109", ".txt", cleaned_directory)
        print("Files cleaned successfully!")

    elif choice == "4":
        cleaned_directory = "./cleaned"
        print("//*** Term Frequency ***//")
        cleaned_files_list = list_of_files(cleaned_directory, ".txt")
        for filename in cleaned_files_list:
            with open(os.path.join(cleaned_directory, filename), 'r', encoding='utf-8') as file:
                text = file.read()
                word_counts = calculate_word_occurrences(text)
                print(f"Word occurrences in the file {filename}:")
                print()
                for word, count in word_counts.items():
                    print(f"The word '{word}' appears {count} times.")
                print()

    elif choice == "5":
        print("//*** Inverse Document Frequency ***//")
        corpus_directory = "./cleaned"
        idf_scores = calculate_idf_score(corpus_directory, ".txt")
        for word, score in idf_scores.items():
            print(f"Word: {word}, IDF Score: {score}")
        print()

    elif choice == "6":
        corpus_directory = "./cleaned"
        tf_idf_matrix = calculate_tf_idf_matrix(corpus_directory, ".txt")
        print("//*** TF-IDF Matrix ***//")
        for row in tf_idf_matrix:
            print(row)

    elif choice == "7":
        print("//*** Least Important Words ***//")
        corpus_directory = "./cleaned"
        tf_idf_matrix = calculate_tf_idf_matrix(corpus_directory, ".txt")
        idf_scores = calculate_idf_score(corpus_directory, ".txt")
        unimportant_words = display_unimportant_words(tf_idf_matrix, list(idf_scores.keys()))
        print(unimportant_words)


    elif choice == "8":
        print("//*** Mots ayant un score TD-IDF le plus élevé ***//")
        print()
        corpus_directory = "./cleaned"
        tf_idf_matrix = calculate_tf_idf_matrix(corpus_directory, ".txt")
        idf_scores = calculate_idf_score(corpus_directory, ".txt")
        unimportant_words_indices = less_important_words(tf_idf_matrix, list(idf_scores.keys()))
        unique_words = list(idf_scores.keys())
        unimportant_words = [unique_words[i] for i in unimportant_words_indices]
        if unimportant_words:
            print("Words with the highest TF-IDF score:", unimportant_words)
        else:
            print("No words found with a high TF-IDF score.")


    elif choice == '9':
        print("//*** Mots les plus répétés par Chirac ***//")
        print()
        corpus_directory = "./cleaned"
        # Assurez-vous que l'index est correct selon votre structure de données
        president_index_chirac = 0
        tf_idf_matrix = calculate_tf_idf_matrix(corpus_directory, ".txt")
        idf_scores = calculate_idf_score(corpus_directory, ".txt")
        unique_words = list(idf_scores.keys())
        highest_words_by_chirac = most_repeated_words_chirac(tf_idf_matrix, unique_words, president_index_chirac)
        if highest_words_by_chirac:
            print(f"The most repeated word for Chirac (excluding unimportant words) is: {highest_words_by_chirac[0]}")
        else:
            print("No most repeated word for Chirac found.")


    elif choice == '10':
        print("//*** Display the presidents who mentioned 'Nation' and the one who mentioned it most frequently ***//")
        print()

        corpus_directory = "./cleaned"
        tf_idf_matrix = calculate_tf_idf_matrix(corpus_directory, ".txt")
        idf_scores = calculate_idf_score(corpus_directory, ".txt")
        unique_words = list(idf_scores.keys())
        file_list = list_of_files("./speeches-20231109", ".txt")
        president_names = extract_president_names(file_list)
        result = presidents_speaking_about_nation(tf_idf_matrix, unique_words, president_names)
        if result and isinstance(result, list) and len(result) > 0:
            if isinstance(result[0], tuple):
                # Si le premier élément de result est un tuple
                most_repeated_president = result[0][1].replace('.txt', '')
                print("The president(s) who mentioned 'Nation':", result)
                print("The president who mentioned it most frequently:", most_repeated_president)
            else:
                print("Unexpected result format:", result)
        else:
            print("No president mentioned 'Nation' or the word was not found.")

    elif choice == '11':
        corpus_directory = "./cleaned"
        file_list = list_of_files("./speeches-20231109", ".txt")
        president_names = extract_president_names(file_list)
        result = presidents_speaking_about_nation(corpus_directory, ".txt", president_names)
        if result:
            most_repeated_president = result[0][0].replace('.txt', '')
            print("Presidents who mentioned 'Nation':", [president[0].replace('.txt', '') for president in result])
            print("President who repeated 'Nation' most often:", most_repeated_president)
        else:
            print("No president mentioned 'Nation' or the word was not found.")

    elif choice == '12':
        print("//*** Presidents Talking about Climate and Ecology ***//")
        corpus_directory = "./cleaned"
        climate_ecology_words = ['climat', 'écologie']  # Add other relevant words
        file_list = list_of_files("./speeches-20231109", ".txt")
        president_names = extract_president_names(file_list)
        result = presidents_talking_about_climate_ecology(corpus_directory, ".txt", climate_ecology_words, president_names)
        if result:
            print("Presidents who talked about climate and/or ecology:")
            for president, score in result:
                print(f"{president.replace('.txt', '')}: {score}")
        else:
            print("No president talked about climate and/or ecology or the keywords were not found.")

    elif choice == '13':
        corpus_directory = "./cleaned"
        idf_scores = calculate_idf_score(corpus_directory, ".txt")

        question = input("Ask your question: ")
        question_tokens = analyze_question(question)

        term_in_corpus = find_relevant_terms(question_tokens, list(idf_scores.keys()))
        print("Terms in the question present in the corpus:", term_in_corpus)

    elif choice == "0":
        print("GOOD BYE!")
        break

    else:
        print("Invalid option. Please choose a valid option.")
