import os.path
import base64
import google.auth
from flask import Blueprint, jsonify, request
from random import randint

from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]

def gmail_send_message(sender_email : str, otp:str):
  """Create and send an email message
  Print the returned  message id
  Returns: Message object, including message id

  Load pre-authorized user credentials from the environment.
  TODO(developer) - See https://developers.google.com/identity
  for guides on implementing OAuth2 for the application.
  """
  # verify correct input
  if len(otp)!=5:
    return


  # Get token first
  creds = None
  # The file token.json stores the user's access and refresh tokens, and is
  # created automatically when the authorization flow completes for the first
  # time.
  if os.path.exists("secrets/token.json"):
    creds = Credentials.from_authorized_user_file("secrets/token.json", SCOPES)
  # If there are no (valid) credentials available, let the user log in.
  if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
      creds.refresh(Request())
    else:
      flow = InstalledAppFlow.from_client_secrets_file(
          os.getcwd()+"\\secrets\\credentials.json", SCOPES
      )
      creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open("secrets\\token.json", "w") as token:
      token.write(creds.to_json())

  try:
    service = build("gmail", "v1", credentials=creds)
    message = EmailMessage()

    message.set_content("Your verification number is "+otp)

    message["To"] = sender_email
    message["From"] = "harimaudmn@gmail.com"
    message["Subject"] = "Verification Email"

    # encoded message
    encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

    create_message = {"raw": encoded_message}
    # pylint: disable=E1101
    send_message = (
        service.users()
        .messages()
        .send(userId="me", body=create_message)
        .execute()
    )
    print(f'Message Id: {send_message["id"]}')
  except HttpError as error:
    print(f"An error occurred: {error}")
    send_message = None
  return send_message

# Create endpoint
emailRoutes = Blueprint('email', __name__) # declare our endpoint

@emailRoutes.route('/send_email', methods=["GET"])
def send_email():
  random_number = randint(0,99999)
  padded_number = str(random_number).zfill(5)
  target_email = request.args.get('target')

  # gmail_send_message(target_email, padded_number)

  try:
    gmail_send_message(target_email, padded_number)
  except google.auth.exceptions.RefreshError as err:
    return jsonify({'message': 'You have to recreate OAuth Token. Refer Github documentations'}), 400
  
  with open("secrets/otp.txt", "w") as file:
    file.write(padded_number)

  return jsonify({"message": "Application attempted to send email, check CLI for any errors"}), 200

@emailRoutes.route('/verify_user', methods=["GET"])
def verify_user():
  otp_by_user = request.args.get('otp')

  lines = list()
  with open("secrets/otp.txt", "r") as file:
    for line in file:
      lines.append(line.strip())
  real_otp = lines[0]

  if real_otp == otp_by_user:
    return jsonify({"Verified":True}), 200
  else:
    return jsonify({"Verified":False}), 404
