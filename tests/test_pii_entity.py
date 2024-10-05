import unittest

from pii_extraction_api.models.PiiEntity import PiiEntity


class TestPiiEntity(unittest.TestCase):
    
    def test_name_is_not_none(self):
        try:
            PiiEntity(name=None, category='jwxnw', confidence_score=0.6)
            self.fail( "Didn't raise ValueError" )
        except:
            pass

    def test_name_is_empty(self):
        try:
            PiiEntity(name='', category='jwxnw', confidence_score=0.6)
            self.fail( "Didn't raise ValueError" )
        except:
            pass

    def test_category_is_empty(self):
        try:
            PiiEntity(name='test', category='', confidence_score=0.6)
            self.fail( "Didn't raise ValueError" )
        except:
            pass
        # try:
            
        # except:
        #     self.fail("The empty category should not throw exception.")

    def test_category_is_none(self):
        try:
            PiiEntity(name='test', category=None, confidence_score=0.6)
            self.fail( "Didn't raise ValueError" )
        except:
            pass

    def test_confidence_score_less_then_0(self):
        try:
            PiiEntity(name='test', category=None, confidence_score=-0.6)
            self.fail( "Didn't raise ValueError" )
        except:
            pass
    
    def test_confidence_score_grather_then_1(self):
        try:
            PiiEntity(name='test', category="Test", confidence_score=1.01)
            self.fail( "Didn't raise ValueError" )
        except:
            pass

    def test_confidence_score_equal_to_1(self):
        try:
            PiiEntity(name='test', category="Test", confidence_score=1)    
        except:
            self.fail( "Didn't raise ValueError" )
    
    def test_confidence_score_equal_to_0(self):
        try:
            PiiEntity(name='test', category="Test", confidence_score=0.6)            
        except:
            self.fail( "Didn't raise ValueError" )
    
    def test_pass(self):
        try:
            PiiEntity(name='test', category="Test", confidence_score=0.9888)            
        except:
            self.fail( "Didn't raise ValueError" )


if __name__ == '__main__':
    unittest.main()