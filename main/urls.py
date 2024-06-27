from django.urls import path
from .views import index, chatbot_rag,chatbot_view
from . import views

# Nommer les applications permet de les distinguer des autres apps au cas où il y en aurait plusieurs
app_name = 'main'

# a la racine du projet on va affiché la vue index
urlpatterns = [
    # Page d'accueil
    path('', index, name = 'index'),
    
    # Vue du chatbot utilisant le RAG
    path('chat_rag/', views.chatbot_rag, name='chat_rag'),
    
    # Vue pour afficher les détails d'un article qui reçoit en paramètre l'id de l'article concerné
    path('article/<int:id>/', views.article_detail, name='article_detail'), #ce chemin ramene au niveau de la vue article_detail 
    
    # chemin vers la fonction my_rag
    path('my_rag', views.my_rag, name='rag_view'),
    
    # Vue du chatbot sans RAG (juste un LLM)
    path('chatbot', views.chatbot_view, name='chatbot'),
]