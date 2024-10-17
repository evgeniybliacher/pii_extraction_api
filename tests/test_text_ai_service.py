import unittest
from assertpy import assert_that

from pii_extraction_api.services.text_ai_service import TextAiActions, compose_text_action_list

from azure.ai.textanalytics import (
                RecognizeEntitiesAction,
                RecognizeLinkedEntitiesAction,
                RecognizePiiEntitiesAction,
                ExtractKeyPhrasesAction,
                AnalyzeSentimentAction,
                RecognizeCustomEntitiesAction,
                SingleLabelClassifyAction,
                MultiLabelClassifyAction,
                AnalyzeHealthcareEntitiesAction,
                ExtractiveSummaryAction,
                AbstractiveSummaryAction
    )



class TestTextAiService(unittest.TestCase):
    
    def test_pii_action_alone(self):
        actions = compose_text_action_list(TextAiActions.PII)
        (assert_that(actions)
         .is_not_none()
         .is_not_empty()
         .is_length(1)
         .contains_only(RecognizePiiEntitiesAction(domain_filter="phi")))
    
    def test_keyphrase_action_alone(self):
        actions = compose_text_action_list(TextAiActions.KEYPHRASE)
        (assert_that(actions)
         .is_not_none()
         .is_not_empty()
         .is_length(1)
         .contains_only(ExtractKeyPhrasesAction()))
        
    def test_healthcore_action_alone(self):
        actions = compose_text_action_list(TextAiActions.HEALTHCARE)
        (assert_that(actions)
        .is_not_none()
         .is_not_empty()
         .is_length(1)
         .contains_only(AnalyzeHealthcareEntitiesAction()))
        
    def test_multi_action_alone(self):
        actions = compose_text_action_list(TextAiActions.HEALTHCARE | TextAiActions.PII)
        (assert_that(actions)
            .is_not_none()
            .is_not_empty()
            .is_length(2)
            .contains(AnalyzeHealthcareEntitiesAction())
            .contains(RecognizePiiEntitiesAction(domain_filter="phi")))
        
    def test_exception_action_alone(self):
        (assert_that(compose_text_action_list)
            .raises(TypeError)
            .when_called_with(""))