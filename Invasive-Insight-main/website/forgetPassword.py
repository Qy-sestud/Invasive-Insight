from flask import Blueprint, request, session, jsonify
from .email import gmail_send_message
from .models import User, db
from random import randint
from google.auth.exceptions import RefreshError

forgetPassword = Blueprint('forgetPassword', __name__)

# method to check whether email exists
def checkEmail(input : str) ->bool:
    query = User.query.filter_by(email=input).first()
    print(query)
    if query:
        return True # user exists
    else:
        return False
    
# method to update user's password
def updatePassword(email : str, password : str) -> bool:
    user = User.query.filter_by(email=email).first()
    if not user: # Assume user already exists, so it reaches the next point.
        # if user does not exist, drop silently
        return False
    user.password = password
    try:
        db.session.commit()
        return True # Successful change of password
    except Exception as e:
        db.session.rollback()  # Roll back the session in case of an error
    return jsonify({"error": str(e)}), 500
     

# endpoint to send verification email
# To send email, send a GET request to /send_email?target=emailAddress
@forgetPassword.route('/send_email', methods=["GET"])
def send_email():
  random_number = randint(0,99999)
  padded_number = str(random_number).zfill(5)
  target_email = request.args.get('target')

  # check for valid email address
  if(not checkEmail(target_email)):
     return jsonify({"message": "Invalid Email"}), 400

  try:
    gmail_send_message(target_email, padded_number)
  except RefreshError as err:
    return jsonify({'message': 'You have to recreate OAuth Token. Refer Github documentations'}), 400
  
  with open("secrets/forgetpasswordOTP.txt", "w") as file:
    file.write(padded_number)
  with open("secrets/forgetpasswordEmail.txt", "w") as file:
    file.write(target_email)
  return jsonify({"message": "Application attempted to send email, check CLI for any errors"}), 200


# endpoint to receive user's otp 
@forgetPassword.route('/verify_user', methods=["GET"])
def verify_user():
  otp_by_user = request.args.get('otp')

  lines = list()
  with open("secrets/forgetpasswordOTP.txt", "r") as file:
    for line in file:
      lines.append(line.strip())
  real_otp = lines[0]
  
  lines = list() # clear lines
  with open("secrets/forgetpasswordEmail.txt", "r") as file:
    for line in file:
      lines.append(line.strip())
  userEmail = lines[0]

  if real_otp == otp_by_user:
    if userEmail == None:
       return jsonify({"message": "Havent sent email yet"}), 404
    with open("secrets/verifiedEmail.txt", "w") as file:
      file.write(userEmail)
    with open("secrets/forgetpasswordEmail.txt", "w") as file:
      file.write("")
    return jsonify({"Verified":True}), 200
  else:
    return jsonify({"Verified":False}), 404

# endpoint to change user's password
# To change password, /change_password
@forgetPassword.route('/change_password', methods=['GET'])
def changePassword():
   newPassword = request.args.get('password')

   lines = list()
   with open("secrets/verifiedEmail.txt", "r") as file:
    for line in file:
      lines.append(line.strip())
   print(lines[0])

   if (lines[0]):
       updatePassword(lines[0], newPassword)
       # reset verified passwords
       with open("secrets/verifiedEmail.txt", "w") as file:
          file.write("")
       return jsonify({"message": "Password changed"}), 200
   else:
      return jsonify({"message": "OTP not entered yet. And you are a hacker"}), 404