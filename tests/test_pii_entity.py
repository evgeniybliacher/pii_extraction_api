import traceback
import unittest

from assertpy import assert_that
from pydantic import ValidationError

from pii_extraction_api.models.pii_models import PiiEntity


class TestPiiEntity(unittest.TestCase):
    
    def test_entity_is_none(self):
        (assert_that(PiiEntity)
            .raises(ValidationError)
            .when_called_with(entity=None, category='jwxnw', confidence_score=0.6))

    def test_entity_is_empty(self):
        (assert_that(PiiEntity)
            .raises(ValidationError)
            .when_called_with(entity="", category='jwxnw', confidence_score=0.6))

    def test_category_is_empty(self):
        (assert_that(PiiEntity)
            .raises(ValidationError)
            .when_called_with(entity="test", category='', confidence_score=0.6))

    def test_category_is_none(self):
        (assert_that(PiiEntity)
            .raises(ValidationError)
            .when_called_with(entity="test", category=None, confidence_score=0.6))

    def test_confidence_score_less_then_0(self):
        (assert_that(PiiEntity)
            .raises(ValidationError)
            .when_called_with(entity="test", category='jwxnw', confidence_score=-0.6))
    
    def test_confidence_score_grather_then_1(self):
        (assert_that(PiiEntity)
            .raises(ValidationError)
            .when_called_with(entity="test", category='jwxnw', confidence_score=1.01))

    def test_confidence_score_equal_to_1(self):
        try:
            PiiEntity(entity='test', category="Test", confidence_score=1.0)
        except :
            traceback.print_exc()
            self.fail( "Throw exception when we do not expect it" )
    
    def test_confidence_score_equal_to_0(self):
        try:
            PiiEntity(entity='test', category="Test", confidence_score=0.0)
        except :
            traceback.print_exc()
            self.fail( "Throw exception when we do not expect it" )
            
    
    def test_pass(self):
        try:
            PiiEntity(entity='test', category="Test", confidence_score=0.9888)            
        except :
            traceback.print_exc()
            self.fail( "Throw exception when we do not expect it" )

    def test_immutable(self):
        try:
            entity = PiiEntity(entity='test', category="Test", confidence_score=0.9888)            
            entity.entity = 'ccc'
            self.fail( "Validation error was not thrown" )
        except ValidationError:
            pass

    def test_extra_fields_forbid(self):
        (assert_that(PiiEntity)
            .raises(ValidationError)
            .when_called_with(entity="test", category='jwxnw', confidence_score=1.01, nor_text="text"))


if __name__ == '__main__':
    unittest.main()