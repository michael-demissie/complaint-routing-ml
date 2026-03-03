# Departmental Classification Model – Feature Selection Explanation

## Model Goal

The goal of this model is to send each complaint to the correct CFPB department.

Only information available at the time the complaint is first submitted is used.  
Any column that is added later, used for tracking, or not directly related to department type is removed.

---

## Target

**Product**  
This shows which department handles the complaint.  
It is what the model is trying to predict.

---

## Feature

**Consumer complaint narrative**  
This is the text written by the customer.  
It explains the problem and is the main information used to decide the department.

---

## Removed Columns

These columns were removed because they are either added later, administrative, or could leak information:

- **Date received** – Only shows when the complaint was submitted. It does not determine the department.
- **Sub-product** – Very similar to Product. Causes information leakage.
- **Issue** – Added by CFPB after reviewing the complaint.
- **Sub-issue** – A more detailed label added by CFPB.
- **Company public response** – Added after the company replies.
- **Company** – The company name is not needed to decide the department.
- **State** – Location is not used in this model.
- **ZIP code** – Detailed location not needed.
- **Tags** – Special labels like Servicemember or Older American; not needed for department decision.
- **Consumer consent provided?** – Administrative information.
- **Submitted via** – Shows how the complaint was sent (web, phone, etc.). Does not determine department.
- **Date sent to company** – Happens after routing.
- **Company response to consumer** – Added after company action.
- **Timely response?** – Shows if the company replied on time.
- **Consumer disputed?** – Shows if the consumer disagreed later.
- **Complaint ID** – Just a tracking number.

---

## Final Model Setup

- **Target:** Product  
- **Feature:** Consumer complaint narrative  

This setup keeps the model simple and realistic by using only the complaint text to decide the correct department.

---

# Target Category Cleaning

## Credit Reporting Categories

### 1. Credit reporting or other personal consumer reports  
This category includes complaints about problems with a person’s credit report or credit score, such as:
- Incorrect information  
- Fraud accounts  
- Errors not properly fixed  

Credit bureaus like Experian, Equifax, and TransUnion collect information from banks, lenders, credit card companies, and collection agencies.

---

### 2. Credit reporting, credit repair services, or other personal consumer reports  
This is a newer, expanded label.  
Credit repair services are companies that claim they can improve your credit score or remove negative items from your credit report.

---

## #1 Credit Reporting Department

We merge the two categories above into one **Credit Reporting** department.  
We also include complaints labeled simply as credit reporting.

### Two-Level Prediction Strategy

- First, predict the broad department: **Credit Reporting**
- Then, for complaints predicted as Credit Reporting, run a second model to split into sub-types:

1. Credit report errors  
2. Identity theft and fraud accounts  
3. Dispute process problems  
4. Mixed file errors  
5. Credit repair service problems  
6. Background and tenant screening report issues  
7. Credit score problems  
8. Credit freeze and fraud alert issues  

---

## #2 Debt Collection

Debt Collection complaints involve someone trying to collect money from a person.

They usually involve:
- Collection agencies or debt buyers  
- Harassment  
- Incorrect amounts  
- Lawsuit threats  
- Calling too often  
- Contacting the wrong person  

**Difference:**  
Debt Collection is about someone trying to collect money.  
Credit Reporting is about incorrect information on a credit report.

---

## #3 Bank Accounts

Created by merging:
- Checking or savings account  
- Bank account or service  

This category covers complaints about regular bank accounts, such as:
- Unauthorized withdrawals  
- Account freezes or closures  
- Overdraft fees  
- Problems accessing funds  
- Incorrect transactions  

---

## #4 Mortgage

Mortgage complaints involve home loans and related issues such as:

- Problems with monthly payments  
- Escrow account errors  
- Loan modification requests  
- Foreclosure concerns  
- Interest rate or payment changes  

The target is usually the company managing the home loan, not a credit bureau or debt collector.

---

## #5 Money Transfers and Digital Payments

Created by merging:
- Money transfer, virtual currency, or money service  
- Money transfers  
- Virtual currency  

---

## #6 Credit Cards

Created by merging:
- Credit card or prepaid card  
- Credit card  
- Prepaid card  

---

## #7 Student Loans

Complaints related to student loan servicing and repayment issues.

---

## #8 Vehicle Loan or Lease

Complaints related to car loans or lease agreements.

---

## #9 Consumer Loan

Created by merging:
- Payday loan  
- Title loan  
- Personal loan  
- Advance loan  
- Consumer loan  

These involve short-term or personal lending products.

---

## #10 Financial Services Support

Created by merging:
- Other financial service  
- Debt or credit management  

This category includes complaints about companies that provide financial help or support services but are not direct lenders, banks, credit bureaus, or debt collectors.

It covers issues with:
- Debt settlement companies  
- Credit counseling services  
- Other financial service providers  

Complaints may involve:
- High fees  
- Unclear terms  
- Failed promises  
- Poor service  

---