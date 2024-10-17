

# import os
# import sys
# from dotenv import dotenv_values
# from fastapi import FastAPI, HTTPException

# from azure.ai.textanalytics import (
#                 RecognizeEntitiesAction,
#                 RecognizeLinkedEntitiesAction,
#                 RecognizePiiEntitiesAction,
#                 ExtractKeyPhrasesAction,
#                 AnalyzeSentimentAction,
#                 RecognizeCustomEntitiesAction,
#                 SingleLabelClassifyAction,
#                 MultiLabelClassifyAction,
#                 AnalyzeHealthcareEntitiesAction,
#                 ExtractiveSummaryAction,
#                 AbstractiveSummaryAction
#     )

# from pymonad.either import Either
# from pii_extraction_api.api.TextAnalitycsApi import clear_pii_from_document, create_client, perform_analyze_actions, retrieve_pii_results

# from enum import Flag, auto


    


# def run_mask_by_pii(document:str)->str:
#     dotenv_path = os.path.join(sys.path[0], ".env")
#     secrets = dotenv_values(dotenv_path)
#     endpoint = secrets["AZURE_LANG_ENDPOINT"]
#     key = secrets["AZURE_LANG_SECRET"]
    
#     return (Either.insert(create_client(endpoint, key))
#             .then(lambda x: perform_analyze_actions(x, document, "Text analys", actions=[RecognizePiiEntitiesAction(domain_filter="phi")]))
#             .then(lambda x: zip([document], x))
#             .then(retrieve_pii_results)
#             .either(lambda l: f"Failor: {l}", lambda r: clear_pii_from_document(document,r)))

# app = FastAPI()

# @app.get("/")
# def root():
#     return {"message": "Hello World"}

# @app.get("/piimask")
# def get_pii_masked_doc():
#     try:
#         document = """
#                 Patient Profile:

#         Name: Jane Doe
#         Date of Birth: January 15, 1985
#         Address: 123 Main St, Springfield, IL 62701
#         Phone Number: 2124567890
#         Email: janedoe@example.com
#         Medical Information:

#         Primary Diagnosis: Hypertension
#                 """
#         return run_mask_by_pii(document)
#     except Exception as ex:
#         raise HTTPException(status_code=500, detail=f"{ex}")
#     #return {"message":f"{run_mask_by_pii()}"}
    

import asyncio
from enum import Flag, auto
import os
import sys
import time
from typing import Any, Dict, List

from dotenv import dotenv_values

from pii_extraction_api.services.text_ai_service import TextAiActions, create_client, perform_analyze_action, perform_analyze_action_async, retrieve_multi_results


async def main() -> None:
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
    
    dotenv_path = os.path.join(sys.path[0], ".env")
    secrets = dotenv_values(dotenv_path)
    endpoint = secrets["AZURE_LANG_ENDPOINT"]
    key = secrets["AZURE_LANG_SECRET"]
    client = create_client(endpoint, key)
    api_request_list = [
        perform_analyze_action_async(client, document, "test", TextAiActions.PII),
        perform_analyze_action_async(client, document, "test", TextAiActions.HEALTHCARE)
    ]
    
    timer_start = time.perf_counter()

    await asyncio.gather(*api_request_list)

    timer_stop = time.perf_counter()
    print(f"Performed all requests in async... {timer_stop - timer_start:0.4f} seconds")

def main_sync() -> None:
    document = """
                 Medical History:

Presenting Symptoms: [List symptoms, e.g., increased thirst, frequent urination, fatigue, blurred vision]
Relevant Past Medical History: [Any previous conditions, surgeries, or treatments]
Family History of Diabetes: [Yes/No; details if applicable]
Physical Examination:

Vital Signs:

Blood Pressure: [e.g., 120/80 mmHg]
Heart Rate: [e.g., 75 bpm]
Weight: [e.g., 180 lbs]
Height: [e.g., 5'8"]
General Appearance: [Describe any relevant observations]

Laboratory Results:

Fasting Blood Glucose: [e.g., 130 mg/dL]
Hemoglobin A1c: [e.g., 7.2%]
Oral Glucose Tolerance Test (if applicable): [Results]
Other Relevant Tests: [e.g., lipid profile, kidney function tests]
Diagnosis:

Primary Diagnosis: Type 1 / Type 2 Diabetes Mellitus (specify)
ICD-10 Code: [e.g., E11 for Type 2 Diabetes]
Recommendations:

Dietary Modifications: [e.g., low-carb diet, meal planning]
Exercise Recommendations: [e.g., 30 minutes of moderate exercise daily]
Medication: [e.g., Metformin, insulin therapy]
Follow-up Appointments: [e.g., schedule in 3 months]
Patient Education:

Discussed the nature of diabetes, management strategies, and the importance of regular monitoring of blood glucose levels.
                """
    
    dotenv_path = os.path.join(sys.path[0], ".env")
    secrets = dotenv_values(dotenv_path)
    endpoint = secrets["AZURE_LANG_ENDPOINT"]
    key = secrets["AZURE_LANG_SECRET"]
    client = create_client(endpoint, key)
    
    timer_start = time.perf_counter()

    result = perform_analyze_action(client, document, "test", TextAiActions.PII|TextAiActions.KEYPHRASE)
    dict_result = retrieve_multi_results(result)

    if (TextAiActions.PII in dict_result):
        print("The PII results have been detected")
    if(TextAiActions.KEYPHRASE in dict_result):
        print("The Key phrase result has been detected")
        print(dict_result[TextAiActions.KEYPHRASE])


    timer_stop = time.perf_counter()
    print(f"Performed all requests in sync... {timer_stop - timer_start:0.4f} seconds")
    

if (__name__=="__main__"):
    #asyncio.run(main())
    main_sync()
    # class TextAiActions(Flag):
    #     NONE = 0
    #     PII = auto()
    #     KEYPHRASE = auto()
    #     HEALTHCARE = auto()

    # from typing import TypedDict

    # TextAiResult = TypedDict('TextAiResult', {'kind': TextAiActions, 'results': List[Any]})
    # data: TextAiResult = TextAiResult()

    # data[TextAiActions.KEYPHRASE] = [1,2,3,4]
    # data[TextAiActions.PII] = ["1","2"]

    # print(data[TextAiActions.PII].copy())

    # print(data[TextAiActions.KEYPHRASE])
    # print(data[TextAiActions.PII])