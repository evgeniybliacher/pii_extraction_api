from typing import Any, Dict, List, Union
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from enum import Flag, auto

import asyncio

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

from pii_extraction_api.models.key_phrase_model import KeyPhrases
from pii_extraction_api.models.pii_models import PiiEntity



type TextAnalyticsActions = Union[
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
                AbstractiveSummaryAction,
            ]

class TextAiActions(Flag):
    NONE = 0
    PII = auto()
    KEYPHRASE = auto()
    HEALTHCARE = auto()

from typing import TypedDict

TextAiResult = TypedDict('TextAiResult', {'kind': TextAiActions, 'results': List[Any]})

def compose_text_action_list(action_flags: TextAiActions)->List[TextAnalyticsActions]:
    result:List[TextAiActions] = []
    inner_actions = action_flags
    while(inner_actions != TextAiActions.NONE):
        match inner_actions:
            case inner_actions if TextAiActions.PII in inner_actions:
                result.append(RecognizePiiEntitiesAction(domain_filter="phi"))
                inner_actions &= ~TextAiActions.PII
            case inner_actions if TextAiActions.KEYPHRASE in inner_actions:
                result.append(ExtractKeyPhrasesAction())
                inner_actions &= ~TextAiActions.KEYPHRASE
            case inner_actions if TextAiActions.HEALTHCARE in inner_actions:
                result.append(AnalyzeHealthcareEntitiesAction())
                inner_actions &= ~TextAiActions.HEALTHCARE
            case _:
                raise ValueError("Unrecognized action required.")
    return result
        

def create_client(endpoint: str, key: str)->TextAnalyticsClient:
    return TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

def perform_analyze_actions(text_analytics_client: TextAnalyticsClient, documents: List[str], name: str, actions: TextAiActions)->Any:
    poller = text_analytics_client.begin_analyze_actions(
        documents,
        display_name=name,
        actions=compose_text_action_list(actions)
    )
    return poller.result()

async def perform_analyze_actions_async(text_analytics_client: TextAnalyticsClient, documents: List[str], name: str, actions: TextAiActions)->Any:
    return  perform_analyze_actions(text_analytics_client, documents, name, actions)

def perform_analyze_action(text_analytics_client: TextAnalyticsClient, document: str, name: str, action: TextAiActions)->Any:
    return perform_analyze_actions(text_analytics_client, [document], name, action)

async def perform_analyze_action_async(text_analytics_client: TextAnalyticsClient, document: str, name: str, action: TextAiActions)->Any:
    return  perform_analyze_actions(text_analytics_client, [document], name, action)


def retrieve_multi_results(ai_result: Any)->TextAiResult:
    result:TextAiResult = TextAiResult()
    for res in ai_result:
        for r in res:
            if r.kind == "PiiEntityRecognition":
                pii_list: List[PiiEntity] = []
                for pii_entity in r.entities:
                    pii_list.append(PiiEntity(entity=pii_entity.text, category=pii_entity.category, confidence_score=pii_entity.confidence_score))
                result[TextAiActions.PII] = pii_list
            elif r.kind == "KeyPhraseExtraction":
                result[TextAiActions.KEYPHRASE] = KeyPhrases(key_phrases = r.key_phrases.copy()) 
            
    return result

# def clear_pii_from_document(document:str, pii_entities: List[PiiEntity])->str:
#     doc = document
#     for replace_entity in pii_entities:
#         doc = doc.replace(replace_entity.name, f"[masked {replace_entity.category}]")
#     return doc

def ensure_result_kind(result: Any, expected_kind: str, is_raised: bool = True)-> bool:
    try:
        if result.kind == expected_kind:
            return True
        if (is_raised):
            raise AssertionError(f"The kind of result is {result.kind} while kind {expected_kind} is expected")
    except:
        raise AssertionError(f"Something wrong with result instance.")
    
# def validate_result_kind(result: Any, expected_kind: str)->bool:
#     try:
#         if result.kind == expected_kind:
#             return result
#         raise AssertionError(f"The kind of result is {result.kind} while kind {expected_kind} is expected")
#     except:
#         raise AssertionError(f"Something wrong with result instance.")
     
    
#     # v = create_client(endpoint, key)
#     # c = perform_analyze_actions(v, document, "Text analys", actions=[RecognizePiiEntitiesAction(domain_filter="phi")])
#     # result_entities = List[PiiEntity]
#     # for doc,res in cross_res:
#     #     for r in res:
#     #         if r.kind == "PiiEntityRecognition":
#     #             print("Results of Recognize PII Entities action:")
#     #             for pii_entity in r.entities:
#     #                 print(f"......Entity: {pii_entity.text}")
#     #                 print(f".........Category: {pii_entity.category}")
#     #                 print(f".........Confidence Score: {pii_entity.confidence_score}")
#     #                 doc = doc.replace(pii_entity.text, f"[masked due {pii_entity.category}]")
#     #             print (f"Masked document: {doc}")


