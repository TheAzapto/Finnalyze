from ollama import generate, GenerateResponse
from thefuzz import fuzz
import pandas as pd
import json

def fuzzy_match(LLM_json_output: str) -> str|None: 

    name = LLM_json_output['company']
    impact_score = LLM_json_output['impact_score']

    print(name)
    print(impact_score)


    with open('backend\StockNames.csv', 'r') as f:
        reader = pd.read_csv(f)
        company_list = reader['Names'].tolist()

        print(company_list[0])



    for company in company_list:
        ratio_partial = fuzz.partial_ratio(name, company)
        if ratio_partial > 92:
            print(ratio_partial)
            return f'{{"company": "{company}", "impact_score": {impact_score}}}'

            
        
        ratio_full = fuzz.ratio(name, company)
        if ratio_full > 92:
            print(ratio_full)
            return f'{{"company": "{company}", "impact_score": {impact_score}}}'

        ratio_token = fuzz.token_sort_ratio(name, company)
        if ratio_token > 92:
            print(ratio_token)
            return f'{{"company": "{company}", "impact_score": {impact_score}}}'
        
    return None

def Summarize(msg:str) -> str:
    prompt=f"""You are a financial text analysis expert. Your task is to analyze the provided article and generate a single summary sentence for sentiment analysis.

    **Instructions:**
    1. Read and understand the article thoroughly
    2. Identify the main financial topics, entities, and events discussed
    3. Generate ONE simple, clear sentence (15-25 words) that summarizes the article's core message
    4. Output ONLY the sentence - no labels, no explanations, no additional text

    **Article:**
    {msg}

    **Guidelines:**
    - Focus on financial terminology, company names, market movements, and economic indicators
    - The sentence must be grammatically correct and self-contained
    - Include clear sentiment indicators (positive, negative, or neutral words)
    - Avoid jargon; keep it accessible
    - Be objective and accurate to the source material

    **CRITICAL: Return ONLY the summary sentence. Do not include "Summary Sentence:" or any other labels or formatting.**"""

    response: GenerateResponse = generate(model="hf.co/us4/fin-llama3.1-8b:Q5_K_M",
    prompt=prompt,
    options={
        'temperature': 0.2,
        'top_p': 0.85,
        'top_k': 30,
        'num_predict': 60,
        'repeat_penalty': 1.1,
        'num_ctx': 4096,
        'num_thread': 16,
    })

    return response.response

def Evaluate(sen:str) -> str:

    prompt=f"""You are a financial sentiment analysis expert. Your task is to evaluate the provided sentence and assign precise impact scores.

    **Instructions:**
    1. Analyze the sentiment and financial implications of the sentence
    2. Identify ALL companies or entities mentioned in the sentence
    3. For EACH company, assign an impact score between -1.0 and 1.0 where:
    - -1.0 = extremely negative impact
    - -0.5 = moderately negative impact
    - 0.0 = neutral or no clear impact
    - 0.5 = moderately positive impact
    - 1.0 = extremely positive impact
    4. Consider market impact, investor sentiment, and economic implications for each company
    5. Use decimal precision (e.g., -0.73, 0.42, 0.15)

    **Sentence to Analyze:**
    {sen}

    **Scoring Guidelines:**
    - Strong negative words (crash, plunge, collapse, crisis) → -0.7 to -1.0
    - Moderate negative words (decline, fall, weak, concern) → -0.3 to -0.6
    - Neutral words (stable, unchanged, maintained) → -0.2 to 0.2
    - Moderate positive words (rise, growth, improvement, gain) → 0.3 to 0.6
    - Strong positive words (surge, soar, breakthrough, boom) → 0.7 to 1.0

    **Output Format (JSON array only):**
    [{{"company": "Company Name", "impact_score": 0}}]
    For multiple companies:
    [{{"company": "Company A", "impact_score": 0.5}}, {{"company": "Company B", "impact_score": -0.3}}]

    **CRITICAL:**
    - ALWAYS return a JSON array (list), even for a single company
    - Return ONLY valid JSON array
    - No explanations, no additional text, no markdown formatting
    - Each company gets its own impact score**""" 


    response: GenerateResponse = generate(model="hf.co/us4/fin-llama3.1-8b:Q5_K_M", 
    prompt=prompt,
    options={
    'temperature': 0.1,
    'top_p': 0.9,
    'top_k': 40,
    'num_predict': 300,
    'repeat_penalty': 1.0,
    'num_ctx': 2048,
    'num_thread': 16,
    })

    validated_list = []

    print(response.response)

    for token in json.loads(str(response.response).replace("'", '"')):
        print(token)
        validated_string = fuzzy_match(token)

        print(validated_string)
        if validated_string:
            validated_list.append(json.loads(validated_string))
        
    print(validated_list)

    return str(validated_list).replace("'", '"')
