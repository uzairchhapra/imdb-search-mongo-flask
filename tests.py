try:
    from main import app
    import unittest as ut
    import json
except Exception as e:
    print('Module error:', e)

class SearchTest(ut.TestCase):
    """A Test case to test the search API
    """

    def test_search(self):
        """Check status code of the response
        """
        tester = app.test_client(self)
        response = tester.post('/search')
        self.assertEqual(response.status_code,200)

    def test_search_content(self):
        """Checks if content type of response is json.
        """
        tester = app.test_client(self)
        response = tester.post('/search')
        self.assertEqual(response.content_type,'application/json')

    def test_search_data(self):
        """Checks if response contains the key 'data'
        """
        tester = app.test_client(self)
        response = tester.post('/search')
        data = response.get_json()
        self.assertTrue('data' in data)



if __name__ == "__main__":
    ut.main()