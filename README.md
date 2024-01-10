URL du git : https://github.com/emmapourtravaille/CHATAI2024.git

Introduction 
Dans le cadre de notre formation, nous avons dû nous lancer dans la réalisation d'un chatbot en utilisant le langage de programmation Python. Ce projet constitue un défi stimulant, sollicitant à la fois nos compétences en algorithmique, en traitement du langage naturel, et en conception logicielle. Le résultat final reflète non seulement notre compréhension des concepts enseignés, mais également notre capacité à les appliquer.                                                                                                                              Au fil de cette introduction, nous explorerons les fonctions du projet, nous verrons différents aspects de notre algorithme et enfin nous verrons le bilan de tout cet apprentissage. 

1.	Présentation du projet

L'objectif de ce projet consiste à programmer un chatbot en Python qui peut analyser et répondre à des questions en se basant sur un ensemble spécifique de données textuelles. Cela implique le développement de fonctions telles que le traitement des chaînes de caractères, l'utilisation de structures de données comme les listes, les ensembles et les dictionnaires, ainsi que l'application de concepts de traitement du langage naturel tels que le calcul de la fréquence des mots et la similarité des textes. 

2.	Principaux objectifs et enjeux

Ce chatbot a été conçu pour répondre aux interrogations des utilisateurs	 concernant les discours d'investiture des présidents français qu’on possède dans nos données. Son objectif principal est de simplifier l'obtention de réponses en extrayant directement les éléments nécessaires des discours. L'objectif global est de formuler des réponses claires et précises afin d'assister les utilisateurs dans leurs recherches liées à ces discours présidentiels.






I.     Fonctionnalité 
1. Fonctionnalités du projet
1.	Traitement de Texte : Avant toute chose, les textes subissent un traitement général, toutes les majuscules sont converties en minuscules et on supprime également toute la ponctuation hormis les cas spéciaux. Cela garantit une cohérence dans l'ensemble du corpus et facilite une analyse textuelle uniforme.

2.	Calcul de la fréquence des mots : Cette analyse approfondie de la fréquence des mots dans le corpus nous permet d'identifier les termes clés qui donnent un aperçu des mots les plus émergeant du discours inaugural.


3.	Matrice TF-IDF : Cette technique évalue l'importance des mots dans un document en considérant leur fréquence dans l'ensemble du corpus. 

4.	Similarité Cosinus : Pour répondre de manière ciblée aux questions des utilisateurs, la similarité cosinusoïdale est utilisée. Cette méthode mesure la similarité entre les questions posées par les utilisateurs et les documents du corpus, permettant ainsi d'identifier plus facilement les passages les plus pertinents et d'apporter des réponses précises.
5.	Calcule du document le plus pertinent : Le rôle de la fonction décrite est de déterminer le document le plus pertinent en réponse à une question donnée. 









II	Présentation technique
1.	Description des principaux algorithmes réalisés  
Dans la fonction associate_first_name_to_president :
On a choisi d’utiliser une structure avec le dictionnaire car elle est efficace, en effet elle nous permet de relier rapidement le nom avec le prénom associé. 
On a ajouté des cas spécifiques pour "Mitterrand" et "Chirac" permettent de traiter certains noms de famille qui ne correspondent pas exactement au dictionnaire tout en garantissant que le prénom correct soit associé, même si la correspondance exacte du nom de famille n'est pas présente dans le dictionnaire.

Dans la fonction remove_punctuation_and_handle_special : 
La structure permet de parcourir rapidement le contenu du fichier, de le traiter en éliminant certains caractères de ponctuation tout en préservant les apostrophes et les tirets, puis de réécrire le résultat dans le même fichier. Cela permet de modifier le fichier sans créer des fichiers intermédiaires.

La fonction calculate_tf_idf_matrix prend en paramètre (cleaned_directory) 	contenant des documents textuels et une extension de fichier spécifiée 		(extension). On a décidé d’utiliser une liste pour répertorier les noms des 		fichiers et les mots uniques généré à partir de leur score du TF-IDF, puisque 	grâce à la longueur de la liste on peut parcourir les fichiers et ainsi calculer le 	TF-IDF


1.	Difficultés rencontrées et solutions apportées  
 
En effet, durant l'avancement du projet, nous avons rencontré de nombreux obstacles nous mettant à difficulté : 

1. Calcul de TF-IDF : ne sachant pas ce qu’était le TF-IDF nous avons eu beaucoup de mal à comprendre son but exact. Par conséquent l’approche de cette fonction à prit plus de temps que prévu puisque nous avons eu du mal à comprendre par où commencer.
 	
2. Similarité Cosinus : L'application de la similarité cosinus pour comparer efficacement les vecteurs était techniquement exigeante puisqu’il y’avait plusieurs détails à prendre en compte car fonction cosinus_similarite effectue une division par le produit des deux normes donc il était important de s'assurer que les normes des vecteurs ne soient pas nulles pour éviter une division par zéro.  



IV	Bilan apprentissages
En conclusion, ce projet a été une expérience d'apprentissage précieuse à plusieurs niveaux :

1.	     Le plan technique  

Sur le plan technique, la réalisation de ce projet nous a permis d’approfondir nos connaissances ainsi que nos capacités à résoudre des problèmes. C’était en effet très enrichissant pour l’une et pour l’autre. Les défis rencontrés, tels que l'implémentation du calcul TF-IDF et la mesure de la similarité cosinus, ont renforcé nos compétences en programmation et en résolution de problèmes.


2.	     L’organisation du travail   

Afin de parvenir au projet, il nous a fallu savoir communiquer clairement ainsi que de répartir les tâches en fonction de la facilité que chacune possède. A l’origine, on travaillait séparément sur différentes parties avant de tout assembler puis sur la dernière semaine, nous avons dû s’entraider sur les difficultés de sa partenaire.

3.	     La gestion du temps  

La gestion du temps est également extrêmement importante pour ne pas se perdre dans le projet et pouvoir continuer avec un suivi homogène. 
Nous avons appris l'importance de planifier et de respecter les délais dans un projet complexe, équilibrant les exigences techniques avec les contraintes de temps. En effet, d’un point de vue extérieur cela nous donnait l’impression d’avoir une grande marge de temps, or, ayant aperçu nos difficultés face à la programmation, le projet se rapprochait à grand pas de la date limite sans le remarquer. 
