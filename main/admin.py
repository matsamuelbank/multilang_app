from django.contrib import admin
from .models import Article

#en utilisant le admin.ModelAdmin ,le model Article sera affiché comme une table 
#dans le dashbord admin
@admin.register(Article)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ("title", 'content', 'publication_date',"title_trad", "content_trad")



