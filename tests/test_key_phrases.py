import traceback
import unittest

from assertpy import assert_that
from pydantic import ValidationError

from pii_extraction_api.models.key_phrase_model import KeyPhrases


class TestKeyPhrases(unittest.TestCase):
    
    def test_incorrect_list_type(self):
        (assert_that(KeyPhrases)
            .raises(ValidationError)
            .when_called_with(key_phrases = [1,2,3]))
        
    def test_none(self):
        (assert_that(KeyPhrases)
            .raises(ValidationError)
            .when_called_with(key_phrases = None))
    
    def test_empty_list(self):
        try:
            KeyPhrases(key_phrases = [])
        except ValidationError:
            self.fail( "Empty list should not throw error" )
    
    def test_immutable(self):
        try:
            item = KeyPhrases(key_phrases = [])
            item.key_phrases = []
        except ValidationError:
            pass

    def test_correct_behavior(self):
        try:
            KeyPhrases(key_phrases = ["1","2","edcecec"])
        except ValidationError:
            self.fail( "Empty list should not throw error" )