## Weak Priority Label Engineering from Complaint Narratives

Priority labels were weakly engineered from the complaint narratives.

Three priority levels were defined:

- **Immediate** – complaints indicating possible fraud, identity theft, unauthorized activity, security compromise, or other situations where a consumer may be actively losing money or experiencing identity misuse.
- **Same day** – complaints describing operational issues that prevent the customer from using their account or completing transactions, such as being unable to access an account, login failures, locked or blocked accounts, or failed transactions.
- **Regular** – all remaining complaints that represent disputes, reporting issues, service dissatisfaction, billing questions, or other non-urgent matters.

Labels were generated using rule-based keyword patterns extracted from the complaint narratives. Core fraud-related nouns (e.g., identity, fraud, theft, unauthorized, phishing, breach) were paired with action verbs (e.g., steal, hack, open, access, charge) to identify likely fraud events and assign **immediate** priority. Access-related keywords (e.g., access, login, account) combined with failure signals (e.g., cannot, unable, locked, blocked) were used to assign **same day** priority.

These labels are not ground truth; they represent **weak supervision** designed to create a large labeled dataset that can be used to train a machine learning model to learn richer linguistic patterns of urgency from the complaint narratives.
