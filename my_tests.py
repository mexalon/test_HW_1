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
    """Как поместить все патчи с подменой документов в один метод, чтобы каждый раз это не делать?"""
    @patch('main.documents', new=mock_documents)
    def test_check_document_existance(self):
        """проверка существующего документа"""
        self.assertEqual(check_document_existance('10006'), True)

    @patch('main.documents', new=mock_documents)
    def test_check_document_existance(self):
        """проверка не существующего документа"""
        self.assertEqual(check_document_existance('bad_doc'), False)

    @patch('main.documents', new=mock_documents)
    def test_get_all_doc_owners_names(self):
        exp_res = set([doc['name'] for doc in mock_documents])
        self.assertEqual(get_all_doc_owners_names(), exp_res)

    @patch.dict('main.directories', mock_directories)
    @patch('main.documents', new=mock_documents)
    def test_get_doc_owner_name(self):
        with unittest.mock.patch('builtins.input', return_value='10006'):
            self.assertEqual(get_doc_owner_name(), 'Аристарх Павлов')

    @patch.dict('main.directories', mock_directories)
    def test_get_doc_shelf_1(self):
        """неверный номер документа"""
        with unittest.mock.patch('builtins.input', return_value='not_spam'):
            self.assertEqual(get_doc_shelf(), None)

    @patch.dict('main.directories', mock_directories)
    @patch('builtins.input', return_value='10006')
    @patch('main.check_document_existance', return_value=True)
    def test_get_doc_shelf_2(self, check_document_existance, input):
        """верный номер документа"""
        self.assertEqual(get_doc_shelf(), '2')

    @patch.dict('main.directories', mock_directories)
    @patch('builtins.input', return_value='11-2')
    @patch('main.check_document_existance', return_value=True)
    def test_remove_doc_from_shelf(self, check_document_existance, input):
        remove_doc_from_shelf('11-2')
        self.assertEqual(get_doc_shelf(), None)

    @patch.dict('main.directories', mock_directories)
    @patch('builtins.input', return_value='4')
    def test_add_new_shelf_1(self, input):
        """новая полка"""
        self.assertEqual(add_new_shelf(), ('4', True))

    @patch.dict('main.directories', mock_directories)
    @patch('builtins.input', return_value='1')
    def test_add_new_shelf_2(self, input):
        """уже существующая полка"""
        self.assertEqual(add_new_shelf(), ('1', False))

    @patch.dict('main.directories', mock_directories)
    @patch('builtins.input', return_value='some_doc_number')
    @patch('main.check_document_existance', return_value=True)
    def test_append_doc_to_shelf(self, check_document_existance, input):
        append_doc_to_shelf('some_doc_number', '3')
        self.assertEqual(get_doc_shelf(), '3')

    @patch.dict('main.directories', mock_directories)
    @patch('main.documents', new=mock_documents)
    @patch('builtins.input', return_value='2207 876234')
    @patch('main.check_document_existance', return_value=True)
    def test_delete_doc(self, check_document_existance, input):
        """не могу понять, почему в этом принте выводится оригинал списка, а не его подмена,
        хотя внутри функций из мейна всё подставляется как надо - из mock_documents"""
        print(documents)  # <-----------
        self.assertEqual(delete_doc(), ('2207 876234', True))

    @patch.dict('main.directories', mock_directories)
    def test_move_doc_to_shelf(self):
        with unittest.mock.patch('builtins.input', new=make_fake_input('10006', '3')):
            move_doc_to_shelf()
        with unittest.mock.patch('builtins.input', return_value='10006'):
            self.assertEqual(get_doc_shelf(), '3')

    @patch.dict('main.directories', mock_directories)
    @patch('main.documents', new=mock_documents)
    @patch('builtins.input', new=make_fake_input('test_num', 'test_type', 'test_name', '3'))
    def test_add_new_doc(self):
        self.assertEqual(add_new_doc(), '3')


if __name__ == '__main__':
    unittest.main()
