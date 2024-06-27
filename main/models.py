from django.db import models

# déclaration du modèle d'article,il permet l'ajout d'un article
class Article(models.Model):
    title = models.CharField(max_length=255) 
    content = models.TextField()  
    publication_date = models.DateTimeField()
    title_trad = models.CharField(max_length=255, default='')
    content_trad = models.TextField(default='')

    def __str__(self):
        return self.title

    None
    
    def get_title(self):
        return self.title
    
    def get_date(self):
        return self.publication_date
    