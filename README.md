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
cd backend
pipenv install
```

3. Run the script:

Feeding data based on urls:
```
pipenv run cli load-data "https://uscarseat.com/pages/shipping-policy" "https://uscarseat.com/pages/return-refund" "https://uscarseat.com/pages/terms-of-services" --chatbot-id="yourchatbotid"
```

Answer the question:
```
pipenv run cli src/main.py answer-question "I want to return my product" --chatbot-id="yourchatbotid"
```

4. Run the API server
```
pipenv run api
```

# API Documentation
## Feed Data Based on URLs

This endpoint allows you to feed data to the chatbot by providing a list of URLs.

- **URL**: `/feed_data/{chatbot_id}`
- **Method**: POST
- **Content-Type**: application/json

### Request Body

| Field | Type   | Description                |
|-------|--------|----------------------------|
| urls  | array  | List of URLs to feed data. |

### Example Request
```
curl -X POST -H "Content-Type: application/json" -d '{
"urls": [
"https://uscarseat.com/pages/shipping-policy",
"https://uscarseat.com/pages/return-refund",
"https://uscarseat.com/pages/terms-of-services"
]
}' "http://localhost:8000/{chatbot_id}/feed_data"
```


### Response

- HTTP Status Code: 200 (OK)
- Content-Type: application/json

### Example Response

```json
{
  "message": "Data loaded successfully!"
}
```


## Answering a Question

This endpoint allows you to ask a question to the chatbot and retrieve an answer.

- **URL**: `/answer/{chatbot_id}`
- **Method**: POST
- **Content-Type**: application/json

### Request Body

| Field        | Type           | Description                         |
|--------------|----------------|-------------------------------------|
| question     | string         | The question to be answered.         |
| chat_history | array of objects | List of chat history (question/answer) tuples. |

### Example Request

```
curl -X POST -H "Content-Type: application/json" -d '{
"question": "I want to return my product",
"chat_history": []
}' "http://localhost:8000/{chatbot_id}/answer"
```


### Response

- HTTP Status Code: 200 (OK)
- Content-Type: application/json

### Example Response

```json
{
  "question": "Generated question",
  "answer": "Generated answer"
}
```
