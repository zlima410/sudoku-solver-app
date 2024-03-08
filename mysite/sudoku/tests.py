from django.test import TestCase, Client
from .models import Sudoku

# Create your tests here.

class SudokuSolverTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        # create a new puzzle
        self.test_puzzle = Sudoku.objects.create(puzzle='530070000600195000098000060800060003400803001700020006060000280000419005000080079')

    def test_solver(self):
        # solve the puzzle
        response = self.client.get(f'/solve/{self.test_puzzle.id}/')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['status'], 'success')
        self.assertEqual(response.json()['message'], 'Puzzle solved successfully')
        self.assertEqual(response.json()['solution'], '534678912672195348198342567859761423426853791713924856961537284287419635345286179')