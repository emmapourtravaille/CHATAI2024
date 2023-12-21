from functions import*

directory = "./speeches-20231109"
extension = "txt"
cleaned_directory = "./cleaned"
output_directory = "./cleaned"

files_names = list_of_files(directory, extension)
print("\n\-/   Liste des fichiers dans le répertoire :   \-/\n ")
print_list(files_names)

president_names = extract_president_names(files_names)
print("\n\-/    Liste des noms des présidents :   \-/\n ")
print_list(president_names)



president_names_with_first_names = [associer_prenom_president(nom) for nom in president_names]
print("\n\-/    Noms avec prénoms associés :   \-/\n ")
print_list(president_names_with_first_names)

afficher_liste_noms_presidents(files_names)

convertir_texte_minuscules(directory, extension, output_directory)
supprimer_ponctuation_et_traiter_special(cleaned_directory)

occurrences_globales = calculer_occurrences_fichiers(cleaned_directory, extension)
print("\nOccurrences globales des mots dans tous les fichiers:\n", occurrences_globales)



resultat_score_idf = calculer_score_idf(cleaned_directory, extension)
print("\nScore IDF pour chaque mot:\n", resultat_score_idf)
print()


tf_idf_matrix = calculer_tf_idf_matrix(cleaned_directory, extension)
print("\nMatrice TF-IDF :\n")
for row in tf_idf_matrix:
    formatted_row = [round(value, 2) for value in row]
    print(formatted_row)

mots_uniques = list(occurrences_globales.keys())

non_importants = mots_moins_importants(tf_idf_matrix, mots_uniques)
print("\nMots les moins importants (TF-IDF = 0 dans tous les fichiers) :\n")
for index in non_importants:
    print(mots_uniques[index])

max_tf_idf = mot_max_tf_idf(tf_idf_matrix, mots_uniques)
print("\nMot(s) avec le score TF-IDF le plus élevé :\n")
print(max_tf_idf)


index_chirac = president_names.index('Chirac')
mots_plus_repetes = mots_plus_repetes_chirac(tf_idf_matrix, mots_uniques, index_chirac)
print("\nMot(s) le(s) plus répété(s) par le président Chirac (hors mots non importants) :\n")
print(mots_plus_repetes)


mot_nation_occurrences = occurrences_mot_president(tf_idf_matrix, mots_uniques, 'nation')
print("\nOccurrences du mot 'Nation' par président :\n")
for score, president in mot_nation_occurrences:
    print(f"{president}: {score}")


mots_climat_ecologie = ['climat', 'écologie']
presidents_climat_ecologie = presidents_parlant_climat_ecologie(tf_idf_matrix, mots_uniques, mots_climat_ecologie)
print("\nPrésident(s) parlant du climat et/ou de l'écologie :\n")
for president, score in presidents_climat_ecologie:
    print(f"{president}: {score}")


def afficher_menu():
    print("\nMenu:")
    print("1. Afficher la liste des mots les moins importants")
    print("2. Afficher le(s) mot(s) ayant le score TD-IDF le plus élevé")
    print("3. Indiquer le(s) mot(s) le(s) plus répété(s) par le président Chirac")
    print("4. Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation »")
    print("5. Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé du climat et/ou de l’écologie")
    print("0. Quitter")

def main():
    files_names = list_of_files(directory, extension)
    president_names = extract_president_names(files_names)

    while True:
        afficher_menu()
        choix = input("Choisissez une option (0-5): ")

        if choix == '1':
            tf_idf_matrix = calculer_tf_idf_matrix(directory, extension)
            mots_uniques = list(calculer_occurrences_fichiers(directory, extension).keys())
            non_importants = mots_moins_importants(tf_idf_matrix, mots_uniques)
            print("Mots les moins importants :", non_importants)

        elif choix == '2':
            mots_importants = mots_plus_importants(tf_idf_matrix, mots_uniques)
            print("Mot(s) ayant le score TD-IDF le plus élevé :", mots_importants)

        elif choix == '3':
            mots_plus_repetes_chirac = mots_plus_repetes_par_president(tf_idf_matrix, president_names, 'Chirac')
            print("Mot(s) le(s) plus répété(s) par le président Chirac :", mots_plus_repetes_chirac)

        elif choix == '4':
            noms_presidents_nation = presidents_parlant_de_mot(tf_idf_matrix, president_names, 'Nation')
            print("Nom(s) du (des) président(s) parlant de la « Nation » :", noms_presidents_nation)

        elif choix == '5':
            noms_presidents_climat_ecologie = presidents_parlant_de_mot(tf_idf_matrix, president_names, 'climat', 'écologie')
            print("Nom(s) du (des) président(s) parlant du climat et/ou de l’écologie :", noms_presidents_climat_ecologie)

        elif choix == '0':
            print("Au revoir !")
            break

        else:
            print("Option invalide. Veuillez choisir une option valide (0-5).")

if __name__ == "__main__":
    main()


question_utilisateur = input("Posez votre question : ")
mots_question = tokeniser_question(question_utilisateur)
print("Mots de la question :", mots_question)

termes_communs = trouver_termes_dans_corpus(mots_question, mots_uniques)
print("Termes de la question présents dans le corpus :", termes_communs)

# Calculer le vecteur TF-IDF pour les termes de la question
vecteur_tf_idf_question = calculer_vecteur_tf_idf_question(mots_question, scores_tf_corpus, scores_idf_corpus, mots_uniques)
print("Vecteur TF-IDF de la question :", vecteur_tf_idf_question)
t