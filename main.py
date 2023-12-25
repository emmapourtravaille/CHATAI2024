from functions import*


# Définition des répertoires et de l'extension
directory = "./speeches-20231109"
extension = "txt"
cleaned_directory = "./cleaned"
output_directory = "./cleaned"

# Liste des fichiers dans le répertoire
files_names = list_of_files(directory, extension)

# Affichez la liste des fichiers dans le répertoire
print("\n\-/ Liste des fichiers dans le répertoire : \-/\n")
print_list(files_names)

# Extrait les noms des présidents des noms de fichiers
president_names = extract_president_names(files_names)

# Affichez la liste des noms des présidents
print("\n\-/ Liste des noms des présidents : \-/\n")
print_list(president_names)

# Associez les prénoms aux noms de présidents
president_names_with_first_names = [associer_prenom_president(nom) for nom in president_names]

# Affichez les noms avec prénoms associés
print("\n\-/ Noms avec prénoms associés : \-/\n")
print_list(president_names_with_first_names)

# Affichez la liste des noms de présidents par fichier
afficher_liste_noms_presidents(files_names)

# Convertissez le texte en minuscules et supprimez la ponctuation
convertir_texte_minuscules(directory, extension, output_directory)
supprimer_ponctuation_et_traiter_special(cleaned_directory)

# Calculez les occurrences globales des mots dans tous les fichiers
occurrences_globales = calculer_occurrences_fichiers(cleaned_directory, extension)
print("\nOccurrences globales des mots dans tous les fichiers:\n", occurrences_globales)

# Calculez le score IDF pour chaque mot
resultat_score_idf = calculer_score_idf(cleaned_directory, extension)
print("\nScore IDF pour chaque mot:\n", resultat_score_idf)
print()

# Calculez la matrice TF-IDF
tf_idf_matrix = calculer_tf_idf_matrix(cleaned_directory, extension)
print("\nMatrice TF-IDF :\n")
for row in tf_idf_matrix:
    formatted_row = [round(value, 2) for value in row]
    print(formatted_row)

# Obtenez la liste des mots uniques
mots_uniques = list(occurrences_globales.keys())

# Trouvez les mots les moins importants
non_importants = mots_moins_importants(tf_idf_matrix, mots_uniques)
print("\nMots les moins importants (TF-IDF = 0 dans tous les fichiers) :\n")
for index in non_importants:
    print(mots_uniques[index])

# Trouvez le mot avec le score TF-IDF le plus élevé
max_tf_idf = mot_max_tf_idf(tf_idf_matrix, mots_uniques)
print("\nMot(s) avec le score TF-IDF le plus élevé :\n")
print(max_tf_idf)

# Trouvez le président Chirac et les mots les plus répétés par lui
index_chirac = list(president_names).index('Chirac')
mots_plus_repetes = mots_plus_repetes_chirac(tf_idf_matrix, mots_uniques, index_chirac)
print("\nMot(s) le(s) plus répété(s) par le président Chirac (hors mots non importants) :\n")
print(mots_plus_repetes)

# Trouvez le président qui a parlé le plus du mot 'nation'
resultats_president_mot = president_parlant_de_mot(tf_idf_matrix, mots_uniques, president_names, 'nation')

# Vérifiez si la fonction a renvoyé une valeur
if resultats_president_mot is not None:
    president_max_occurrences, max_occurrences = resultats_president_mot
    print(f"\nLe président qui a le plus parlé du mot 'nation' est : {president_max_occurrences} avec {max_occurrences} occurrences.")
else:
    print("Aucun résultat disponible.")

# Trouvez les présidents qui parlent du climat et/ou de l'écologie
mots_climat_ecologie = ['climat', 'écologie']
presidents_climat_ecologie = presidents_parlant_climat_ecologie(tf_idf_matrix, mots_uniques, mots_climat_ecologie)
print("\nPrésident(s) parlant du climat et/ou de l'écologie :\n")
for president, score in presidents_climat_ecologie:
    print(f"{president}: {score}")

# Exemple d'utilisation de la fonction analyser_question
question = "Quels sont les présidents qui ont parlé de la Nation?"
mots_question = analyser_question(question)

# Exemple d'utilisation de la fonction trouver_termes_pertinents
termes_pertinents = trouver_termes_pertinents(mots_question, mots_uniques)
print(f"\nTermes pertinents dans la question : {termes_pertinents}")

# Exemple d'utilisation de la fonction calculer_vecteur_tf_idf_question
vecteur_tf_idf_question = calculer_vecteur_tf_idf_question(mots_question, resultat_score_idf, mots_uniques)
print(f"\nVecteur TF-IDF de la question : {vecteur_tf_idf_question}")

# Exemple d'utilisation de la fonction similarite_cosinus
resultat_similarite_cosinus = similarite_cosinus(vecteur_tf_idf_question, tf_idf_matrix[0])
print(f"\nSimilarité cosinus avec le premier document : {resultat_similarite_cosinus}")

# Vous pouvez ajouter d'autres fonctionnalités en fonction de vos besoins


def afficher_menu():
    print("\nMenu:")
    print("1. Afficher la liste des mots les moins importants")
    print("2. Afficher le(s) mot(s) ayant le score TD-IDF le plus élevé")
    print("3. Indiquer le(s) mot(s) le(s) plus répété(s) par le président Chirac")
    print("4. Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé de la « Nation »")
    print("5. Indiquer le(s) nom(s) du (des) président(s) qui a (ont) parlé du climat et/ou de l’écologie")
    print("0. Quitter")


