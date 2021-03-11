from unittest import TestCase
from app import app
from flask import session
from boggle import Boggle

app.config['TESTING'] = True
app.config['DEBUG_TB_HOSTS'] = ['hide-debug-toolbar']


class FlaskTests(TestCase):

    def test_homepage(self):
        """ test if score and highscore dispays on page"""
        with app.test_client() as client:
            response = client.get('/')

            self.assertEqual(response.status_code, 200)
            self.assertIn('board', session)
            self.assertIsNone(session.get('highscore'))
            self.assertIsNone(session.get('nplays'))

    def test_word(self):
        """ testing if the word is valid"""
        with app.test_client() as client:
            client.get('/')
            response = client.get('/check-word?word="ghghgh')

            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json['result'], 'not-word')

    def test_score(self):
        """testing highscore from post request """
        with app.test_client() as client:
            response = client.post('/user-score', data={'$score': 1})

            self.assertEqual(response.status_code, 200)
            self.assertIn(response.json['$score'], 1)