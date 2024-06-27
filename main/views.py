from django.shortcuts import redirect, render, HttpResponse
from django.utils.translation import gettext_lazy as _
from .models import Article
from django.views import View
from django.contrib import messages
import os
from langchain_community.document_loaders import PyPDFLoader
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()  # Charge les variables d'environnement à partir du fichier .env
api_key = os.getenv("API_KEY")


# Définition de la fonction de vue 'index'
def index(request, *args, **kwargs):
    # récupère tous les articles présent dans le modèle Article
    liste_articles = Article.objects.all()
    
    # rajoutes les articles créés dans la liste appelé liste_articles
    context = {'articles': liste_articles}
    
    # Envoie le context au templates index.html
    return render(request, 'index.html', context)

def article_detail(request, id):
    # recupère l'article (ou l'objet) dans le modèle dont l'id correspond à l'id passé en paramètre (id modèle == id passé en paramètre) dans l'url vers le template  article_detail
    article = Article.objects.get(id=id)
    return render(request, 'articles/article_detail.html', {'article': article})

# Chargement du fichier dans lequel se trouves les données(des articles)
file_path = os.path.join(os.path.dirname(__file__), 'data', 'articles.pdf')
loader = PyPDFLoader(file_path)
pages = loader.load_and_split()

# Création des embeddings
embeddings = OpenAIEmbeddings(api_key=api_key)

# Création de l'index FAISS
faiss_index = FAISS.from_documents(pages, embeddings)

# Fonction de recherche de similarité et de génération de réponses
def my_rag(query, k=2):
    # Recherche de similarité
    docs = faiss_index.similarity_search(query, k=k)
    
    # Construit le contexte pour la génération de réponses
    context = "\n\n".join([doc.page_content for doc in docs])
    prompt = f"Context:\n{context}\n\nQuestion: {query}\nAnswer:"
    
    client = OpenAI(api_key=api_key)
    
    # Génère la réponse
    response = client.chat.completions.create(
        model="gpt-4",  
        messages=[
            {"role": "system", "content": "assistant"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=2000
    )
    
    # Retourne la réponse générée
    return response.choices[0].message.content.strip()

# vue qui permet d'afficher les requêttes-réponses du chatbot qui utilise le RAG (elle utilise la fonction my_rag)
def chatbot_rag(request):
    # Vérifie s'il existe déjà une conversation en session, sinon initialisez une nouvelle conversation
    conversation = request.session.get('conversation', [])

    if request.method == 'POST':
        # Vérifie si l'utilisateur a demandé une réinitialisation de la conversation
        if 'reset' in request.POST:
            # Réinitialise la conversation
            conversation = []
        else:
            # Récupère l'entrée utilisateur depuis la requête POST
            user_input = request.POST.get('user_input')
            chatbot_replies = []

            if user_input:
                # Ajoute l'entrée utilisateur à la conversation
                conversation.append({"role": "user", "content": user_input})

                # Utilise my_rag pour générer la réponse
                reply = my_rag(user_input)
                chatbot_replies.append(reply)
                
                # Ajoute la réponse du chatbot à la conversation
                conversation.append({"role": "assistant", "content": reply})

        # Met à jour la conversation en session
        request.session['conversation'] = conversation

        # Renvoie la page chat.html avec les données de la conversation
        return render(request, 'chat_rag.html', {'conversation': conversation})
    else:
        # Affiche la conversation en cours sans la réinitialiser
        return render(request, 'chat_rag.html', {'conversation': conversation})
    

# vue qui permet de créer un chatbot avec le LLM gpt-4 sans RAG
def chatbot_view(request):
    conversation = request.session.get('conversation', [])
    
    # si la méthode de la requête de l'utilisateur est une POST
    if request.method == 'POST':
        
        # Vérifie si l'utilisateur a demandé une réinitialisation de la conversation
        if 'reset' in request.POST:
            # Réinitialise la conversation
            conversation = []
            # Met à jour la conversation en session
            request.session['conversation'] = conversation
            # Renvoie la page sans aucun user_input ou chatbot_replies
            return render(request, 'chatbot.html', {'conversation': conversation})
        else:
            # Récupère l'entrée utilisateur depuis la requête POST
            user_input = request.POST.get('user_input')
            prompts = []
            request.session['conversation'] = conversation

            if user_input:
                # Ajoute l'entrée utilisateur à la conversation
                conversation.append({"role": "user", "content": user_input})

            # ettend la liste des conversation avec les anciennes(cela permet de conserver l'historique des conversations précédentes)
            prompts.extend(conversation)

            # Initialise le client OpenAI avec la clé d'API
            client = OpenAI(api_key=api_key)

            # Génère une réponse du chatbot en utilisant le modèle GPT-4
            response = client.chat.completions.create(
                messages=prompts,
                model="gpt-4",
            )

            # Extrait les réponses du chatbot de la réponse complète
            chatbot_replies = [message.message.content for message in response.choices if message.message.role == 'assistant']
            
            # Ajoute les réponses du chatbot à la conversation
            for reply in chatbot_replies:
                conversation.append({"role": "assistant", "content": reply})

        # Met à jour la conversation en session
        request.session['conversation'] = conversation

        # Renvoie la page chat.html avec les données de la conversation
        return render(request, 'chatbot.html', {'user_input': user_input, 'chatbot_replies': chatbot_replies, 'conversation': conversation})
    else:
        # Efface la conversation en session
        request.session.clear()
        return render(request, 'chatbot.html', {'conversation': conversation})
