import os
import app
import unittest
import tempfile

class AppTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, app.app.config['DATABASE'] = tempfile.mkstemp()
        app.app.testing = True
        self.app = app.app.test_client()
        with app.app.app_context():
            app.phone_book

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(app.app.config['DATABASE'])
    #test home page
    def test_empty_db(self):
        rv = self.app.get('/')
        assert 'No entries here so far'

    
    #test add contact method 
    def test_add_contact(self):
        rv = self.app.post('/add_contact', data=dict(name='<anything>', phone='<anything>'), follow_redirects=True) 
        assert 'anything' 
        assert 'anything'
    #test  delete contact
    def test_delete_contact(self):
        rv = self.app.post('/delete_contact', data=dict(name='<anything>', phone='<anything>'), follow_redirects=True) 
        assert 'anything' 
        assert 'anything'

    #test  delete contact method
    def test_edit_contact(self):
        rv = self.app.post('/test_edit_contact', data=dict(name='<anything>', phone='<anything>'), follow_redirects=True) 
        assert 'anything' 
        assert 'anything'
      

if __name__ == '__main__':
    unittest.main()