from ollama import generate, GenerateResponse
import csv

with open('StockNames.csv', 'r') as f:
    reader = csv.reader(f)
    company_list = [row[0] for row in reader][1:]

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
    global company_list

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

    **Sentence to Analyze:**\n""" + sen + """\n**Scoring Guidelines:**
    - Strong negative words (crash, plunge, collapse, crisis) → -0.7 to -1.0
    - Moderate negative words (decline, fall, weak, concern) → -0.3 to -0.6
    - Neutral words (stable, unchanged, maintained) → -0.2 to 0.2
    - Moderate positive words (rise, growth, improvement, gain) → 0.3 to 0.6
    - Strong positive words (surge, soar, breakthrough, boom) → 0.7 to 1.0

    **Output Format (JSON array only):**
    [\{"company": "Company Name", "impact_score": 0}]

    For multiple companies:
    [{"company": "Company A", "impact_score": 0.5}, {"company": "Company B", "impact_score": -0.3}]

    **CRITICAL: 
    - ALWAYS return a JSON array (list), even for a single company
    - Return ONLY valid JSON array
    - No explanations, no additional text, no markdown formatting
    - Each company gets its own impact score
    - Match the company name to a company from this list:\n""" + str(company_list) + "**"


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

    return response.response