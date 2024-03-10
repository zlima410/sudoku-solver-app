from django.urls import path
from .views import generate_puzzle, solve_puzzle, get_puzzle

urlpatterns = [
    path('generate/', generate_puzzle, name='generate_puzzle'),
    path('solve/<int:puzzle_id>/', solve_puzzle, name='solve_puzzle'),
    path('get/<int:puzzle_id>/', get_puzzle, name='get_puzzle'),
]