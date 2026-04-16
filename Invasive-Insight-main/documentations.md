# Initial Set Up
1. First, we will need to clone the repository (if you haven't yet)
```sh
git clone git@github.com:DYing04/Invasive-Insight.git
```
2. We will set up SQLite and SQLAlchemy for database
```sh
pip install Flask-SQLAlchemy
```
Remember to also run the below line
```
pip install -U flask-cors
```
- Yep that's it :)
3. Try to start server.
```sh
cd Invasive-Insight
python main.py
```
4. Install relevant python modules. Paste in CLI
```sh
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
```
5. Open a Gmail Account or use my throwaway gmail address
6. Request Oauth ID from Gmail API at
```
https://console.cloud.google.com/apis/credentials?project=harimau-407712
```
7. Create OAuth client ID 
8. Download the JSON file 
9. Create a directory called `secrets` in `Invasive-Insight` and paste the file in the dir. If you already have this directory, please delete <u>everything</u> in the file first.
10. Rename the json file as `credentials.json`
11. Run the server
12. Query `http://127.0.0.1:5000/email/send_email?target=youremail@address.com` endpoint to send email
13. Allow the app to send email on your behalf ![[Pasted image 20241114215650.png]]
14. If you are successful, you will get this output
```
"Application attempted to send email, check CLI for any errors"
```

# Endpoint Documentations
## Verify Email
1. To send verification email to users, send a GET request to `/email/send_email`. 
```http
GET /email/send_email?target=youremail@address.com HTTP/2.0
```
The application will return a response like this if successful (Check CLI if there is anymore errors) 
```json
{"message": "Application attempted to send email, check CLI for any errors"}
```
If your token has expired, you will see this with response code 400
```json
{'message': 'You have to recreate OAuth Token. Refer Github documentations'}
```
If successful, you will see this in the CLI:
```
Message Id: blablabla
```
If unsuccessful, you will see this in the CLI:
```
An error occurred: blablabla
```
2. To verify users, send a GET request to `/email/verify_user` with the code as GET parameter. 
Example request
```http
GET /email/verify_user?otp=12345 HTTP/2.0
```
If successful, you will see this response
```json
{"Verified":True}
```
If unsuccessful, you will see this response
```json
{"Verified":False}
```

## Landing page
1. To get information about completed quiz, send a GET request to `/landing/get_completed_quiz`
```http
GET /landing/get_completed_quiz HTTP/2.0
```
It will return a response like this:
```json
{"name":["Easy Invasive Species Quiz"]}
```

## Register new user
1. To register new user to database, choose the POST method in Postman and enter URL for endpoint:
```
http://127.0.0.1:5000/add_user
```
2. Set the request body
- Go to the Body tab in Postman.
- Select raw and set the type to JSON from the dropdown menu.
- Enter the JSON data, here is an example:
```
{
    "username" : "Ying",
    "email" : "ying@gmail.com",
    "password" : "ying123"
}
```
3. Click the send button
4. If successful, you should receive a response like this
```
{
    "message": "User added successfully"
}
```

## Login
1. In Postman, choose POST method
2. Enter the URL for the endpoint
```
http://127.0.0.1:5000/login
```
3. Set the Request Body
- Go to the Body tab in Postman.
- Select raw and set the type to JSON from the dropdown menu.
- Enter the JSON data with the fields you want to update. Here’s an example:
```
{
    "username": "Ying",
    "password": "ying123"
}
```
- Click the Send button
4. If successful, you should receive a response like this:
```
{
    "message": "Login successful"
}
```
5. If the username or password is incorrect, you will receive an error response:
```
{
    "error": "Invalid password or username"
}
```
## Logout
1. In Postman, choose POST method
2. Enter the endpoint URL:
```
http://127.0.0.1:5000/logout
```
- No need to include a request body
- Click Send
3. Expected response:
```
{
    "message": "Logged out successfully"
}
```

## Update Profile
1. In Postman, choose the PUT method.
2. Enter the URL for the endpoint
```
http://127.0.0.1:5000/user/update_profile/<user_id>
```
- Replace <user_id> with the ID of the user you want to update (e.g., 1).
3. Set the Request Body
- Go to the Body tab in Postman.
- Select raw and set the type to JSON from the dropdown menu.
- Enter the JSON data with the fields you want to update. Here’s an example:
```
{
    "username": "new_username",
    "password": "new_password"
}
```
- Note: Only include the fields you wish to update; any missing fields will remain unchanged.
4. Click the Send button to submit the request.
5. If successfull, you should receive a response like this
```
{
    "message": "Profile updated successfully"
}
```

## Get all User details
1. To get all user details, send a GET request to 
```
http://127.0.0.1:5000/users
```
* Note: you have to register new user first only there will be users data in your database
2. It will return a response like this (example):
```
[
    {
        "email": "wee@gmail.com",
        "id": 1,
        "password": "wee123",
        "score": null,
        "username": "wee"
    },
    {
        "email": "peter@gmail.com",
        "id": 2,
        "password": "peter123",
        "score": null,
        "username": "Peter"
    }
]
```

## Get all questions
1. To get all quiz questions, send a GET request to `http://127.0.0.1:5000/quiz_all`
2. It will return a response like this:
```
[
    {
        "answer": "B) Suckermouth catfish (Hypostomus plecostomus)",
        "explanation": "This fish is also known as “Ikan Bandaraya” in Malaysia...",
        "hint": "This fish is black in colour.",
        "options": [
            "A) Ikan pacu (Mylopus)",
            "B) Suckermouth catfish (Hypostomus plecostomus)",
            "C) African catfish",
            "D) Flower horn (Cichiasoma)"
        ],
        "question": "The fish in the picture below is an invasive species in Malaysia that has spread throughout the waterways in Malaysia. What is the name of the fish?",
        "question_id": 1,
        "quiz_completed": false,
        "quiz_id": 1
    },
    {
        "answer": "C",
        "explanation": "Invasive species often grow quickly in a new environment because they lack natural predators. In their native habitats, predators, parasites, and diseases help control their populations. However, when these species are introduced to a new area, the local ecosystem often lacks the specific predators or diseases that can limit their growth. This allows invasive species to reproduce rapidly, often outcompeting native species and disrupting the balance of the ecosystem.",
        "hint": "Think about what controls the population of a species in an ecosystem. What role do predators play in keeping populations in check?",
        "options": [
            "Invasive species are native to an area.",
            "Invasive species are prey to many animals.",
            "Invasive species have no predators.",
            "Invasive species keep the ecosystems in equilibrium."
        ],
        "question": "Why do the populations of invasive species grow so quickly?",
        "question_id": 2,
        "quiz_completed": false,
        "quiz_id": 1
    },
    # and the list goes on
]
```

## Get all completed questions
1. To get quizzes completed, send a GET request to `http://127.0.0.1:5000/quiz_all/completed`
2. It will return a response like this:
```
[]
```

## Get question hint
1. To get hint for each question, send a GET request to `http://127.0.0.1:5000/questions/<question_id>/hint`
2. If question_id: 2 (http://127.0.0.1:5000/questions/2/hint).  It will return a response like this:

```
{
    "hint": "Think about what controls the population of a species in an ecosystem. What role do predators play in keeping populations in check?",
    "question_id": 2
}
```
## Get the completed TIME of a specific user by user ID
1. To get completed quiz time for a specific user, send a GET request at `http://127.0.0.1:5000/user/<user_id>/completed`
2. If user_id:1 and the user haven't completed the quiz.  It will return a response like this:
```
[
{
    "message": "User has not completed the quiz.",
    "user_id": 1,
    "username": "testQY"
}
]
```
3. If user_id:1 and the user have completed the quiz.  It will return a response like this:
```
{
    "completed_at": "2024-12-01T12:00:00", # Time when user completed the quiz
    "user_id": 1,
    "username": "testQY"
}
```

## Get the completed time of ALL users
1. To get completed quiz time for all users, send a GET request at `http://127.0.0.1:5000/users/completed`
2. It will return a response like this:
```
[
    {
        "completed_at": "2024-12-09T23:18:18.179972",
        "user_id": 1,
        "username": "Ying ying"
    },
    {
        "completed_at": "2024-12-09T10:15:30",
        "user_id": 2,
        "username": "wee"
    }
]
```

## Account Recovery
1. To send OTP to client to reset email address, send a GET request to `/forgetPassword/send_email?target=<email>`
```
http://127.0.0.1:5000/forgetPassword/send_email?target=<email>
http://127.0.0.1:5000/forgetPassword/send_email?target=23054588@siswa.um.edu.my
```
Output:
If email is invalid (Not in database), you will receive HTTP 400 with the following JSON
```json
{"message": "Invalid Email"}
```
If your OAuth Client ID has expired, you will receive HTTP 400 with 
```json
{'message': 'You have to recreate OAuth Token. Refer Github documentations'}
```
If email exists in database and an email was sent, you will receive HTTP 200 with
```json
{"message": "Application attempted to send email, check CLI for any errors"}
```
2. To check client's OTP, send a GET request to
```
http://127.0.0.1:5000/forgetPassword/verify_user?otp=94769
```
Output:
If email is not sent yet, it will send a HTTP 404 and 
```json
{'message', 'Haven\'t sent email yet'}
```
If OTP is invalid, it will send a HTTP 404 and
```json
{"Verified":False}
```
If OTP is valid, it will send a HTTP 200 and
```json
{
  "Verified": True
}
```
3. To change user's password, send a GET request to
```
http://127.0.0.1:5000/forgetPassword/change_password?password=cisco
```
Output:
If someone try to change the password without getting OTP first,
```json
{'message': 'OTP not entered yet. And you are a hacker'}
```
If password was changed successfully,
```json
{'message': 'Password changed'}
```

## Get ALL users' score
1. To get ALL USERS' score, send a GET request to `http://127.0.0.1:5000/users/scores`
2. It will return a response like this:
```
{
    "data": [
        {
            "score": 95,
            "user_id": 1,
            "username": "Ying"
        },
        {
            "score": 80,
            "user_id": 2,
            "username": "wee"
        }
    ]
}
```

## Store a user's score & quiz complete time into database
1. To submit a user's score, send a POST request to `http://127.0.0.1:5000/user/users/<user_id>/score_time`
- Replace <user_id> with the ID of the user you want to update (e.g., 1).
2. Set the request body:
```
{
    "score": 95,
    "completed_at": "2024-12-09T10:15:30"  // Optional. If omitted, the current time will be used.
}

```
3. If successful, it will return a response like this:
```
{
    "data": {
        "completed_at": "2024-12-09T10:15:30",
        "new_score": 95,
        "user_id": 2
    },
    "message": "Score and completion time updated successfully",
    "status": "success"
}
```
4. If error (for example invalid score), the response will be like this:
```
{
    "message": "Score must be a non-negative integer",
    "status": "error"
}
```

## Get score of a specific user by user ID
1. To get a user's score, send a GET request to `http://127.0.0.1:5000/user/users/<user_id>/score`
- Replace <user_id> with the ID of the user you want to update (e.g., 1).
2. If successful, it will return a response like this:
```
{
    "data": {
        "score": 95,
        "user_id": 1,
        "username": "Ying"
    }
}
```
3. If error (for example invalid user id), the response will be like this:
```
{
    "message": "User not found",
    "status": "error"
}
```
## Quiz Bookmarking
1. In Postman, choose POST method
2. Enter the URL for the endpoint
```
http://127.0.0.1:5000/bookmark
```
3. Set the Request Body
- Go to the Body tab in Postman.
- Select raw and set the type to JSON from the dropdown menu.
- Enter the JSON data with user_id and quiz_id. Here’s an example:
```
{
    "user_id": "1",
    "quiz_id": "2"
}
```
- Click the Send button
4. If successful, you should receive a response like this:
```
{
    "message": "Quiz ? bookmarked successfully"
}
```
5. To get the bookmarked quiz_id, choose GET method
6. Enter the URL for the endpoint
```
http://127.0.0.1:5000/bookmark/<user_id>
```
7. If successful and user did bookmark quiz, you should receive a response like this:
```
{
    "quiz_id": 1,
    "user_id": 2
}
```
8. If successful but user didn't bookmard quiz, response:
```
{
    "message": "No quiz bookmarked",
    "user_id": 5
}
```