Weekend Hackathon - Ecom Chatbot 
---

Wiki: https://www.notion.so/tucq/Hackathon-June16-47a16728fe4e4f63b23a738cb1f6d144?pvs=4 

Frontend: https://ecomchatbot.vercel.app/ 

--
### How to run backend
1. Presiquites:
  - Python 3.11
  - pipenv

2. Install dependencies:
```
pipenv install
```

3. Run the script:

Feeding data based on urls:
```
pipenv run python src/main.py load-data "https://uscarseat.com/pages/shipping-policy" "https://uscarseat.com/pages/return-refund" "https://uscarseat.com/pages/terms-of-services"
```

Answer the question:
```
pipenv run python src/main.py answer-question "I want to return my product"
```
