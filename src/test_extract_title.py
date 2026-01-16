import unittest
from generate_page import extract_title

class TestExtractTitle(unittest.TestCase):
    def test_clean_heading(self):
        md = '# Heading 1'
        extracted_title = extract_title(md)
        self.assertEqual(extracted_title, 'Heading 1')

    def test_dirty_heading(self):
        md = '  #   Heading 1     '
        extracted_title = extract_title(md)
        self.assertEqual(extracted_title, 'Heading 1')

    def buried_heading(self):
        md = '''
This is a ploy
So is this
# Headng 1
Gotta ignore this too
'''
        extracted_title = extract_title(md)
        self.assertEqual(extracted_title, 'Heading 1')