import unittest
from app import app


class TestingApp(unittest.TestCase):


    #Does the app loads up correctly
    def test_index(self):
        tester = app.test_client(self)
        resp = tester.get('/', content_type='html/text')
        self.assertEqual(resp.status_code, 200)
    
    #Does the app requires login when one wants to add a post
    def test_requiresLoginBeforePost(self):
        tester = app.test_client(self)
        resp = tester.get('/addPost', data=dict(username="username1", password="password1"), follow_redirects=True)
        self.assertIn(b'You are trying', resp.data)
'''
    #If the user visits unknown Page. Does the error page loads
    def test_unkownPageVisited(self):
        tester = app.test_client(self)
        resp = tester.post('/posts/maina', data=dict(username="user", password="pass"), follow_redirects=True)
        self.assertIn(b'Sorry', resp.data)

    #Corerct logins
    def test_correctLogin(self):
        tester = app.test_client(self)
        resp = tester.post('/login', data=dict(username='user', password='pass'), follow_redirects=True) 
        self.assertIn(b'You are logged in', resp.data)

    #Incorrect Logins
    def test_incorrectLogint(self):
        tester = app.test_client(self)
        resp = tester.post('/login', data=dict(username='username', password='passwoird'), follow_redirects=True)
        self.assertIn(b'Please try again', resp.data)
    #Does the user able to add a post
    def test_addPost(self):
        tester = app.test_client(self)
        resp = tester.post('/addpost', data=dict(username='username', password='passwoird'), follow_redirects=True)
        self.assertEqual(resp.status_code, 200)

'''
if __name__ == '__main__':
    unittest.main()
    
    
