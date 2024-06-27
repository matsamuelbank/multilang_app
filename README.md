# multilang_site
projet qui consiste à créer une application multilingue( français et anglais) utilisant le framwork Django et qui utilise un LLM  et une fonctionnalité RAG pour répondre aux questions des utilisateurs.

## Prérequis
Avant d'exécuter ce projet, assurez-vous d'avoir les éléments suivants :
- Python installé sur votre ordinateur.
- Avoir une clé OpenAi valide 

## Installation des dépendances 
1. Ouvrez le dossier du projet dans un éditeur de texte tel que Visual Studio Code.
2. Allez dans le fichier settings et faites ceci :
    - décommentez ces lignes :
          DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.sqlite3',
              'NAME': BASE_DIR / 'db.sqlite3',
          }
      }
    - commentez ces lignes : 
      DATABASES = {
      'default': dj_database_url.parse(config('DATABASE_URL'))
      }
    - Changer la valeur de la variable DEBUG et la mettre à True
      DEBUG = True

3. Ensuite, appuyez sur `Ctrl + J` pour ouvrir le terminal.
4. Installez un envirronnement virtuel en entrant la commande `python -m venv venv`
5. Activez l'envirronnement virtuel en entrant la commande `.\venv\Scripts\activate`
6. Enrez la commande `python.exe -m pip install -r requirements.txt` pour installer toutes les dépendances nécessaires.

## Exécution du projet
1. Toujours dans le terminal, exécutez la commande suivante : `python manage.py runserver`.
   Vous devriez voir un résultat semblable au suivant :
   System check identified no issues (0 silenced).
  June 26, 2024 - 13:33:43
  Django version 5.0.6, using settings 'multilang_site.settings'
  Starting development server at http://127.0.0.1:8000/
  Quit the server with CTRL-BREAK.

Pour accéder au site, survolez l'URL `http://127.0.0.1:8000/` et cliquez dessus, ou copiez l'URL et coller dans votre navigateur.

## Ajouter un article depuis le dashbord admin
Pour ajouter un article depuis le dashbord admin il faut entrer cette url:
  - http://127.0.0.1:8000/admin/

## Test de la fonctionnalité multilingue
- Dans la barre de navigation du site, cliquez sur l'un des drapeaux (français ou anglais) pour changer la langue du contenu.
- Pour ajouter un nouveau contenu au site (titres, paragraphes, etc.) :
- Entourez votre texte avec le mot-clé `trans`, comme dans cet exemple pour un paragraphe :
 ```html
 <p>{% trans "Mettez votre texte ici" %}</p>
 ```
- Exécutez ensuite les commandes suivantes :
 - Pour le français : `python manage.py makemessages -l fr`
 - Pour l'anglais : `python manage.py makemessages -l en`
 - Dans le fichier `django.po`, ajoutez la traduction dans la ligne `msgstr` exemple :  msgstr"mettez votre traduction ici".
 - Compilez les messages traduits avec : `python manage.py compilemessages`.
 - Enfin, exécutez : `django-admin compilemessages`.

## Test de la fonctionnalité de recherche aurgmentée (RAG)
Pour ce projet la fonctionnalité RAG a été implémenté en indexant le fichier articles.pdf, en parcourant ses pages et en donnant des réponses en fonction de son contenu et de la question posée.

Pour tester la fonctionnalité RAG du projet via le ChatBot vous pouvez lui poser ce genre de question :
  - dans la zone de saisie vous pouvez premièrement entrer ceci : `Bonjour, donne-moi des articles sur la tech` et il vous listera les articles ou données sur la tech qu'il a.
  - puis en fonction de la liste d'articles qu'il vous donnera vous pouvez poser la question suivante : `Donne-moi plus de detail sur le premier article` et il vous en dira plus sur le premier article.
