from functions import*

directory = "./speeches-20231109"
extension = "txt"
cleaned_directory = "./cleaned"

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

convertir_texte_minuscules(directory, extension, cleaned_directory)
supprimer_ponctuation_et_traiter_special(cleaned_directory)


resultat_occ_globales = calculer_occurrences_fichiers(directory, extension)
# Affichage des occurrences globales
print()
print(resultat_occ_globales)


resultat_score_idf = calculer_score_idf(directory, extension)
# Affichage des scores IDF
print()
print(resultat_score_idf)
print()
for mot, score_idf in resultat_score_idf.items():
    print(f"{mot}: {score_idf}")