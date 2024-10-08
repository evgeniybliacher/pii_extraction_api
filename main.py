import os
import sys

from dotenv import dotenv_values
from pymonad.either import Either

from pii_extraction_api.api.TextAnalitycsApi import clear_pii_from_document, create_client, perform_analyze_actions, retrieve_pii_results

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

if __name__=="__main__":
    dotenv_path = os.path.join(sys.path[0], ".env")
    secrets = dotenv_values(dotenv_path)
    endpoint = secrets["AZURE_LANG_ENDPOINT"]
    key = secrets["AZURE_LANG_SECRET"]
    document = """
            Patient Profile:

    Name: Jane Doe
    Date of Birth: January 15, 1985
    Address: 123 Main St, Springfield, IL 62701
    Phone Number: 2124567890
    Email: janedoe@example.com
    Medical Information:

    Primary Diagnosis: Hypertension
            """
    clear_doc = (Either.insert(create_client(endpoint, key))
        .then(lambda x: perform_analyze_actions(x, document, "Text analys", actions=[RecognizePiiEntitiesAction(domain_filter="phi")]))
        .then(lambda x: zip([document], x))
        .then(retrieve_pii_results)
        .either(lambda l: f"Failor: {l}", lambda r: clear_pii_from_document(document,r)))

    print(clear_doc)  