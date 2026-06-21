import os
import sys
from dotenv import load_dotenv
import gdown
from langchain_experimental.agents import create_pandas_dataframe_agent
from langchain_openai import ChatOpenAI
import pandas as pd

load_dotenv()  # Load environment variables from .env file

# ==========================================
#  PART 1: AUTOMATIC FILE DOWNLOADER
# ==========================================

files_to_download = {
    "saas_docs.csv":         "https://drive.google.com/file/d/1RElOhN7bYsDAJUNQhYyqM7IzX-Xo6myq/view?usp=sharing",
    "credit_card_terms.csv": "https://drive.google.com/file/d/1_giivc_B0urOKpct0XY2yVZuxW3Eenuf/view?usp=sharing",
    "hospital_policy.csv":   "https://drive.google.com/file/d/1pL7OnDhnmz9pteIpBJ12gu2_ixrc2hPm/view?usp=sharing",
    "ecommerce_faqs.csv":    "https://drive.google.com/file/d/1O4fTjsLFbz55oOiwJUwLwZryO5OSSF6p/view?usp=sharing"
}

print("--- Downloading Files from Google Drive ---")
for filename, url in files_to_download.items():
    if not os.path.exists(filename):
        gdown.download(url, filename, quiet=False)
        print(f"Downloaded: {filename}")
    else:
        print(f"Skipped: {filename} (Already exists)")
print("--- Download Complete ---\n")


# ==========================================
#  PART 2: AI AGENT SETUP (MULTI-FILE)
# ==========================================

# 1. SETUP: Get API Key Securely
api_key = os.getenv("OPENAI_APIKEY")
if not api_key:
    raise ValueError("OPENAI_APIKEY not found in environment variables. Please set it in the .env file.")
print("API Key loaded successfully.")

# 2. LOAD ALL CSVs INTO A LIST
dataframes = []
loaded_names = []

try:
    for filename in files_to_download.keys():
        df = pd.read_csv(filename)
        dataframes.append(df)
        loaded_names.append(filename)
        print(f"Loaded: {filename} (Shape: {df.shape}) ({len(df)} rows)")
except Exception as e:
    print(f"Error loading {filename}: {e}")
    sys.exit()

# 3. DEFINE THE RULES
sys_prompt = """
You are a smart data assistant that answers questions based on the multiple CSV files
- When asked a question, determine which DataFrame is most relevant.
- Answer generic information when asked
- Answer in plain English.
"""

# 4. INITIALIZE THE AGENT WITH MULTIPLE DFS
try:
    llm = ChatOpenAI(
        temperature=0.5,
        model="gpt-4o-mini",
        openai_api_key=api_key
    )

    # --- KEY CHANGE: We pass the LIST 'dataframes' instead of a single 'df' ---
    agent = create_pandas_dataframe_agent(
       llm,
        dataframes,
        verbose=True,
        agent_type="openai-tools", # 'openai-tools' is often more stable than 'functions'
        include_df_in_prompt=True, # Ensures the agent sees column names
        allow_dangerous_code=True  # Required for DataFrame analysis; only use with trusted data and in controlled environments

    )

    print("\nAI Agent is ready! You can ask questions across ALL files.")
    print("Example: 'What is the visiting hour in the hospital?' or 'What is the API limit?'")
    
except Exception as e:
    print(f"Error initializing agent: {e}")
    sys.exit()


# ==========================================
#  PART 3: CHAT LOOP
# ==========================================

print("\nType 'exit' or 'quit' to stop conversation.\n")

while True:
    user_input = input("You: ")

    if user_input.lower() in ["exit", "quit", "q"]:
        print("Goodbye!")
        break

    if not user_input:
        continue

    final_query = sys_prompt + "\n\nQuestion: " + user_input
    print("AI is thinking...", final_query)

    try:
        response = agent.invoke(final_query)['output']
        print(f"AI: {response}\n" + "-"*30)
    except Exception as e:
        print(f"An error occurred: {e}")
