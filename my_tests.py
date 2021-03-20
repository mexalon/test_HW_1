import unittest
from unittest.mock import patch

from main import *

mock_directories = {
    '1': ['2207 876234', '11-2', '5455 028765'],
    '2': ['10006'],
    '3': []
}

mock_documents = [
    {"type": "passport", "number": "2207 876234", "name": "Василий Гупкин"},
    {"type": "invoice", "number": "11-2", "name": "Геннадий Покемонов"},
    {"type": "insurance", "number": "10006", "name": "Аристарх Павлов"}
]


def make_fake_input(*args):
    gen_for_input = (arg for arg in args)

    def fake_input(spam):
        return next(gen_for_input)

    return fake_input


class MyTestCase(unittest.TestCase):
    def test_check_document_existance(self):
        self.assertEqual(check_document_existance('10006'), True)
        self.assertEqual(check_document_existance(''), False)

    @patch('main.documents', new=mock_documents)
    def test_get_all_doc_owners_names(self):
        exp_res = set([doc['name'] for doc in mock_documents])
        self.assertEqual(get_all_doc_owners_names(), exp_res)

    def test_get_doc_owner_name(self):
        with unittest.mock.patch('builtins.input', return_value='10006'):
            self.assertEqual(get_doc_owner_name(), 'Аристарх Павлов')

    def test_get_doc_shelf_1(self):
        with unittest.mock.patch('builtins.input', return_value='10006'):
            self.assertEqual(get_doc_shelf(), '2')
        with unittest.mock.patch('builtins.input', return_value='not_spam'):
            self.assertEqual(get_doc_shelf(), None)

    @patch.dict('main.directories', mock_directories)
    @patch('builtins.input', return_value='10006')
    @patch('main.check_document_existance', return_value=True)
    def test_get_doc_shelf_2(self, check_document_existance, input):
        self.assertEqual(get_doc_shelf(), '2')

    def test_remove_doc_from_shelf(self):
        """это же равноценный синтаксис с предыдущим тестом?"""
        with unittest.mock.patch.dict('main.directories', mock_directories):
            with unittest.mock.patch('main.check_document_existance', return_value=True):
                with unittest.mock.patch('builtins.input', return_value='11-2'):
                    self.assertEqual(get_doc_shelf(), '1')
                    self.assertEqual(remove_doc_from_shelf('11-2'), None)
                    self.assertEqual(get_doc_shelf(), None)

    @patch('builtins.input', return_value='4')
    def test_add_new_shelf(self, input):
        self.assertEqual(add_new_shelf('1'), ('1', False))
        self.assertEqual(add_new_shelf('4'), ('4', True))
        self.assertEqual(add_new_shelf(), ('4', False))

    @patch.dict('main.directories', mock_directories)
    @patch('builtins.input', return_value='some_doc_number')
    @patch('main.check_document_existance', return_value=True)
    def test_append_doc_to_shelf(self, check_document_existance, input):
        append_doc_to_shelf('some_doc_number', '3')
        self.assertEqual(get_doc_shelf(), '3')

    @patch.dict('main.directories', mock_directories)
    @patch('main.documents', new=mock_documents)
    @patch('builtins.input', return_value='2207 876234')
    def test_delete_doc(self, input):
        """не могу понять, почему в этом принте месте выводится оригинал списка, а не его подмена,
        хотя внутри функций из мейна всё подставляется как надо - из mock_documents"""
        print(documents)

        self.assertIn('Василий Гупкин', get_all_doc_owners_names())
        self.assertEqual(delete_doc(), ('2207 876234', True))
        self.assertNotIn('Василий Гупкин', get_all_doc_owners_names())

    @patch.dict('main.directories', mock_directories)
    @patch('main.check_document_existance', return_value=True)
    def test_move_doc_to_shelf(self, check_document_existance):
        with unittest.mock.patch('builtins.input', return_value='10006'):
            self.assertEqual(get_doc_shelf(), '2')
        with unittest.mock.patch('builtins.input', new=make_fake_input('10006', '3')):
            move_doc_to_shelf()
        with unittest.mock.patch('builtins.input', return_value='10006'):
            self.assertEqual(get_doc_shelf(), '3')

    @patch.dict('main.directories', mock_directories)
    @patch('main.documents', new=mock_documents)
    @patch('builtins.input', new=make_fake_input('test_num', 'test_type', 'test_name', '3'))
    def test_add_new_doc(self):
        self.assertEqual(add_new_doc(), '3')
        print(mock_directories)
        print(mock_documents)


if __name__ == '__main__':
    unittest.main()
