
# Quiz app

It's an app for learning new words. It also allow users use different meanings for a word. User can see learned words in history, where added score and time when the word was learned.





## Credentials

The quiz app also uses credentials, and for each request user must be loggined.
## Installation

For installation you need to pull this repo and run follow commands

```bash
  python manage.py createsuperuser
  python3 manage.py runserver
```
    
## API Reference

#### Create new word

```http
  POST api/question
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `` | `string` | User should pass a data with required fields: text, mark, answers |

#### Get all items

```http
  GET api/question
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| ``      | `string` | Show all words for learning|

#### Answear on a question

```http
  POST api/question/{id}/answer
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `id`      | `string` | Send a post request for answer on the question|

#### Get history

```http
  POST api/history
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| ``      | `string` | Show all learned words with score and data when it was learned| 