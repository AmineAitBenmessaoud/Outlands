# Readme - Jeu Vidéo en Python

Ce dépôt contient un jeu vidéo créé en utilisant la librairie Python. Vous êtes sur le point de découvrir un monde virtuel passionnant et des défis stimulants. Suivez les instructions ci-dessous pour installer et jouer au jeu.

## Installation

Avant de pouvoir plonger dans le monde du jeu, assurez-vous d'avoir toutes les dépendances nécessaires installées. Vous pouvez les installer en utilisant pip et le fichier "requirements.txt" fourni.

```bash
pip install -r requirements.txt
```

Assurez-vous également d'avoir Python correctement installé sur votre système. Si ce n'est pas le cas, vous pouvez le télécharger depuis [le site officiel de Python](https://www.python.org/downloads/).

## Lancement du Jeu

Une fois que vous avez installé toutes les dépendances et vérifié que Python est bien configuré, vous êtes prêt à lancer le jeu. Pour ce faire, exécutez le fichier "game.py" à l'aide de Python.

```bash
python game.py
```

## Jouer au Jeu

Félicitations ! Vous avez maintenant accès à une expérience de jeu divertissante. Explorez le monde virtuel, relevez les défis et profitez de l'excitation du jeu. Que la meilleure stratégie gagne !
## Diagramme de classe

<img src="Diagramme de classes.png"></img>

## Environnement de test


	Nous avons effectué trois types de tests pour le jeu : Tests de fonctionnalité, tests d'intégration et tests de performance.
Test de fonctionnalité : vérifie que les méthodes font exactement ce qu’elles sont censées faire.
Test d’intégration : vérifie que l’intégration des méthodes dans le corps du jeu se fait sans conflit avec d’autres méthodes.
Test de performance : vérifie que les méthodes n’ont pas beaucoup de latence et ne ralentissent pas le jeu.
Tests de fonctionnalité et d’intégration :
Ces types sont faits au fur et à mesure de l'implémentation des fonctionnalités. Ces tests se font selon la structure suivante : 

Exemple d’un test pour la fonctionnalité mouvement du joueur : 


Tests de performances :
Se fait qualitativement en testant le jeu dans plusieur PC différents et quantitativement grâce à la bibliothèque time[6] de python selon l’algorithme suivant : 
debut = time.time()  # Temps au début de l'exécution de la méthode
méthode testée()
fin = time.time()  # Temps à la fin de l'exécution de la méthode
temps execution = fin - début 
Le calcul du temps d'exécution permet de valider que les fonctionnalités du jeu sont en accord avec les contraintes imposées dans le cahier de charge du jeu. Les fonctionnalitées qu’on a validées jusqu’à présent sont : 
Le lancement du jeu, les contrôles du jeu, les interactions avec les obstacles et les ennemis.

## Besoin d'Aide ?

Si vous avez des questions, des problèmes techniques ou des commentaires à propos du jeu, n'hésitez pas à créer une nouvelle issue dans ce dépôt. Notre équipe est là pour vous aider.

Amusez-vous bien et que la chance soit de votre côté dans ce jeu passionnant !
