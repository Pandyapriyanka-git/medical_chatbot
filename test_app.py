import unittest
import json
from app import app

class FlaskTestCase(unittest.TestCase):

    def setUp(self):
        """Set up test client."""
        self.app = app.test_client()
        self.app.testing = True

    def test_get_answer(self):
        """Test the /get_answer endpoint."""
        response = self.app.post('/get_answer', json={'question': 'What is asthma?'})
        self.assertEqual(response.status_code, 200)
        response_data = json.loads(response.data)
        self.assertIn('answer', response_data)
        self.assertIn('question', response_data)

    def test_add_knowledge(self):
        """Test adding new knowledge."""
        response = self.app.post('/add_knowledge', json={'question': 'What is diabetes?', 'answer': 'A condition affecting blood sugar levels.'})
        self.assertEqual(response.status_code, 201)

    def test_cache(self):
        """Test cache clearing."""
        response = self.app.get('/clear_cache')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
