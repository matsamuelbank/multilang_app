from django.contrib import admin
from django.urls import path, include
from django.conf.urls.i18n import i18n_patterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns #permet la prise en charges de tous les fichiers static(css, js , ect) une fois le projet déployé

# Utilisation de i18n_patterns pour gérer les URL internationales
urlpatterns = i18n_patterns(
    # URL pour l'interface d'administration
    path('admin/', admin.site.urls),

    # Inclusion des URLs de l'application 'main'
    path('', include('main.urls')),
)

# Gestion des fichiers médias en mode DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += staticfiles_urlpatterns()
