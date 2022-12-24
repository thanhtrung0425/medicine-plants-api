from django.urls import path
from . import views


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('upload/', views.UploadDataFromCSV.as_view()),
    path('clean-cache/', views.ClearCache.as_view()),
    path('medicine-plants/', views.LoadData.as_view({'get':'loadData'})),
    path('medicine-plant/id=<str:id>', views.GetItemMedicinePlants.as_view()),
]
