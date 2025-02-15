import streamlit as st
from openai import OpenAI
import  json
import asyncio
import psycopg2
import pandas as pd
from collections import defaultdict
from pydantic import BaseModel

client = OpenAI()

conn = psycopg2.connect( 
    database="Bank", user='postgres', 
    password='12345', host='localhost', port='5432'
) 

conn.autocommit = True
conn.set_session(readonly=True)
cursor = conn.cursor()

class SQL_OUTPUT(BaseModel):

    sql: list[str]

def execute(sql):

    try:
        
        cursor.execute(sql) 
        results = cursor.fetchall()
        headers = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(columns=headers)
        for r in results:
            df = pd.concat([df,pd.DataFrame(data=[list(r)],columns=df.columns)],axis=0)
        return df
    
    except psycopg2.ProgrammingError as err:

        prompt = f"query: {sql}\nError: {err}\nRewrite the SQL query and fix the errors."
        print(prompt)
        res = generate(prompt)
        res = res['sql'][0]
        return execute(res)

    except Exception as err:

        res = pd.DataFrame([['An unexpected error has occured while fetching the data.']],columns=['Error'])
        return res

def generate(query):

    prompt_template = """You are a SQL Database Assistant. Your task is to write SQL queries to retrieve required information based on user's query. All the information about tables is provided in the database section below.

            <DATABASE>

            BEGIN;


            TABLE customer
            (
                cid uuid NOT NULL,
                name character varying(30) COLLATE pg_catalog."default" NOT NULL,
                credit_score integer NOT NULL DEFAULT 450,
                age integer NOT NULL,
                income integer NOT NULL,
                married boolean NOT NULL,
                gender character varying(10) COLLATE pg_catalog."default" NOT NULL,
                CONSTRAINT "Customer_pkey" PRIMARY KEY (cid)
            );

            TABLE home_loan
            (
                hid uuid NOT NULL,
                loan_amount integer NOT NULL,
                interest_rate integer NOT NULL,
                tenure integer NOT NULL,
                origin_date date,
                disbursement_date date,
                cid uuid NOT NULL,
                CONSTRAINT "HomeLoan_pkey" PRIMARY KEY (hid),
                CONSTRAINT cid FOREIGN KEY (cid) REFERENCES public.customer (cid)
            );

            TABLE credit_history
            (
                chid uuid NOT NULL,
                credit_accounts integer DEFAULT 0,
                ontime_payments integer,
                missed_payments integer DEFAULT 0,
                credit_util_ratio integer,
                loan_defaults integer DEFAULT 0,
                late_payments integer DEFAULT 0,
                credit_account_age integer DEFAULT 0,
                cid uuid NOT NULL,
                CONSTRAINT credit_history_pkey PRIMARY KEY (chid),
                CONSTRAINT cid FOREIGN KEY (cid) REFERENCES public.customer (cid)
            );

            TABLE debt_history
            (
                dhid uuid NOT NULL,
                total_loans integer DEFAULT 0,
                total_loan_amount integer DEFAULT 0,
                loan_rejections integer DEFAULT 0,
                debt_income_ratio integer DEFAULT 0,
                secured_loans integer,
                unsecured_loans integer,
                emi_bounces integer DEFAULT 0,
                cid uuid NOT NULL,
                CONSTRAINT debt_history_pkey PRIMARY KEY (dhid),
                CONSTRAINT cid FOREIGN KEY (cid) REFERENCES public.customer (cid)
            );

            TABLE finance_history
            (
                fhid uuid NOT NULL,
                monthly_balance integer,
                monthly_emi integer,
                spending_income_ratio integer,
                cid uuid NOT NULL,
                CONSTRAINT finance_history_pkey PRIMARY KEY (fhid),
                CONSTRAINT cid FOREIGN KEY (cid) REFERENCES public.customer (cid)
            );

            </DATABASE>

            LIMIT the results to atmost 20 records.

            Give your response only in the following JSON format:

            {
                "sql" : [list of required sql queries]
            }
            """

    completion = client.beta.chat.completions.parse(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content": prompt_template
        },
        {
            "role": "user",
            "content": f"user: {query}"
        },
    ],response_format=SQL_OUTPUT)

    return json.loads(completion.choices[0].message.content)

def getInsights(query,context):

    print("context: ",context)

    prompt_template = """You are a Banking AI assistant. You have to answer user queries by utilizing the tools provided to you.

                ## Tools

                ### database_tool

                Use this tool to get the following information from SQL database:
                
                - Customer's Personal & Demographic Features, Credit History & Behavior, Loan & Debt-Related Features, Financial Transactions & Spending Behavior. 
                - Home Loan details
                
                """ + f""" 
                <context>

                {context}

                </context>"""+"""

                <instructions>
                
                - Refer the context for information before answering the query.

                - Response Format:

                    1. You have all the information to answer the query:

                    {"response" : "Final Answer"}

                    2. You want to fetch some information from the database:

                    {"fetch" : "Description of the information you want from the database"}

                - Don't answer any queries that are not related to the bank and finance.

                </instructions>
            """

    completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {
            "role": "system", 
            "content":prompt_template
        },
        {
            "role": "user",
            "content": f"user: {query}"
        }
    ])

    response = json.loads(completion.choices[0].message.content)   

    keys = response.keys()

    if('fetch' in keys):

        database_queries = generate(response['fetch'])

        st.chat_message("assistant").write("Fetching Data ...")
        st.session_state.messages.append({"role": "assistant", "content":"Fetching Data ..."})

        data = f"Assistant: {response['fetch']}\nFetched Results:\n"

        for q in database_queries['sql']:

            res =  execute(q)
            st.dataframe(res)
            st.session_state['messages'].append({"role":"dataframe","content":res})
            data += res.to_string(index=False) + "\n"

        prompt_template2 = f"""You are a Banking AI Assistant. Answer the user queries using the context and data provided to you.
        <context>
            {context}

            {data}
        </context>
        """

        res = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
            {
                "role": "system", 
                "content":prompt_template2
            },
            {
                "role": "user",
                "content": f"user: {query}"
            }
        ])

        res = res.choices[0].message.content

        st.chat_message("assistant").write(res)
        st.session_state.messages.append({"role": "assistant", "content":res})
        while(len(st.session_state['memory'])>=5):
            st.session_state['memory'].pop(0)
        st.session_state['memory'].append(f"user:{query}\nassistant:{res}\n")

    if('response' in keys):

        st.chat_message("assistant").write(response['response'])
        st.session_state.messages.append({"role": "assistant", "content": response['response']})
        while(len(st.session_state['memory'])>=5):
            st.session_state['memory'].pop(0)
        st.session_state['memory'].append(f"user:{query}\nassistant:{response['response']}\n")

    if('ask' in keys):

        st.chat_message("assistant").write(response['ask'])
        st.session_state.messages.append({"role": "assistant", "content": response['ask']})
        st.session_state['memory'].append(f"user:{query}\nassistant:{response['ask']}\n")

    return

st.title("💬 Chatbot")

if "memory" not in st.session_state:

    st.session_state['memory'] = []

if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]

for msg in st.session_state.messages:

    if(msg['role'] == 'dataframe'):
        st.dataframe(msg['content'])
    else:
        st.chat_message(msg["role"]).write(msg["content"])

if prompt := st.chat_input():

    client = OpenAI()
    st.chat_message("user").write(prompt)
    getInsights(prompt,"\n".join(st.session_state['memory']))
    