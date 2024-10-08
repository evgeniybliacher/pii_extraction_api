import os
import sys
from dotenv import dotenv_values

from typing import Any, List, Union
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient
from pymonad.either import Either

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

from pii_extraction_api.models.PiiEntity import PiiEntity



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


def create_client(endpoint: str, key: str)->TextAnalyticsClient:
    return TextAnalyticsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(key),
    )

def perform_analyze_actions(text_analytics_client: TextAnalyticsClient, documents: List[str], name: str, actions: List[TextAnalyticsActions])->Any:
    poller = text_analytics_client.begin_analyze_actions(
        documents,
        display_name=name,
        actions=actions
    )
    return poller.result()

def perform_analyze_actions(text_analytics_client: TextAnalyticsClient, document: str, name: str, actions: List[TextAnalyticsActions])->Any:
    poller = text_analytics_client.begin_analyze_actions(
        [document],
        display_name=name,
        actions=actions
    )
    return poller.result()

def retrieve_pii_results(result: Any)->List[PiiEntity]:
    li:List[PiiEntity] = []
    for doc,res in result:
        for r in res:
            if r.kind == "PiiEntityRecognition":
                #print("Results of Recognize PII Entities action:")
                for pii_entity in r.entities:
                    li.append(PiiEntity(name=pii_entity.text, category=pii_entity.category, confidence_score=pii_entity.confidence_score))
    return li

def clear_pii_from_document(document:str, pii_entities: List[PiiEntity])->str:
    doc = document
    for replace_entity in pii_entities:
        doc = doc.replace(replace_entity.name, f"[masked {replace_entity.category}]")
    return doc

def validate_result_kind(result: Any, expected_kind: str)->bool:
    try:
        if result.kind == expected_kind:
            return result
        raise AssertionError(f"The kind of result is {result.kind} while kind {expected_kind} is expected")
    except:
        raise AssertionError(f"Something wrong with result instance.")
    
def validate_result_kind(result: Any, expected_kind: str)->bool:
    try:
        if result.kind == expected_kind:
            return result
        raise AssertionError(f"The kind of result is {result.kind} while kind {expected_kind} is expected")
    except:
        raise AssertionError(f"Something wrong with result instance.")
     
    
    # v = create_client(endpoint, key)
    # c = perform_analyze_actions(v, document, "Text analys", actions=[RecognizePiiEntitiesAction(domain_filter="phi")])
    # result_entities = List[PiiEntity]
    # for doc,res in cross_res:
    #     for r in res:
    #         if r.kind == "PiiEntityRecognition":
    #             print("Results of Recognize PII Entities action:")
    #             for pii_entity in r.entities:
    #                 print(f"......Entity: {pii_entity.text}")
    #                 print(f".........Category: {pii_entity.category}")
    #                 print(f".........Confidence Score: {pii_entity.confidence_score}")
    #                 doc = doc.replace(pii_entity.text, f"[masked due {pii_entity.category}]")
    #             print (f"Masked document: {doc}")


