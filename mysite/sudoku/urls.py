from django.urls import path
from .views import generate_puzzle, solve_puzzle

urlpatterns = [
    path('/generate/', generate_puzzle, name='generate_puzzle'),
    path('/solve/<int:puzzle_id>/', solve_puzzle, name='solve_puzzle'),
]