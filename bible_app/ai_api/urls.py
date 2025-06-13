from django.urls import path
from . import views

app_name = 'ai_api'

urlpatterns = [
    path('explain_selection/', views.explain_selection_view, name='explain_selection'),
    path('define_selection/', views.define_selection_view, name='define_selection'),
    path('ask_question/', views.ask_question_view, name='ask_question'), # Renamed from ask_question to avoid conflict with potential future non-selection based ask
    path('ask_selection/', views.ask_selection_view, name='ask_selection'),
    path('get_quiz/', views.get_quiz_view, name='get_quiz'),
    path('submit_quiz/', views.submit_quiz_view, name='submit_quiz'),
    path('summarize_chapter/', views.summarize_chapter_view, name='summarize_chapter'),
    path('search_selection/', views.search_selection_view, name='search_selection'), # For images
    path('search_map_selection/', views.search_map_selection_view, name='search_map_selection'), # For maps
] 