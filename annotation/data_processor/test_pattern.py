# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))
import unittest
from annotation.data_processor.extract_text import Pattern


class TestPattern(unittest.TestCase):

    def test_category(self):
        self.assertTrue(Pattern.get_category("(1) 業績(連結)"))
        self.assertTrue(Pattern.get_category("（１）当期（平成28年４月１日から平成29年３月31日）の概況"))
        self.assertTrue(Pattern.get_category("(2)連結業績"))
        self.assertTrue(Pattern.get_category("(1) 業績"))
        self.assertTrue(Pattern.get_category("(1) 業績\n　当連結会計年度における連結売上高合計"))

        self.assertTrue(Pattern.get_category("(2) キャッシュ・フロー"))
        self.assertTrue(Pattern.get_category("(2) キャッシュ・フロ－の状況"))
                

if __name__ == "__main__":
    unittest.main()
