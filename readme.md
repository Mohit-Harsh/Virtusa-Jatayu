# Credit Score

### What is Credit Score?

A credit score is a numerical representation of a person's creditworthiness, typically ranging from 300 to 850. It is used by banks, lenders, and financial institutions to assess the risk of lending money or extending credit to an individual. A higher credit score indicates a lower risk, making it easier to qualify for loans with better interest rates.

### Factors That Affect Credit Score

#### 1. Payment History (35%)

- Timely payments on credit cards, loans, and bills improve credit scores.
- Late payments, defaults, or bankruptcies negatively impact the score.

#### 2. Credit Utilization Ratio (30%)

- It measures how much of the available credit is being used.
- Keeping utilization below 30% of the total credit limit helps maintain a good score.

#### 3. Length of Credit History (15%)

- A longer credit history shows responsible credit behavior over time.
- The age of the oldest and newest credit accounts matters.

#### 4. Credit Mix (10%)

- Having a mix of different types of credit (credit cards, home loans, personal loans, etc.) can positively impact the score.
- Relying too much on one type of credit may not be beneficial.

#### 5. New Credit Inquiries (10%)

- Applying for multiple loans or credit cards within a short time can lower the score.
- Hard inquiries (lender checks for loan approval) negatively affect credit scores, whereas soft inquiries (self-checks) do not.

#### 6. Outstanding Debt

- Higher existing debt can reduce the score as it indicates a higher risk to lenders.
- Paying down debt regularly can improve the score.

#### 7. Public Records

- Bankruptcy, tax liens, or legal judgments can significantly impact the credit score.
Such records can stay on the credit report for several years.

# Interest Slabs

### **What Are Interest Slabs in Banks?**  

**Interest slabs** refer to the structured interest rate categories used by banks to determine the applicable rate for different financial products such as **Fixed Deposits (FDs), Savings Accounts, and Loans**. Instead of a **flat rate**, banks apply different interest rates based on the amount, tenure, or category of the deposit or loan.

### **Types of Interest Slabs in Banking**  

#### **1. Fixed Deposit (FD) Interest Slabs**  
Banks offer different interest rates based on the deposit **tenure** and **amount**:  

✅ **Tenure-Based Slabs:**  
- Short-term (7 days to 1 year) – Lower interest rate  
- Medium-term (1 to 5 years) – Higher interest rate  
- Long-term (5+ years) – Slightly lower rate due to long lock-in  

✅ **Amount-Based Slabs:**  
- Deposits below ₹2 lakh – Standard rates  
- Deposits ₹2 lakh - ₹5 crore – Special rates for bulk deposits  
- Deposits above ₹5 crore – Negotiable rates  

✅ **Senior Citizen Slabs:**  
- Additional 0.25% - 0.75% higher interest for senior citizens  

✅ **NRE/NRO FD Slabs:**  
- Different rates for Non-Resident External (NRE) and Non-Resident Ordinary (NRO) accounts  

#### **2. Savings Account Interest Slabs**  
Banks often categorize savings interest rates based on account balance:  

- Up to ₹1 lakh – 2.5% to 3.5% interest  
- ₹1 lakh - ₹5 lakh – 3.5% to 4% interest  
- ₹5 lakh - ₹10 lakh – 4% to 5% interest  
- Above ₹10 lakh – 5% to 6% interest  

Some banks also provide **monthly, quarterly, or yearly interest payouts**.  

#### **3. Loan Interest Slabs (Home Loans, Personal Loans, etc.)**  
Loans are structured based on **loan amount, tenure, and borrower profile**:  

✅ **Home Loan Slabs (Example):**  
- Up to ₹30 lakh – 8.0% interest  
- ₹30 lakh - ₹75 lakh – 8.5% interest  
- Above ₹75 lakh – 9.0% interest  

✅ **Credit Score-Based Slabs:**  
- Credit score **750+** – Lower interest (e.g., 7.5%)  
- Credit score **600-750** – Medium interest (e.g., 8.5%)  
- Credit score **Below 600** – Higher risk, higher interest (e.g., 10% or more)  

✅ **Loan Tenure-Based Slabs:**  
- Shorter tenure (5-10 years) – Lower interest  
- Longer tenure (20-30 years) – Higher interest  

✅ **Salary & Occupation-Based Slabs:**  
- Salaried professionals – Lower rates  
- Self-employed – Slightly higher rates due to risk factors  


# Solution

We will calculate Interest Rate using Credit Score and Interest Slabs. Based on the Credit Score the Customer might get a Discount or Penalty on the Interest Slab.

### Approach 1: 

- Both Credit Score and Interest Slabs are **Dynamic** (changing w.r.t to Economic Tredns and Bank Health and Performance).

### Approach 2: 

- Credit Score is **Dynamic** and Interest Slabs are **Static**. 
- The final calculated Interest Rate will then be scaled w.r.t **Economic Trends** and **Bank Health and Performance**. 