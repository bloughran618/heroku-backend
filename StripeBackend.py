import sys
import os
import stripe
import time
from flask import Flask, session, jsonify, request, Response
import sys
import json
import requests
from io import BytesIO
from email.message import Message
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from pytz import timezone
from pythemis.smessage import SMessage
from pythemis.exception import ThemisError
from pythemis.scell import SCellSeal
import base64
from Crypto.Cipher import AES
import binascii
import psycopg2

# import firebase
try:
    import pyrebase
except Exception as e:
    print("The exception is: " + str(e))

stripe.api_key = os.environ.get("api_key")
webhook_secrat = ""
stripe.api_version = "2019-03-14" # "2018-05-21"
app = Flask(import_name="SpotBird")

# print("Charge:\n")
# print(stripe.Charge.retrieve(
#   "ch_1DfXjJLkBK9oeUkAfs7NQdFI",
#   api_key="sk_test_BPL2Sy81u9355r3GlN4XKG2t"
# ))


# Create Account
# print("\n\nAccount:\n")
try:
  # account = stripe.Account.create(
  #     type="custom",
  #     country="US",
  #     email="foo@bar.com"
  # )
  # print("Account successfully created:")
  # print(account[id])
    pass
except stripe.error.CardError as e:
    # Since it's a decline, stripe.error.CardError will be caught
    print("Card Error")
    body = e.json_body
    err  = body.get('error', {})

    print("Status is: %s" % e.http_status)
    print("Type is: %s" % err.get('type'))
    print("Code is: %s" % err.get('code'))
    # param is '' in this case
    print("Param is: %s" % err.get('param'))
    print("Message is: %s" % err.get('message'))
except stripe.error.RateLimitError as e:
    # Too many requests made to the API too quickly
    print("API Timeout")
    body = e.json_body
    err = body.get('error', {})

    print("Status is: %s" % e.http_status)
    print("Type is: %s" % err.get('type'))
    print("Code is: %s" % err.get('code'))
    # param is '' in this case
    print("Param is: %s" % err.get('param'))
    print("Message is: %s" % err.get('message'))
    pass
except stripe.error.InvalidRequestError as e:
    # Invalid parameters were supplied to Stripe's API
    print("Invalid Parameters")
    body = e.json_body
    err = body.get('error', {})

    print("Status is: %s" % e.http_status)
    print("Type is: %s" % err.get('type'))
    print("Code is: %s" % err.get('code'))
    # param is '' in this case
    print("Param is: %s" % err.get('param'))
    print("Message is: %s" % err.get('message'))
    pass
except stripe.error.AuthenticationError as e:
    # Authentication with Stripe's API failed
    # (maybe you changed API keys recently)
    print("Authentication Error")
    body = e.json_body
    err = body.get('error', {})

    print("Status is: %s" % e.http_status)
    print("Type is: %s" % err.get('type'))
    print("Code is: %s" % err.get('code'))
    # param is '' in this case
    print("Param is: %s" % err.get('param'))
    print("Message is: %s" % err.get('message'))
    pass
except stripe.error.APIConnectionError as e:
  # Network communication with Stripe failed
  print("Network Error")
  body = e.json_body
  err = body.get('error', {})

  print("Status is: %s" % e.http_status)
  print("Type is: %s" % err.get('type'))
  print("Code is: %s" % err.get('code'))
  # param is '' in this case
  print("Param is: %s" % err.get('param'))
  print("Message is: %s" % err.get('message'))
  pass
except stripe.error.StripeError as e:
    # Display a very generic error to the user, and maybe send
    # yourself an email
    print("Stripe Error")
    body = e.json_body
    err = body.get('error', {})

    print("Status is: %s" % e.http_status)
    print("Type is: %s" % err.get('type'))
    print("Code is: %s" % err.get('code'))
    # param is '' in this case
    print("Param is: %s" % err.get('param'))
    print("Message is: %s" % err.get('message'))
    pass
except Exception as e:
    # Something else happened, completely unrelated to Stripe
    pass

# expand customer via charge ID
# print("\n\n\n\nCustomer:\n")
# print(stripe.Charge.retrieve("ch_1DfXjJLkBK9oeUkAfs7NQdFI",
#                              expand=['customer']))

# print("Retrieve Acccount")
# account = stripe.Account.retrieve("acct_1DgdW8IWmP3kfqWG")
# print(account.type)
# print(account.email)
# account.legal_entity.type = "individual"
# account.legal_entity.first_name = "Brian"
# account.legal_entity.last_name = "Loughran"
# account.legal_entity.personal_address.line1 = "41 Cambridge Ave."
# account.legal_entity.personal_address.city = "Denville"
# account.legal_entity.personal_address.state = "NJ"
# account.legal_entity.personal_address.postal_code = "07834"
# account.legal_entity.dob.day = "18"
# account.legal_entity.dob.month = "06"
# account.legal_entity.dob.year = "1995"
# account.legal_entity.ssn_last_4 = "2427"
# print(account.legal_entity.type)
# print(account.legal_entity.first_name)
# print(account.legal_entity.personal_address.line1)
# print(account.legal_entity.dob.year)
# print(account.legal_entity.ssn_last_4)
# account.save()


# important functions
# def createAccount():
#     account = stripe.Account.create(
#         country="US",
#         type="custom"
#     )
#     account_id = account.id
#     return account_id


# def updatePersonalInfo(id, first, last, addressLine1, addressLine2, city, state, zip, dobDay, dobMonth, dobYear, last4):
#     account = stripe.Account.retrieve(id)
#
#     account.legal_entity.type = "individual"
#     account.legal_entity.first_name = first
#     account.legal_entity.last_name = last
#     account.legal_entity.personal_address.line1 = addressLine1
#     account.legal_entity.personal_address.line2 = addressLine2
#     account.legal_entity.personal_address.city = city
#     account.legal_entity.personal_address.state = state
#     account.legal_entity.personal_address.postal_code = zip
#     account.legal_entity.dob.day = dobDay
#     account.legal_entity.dob.month = dobMonth
#     account.legal_entity.dob.year = dobYear
#     account.legal_entity.ssn_last_4 = last4
#
#     account.save()


def accept_services_agreement(id, ip):
    account = stripe.Account.retrieve(id)
    account.tos_acceptance.date = int(time.time())
    account.tos_acceptance.ip = ip
    account.save()
#
#
# def delete_account(id):
#     account = stripe.Account.retrieve(id)
#     account.delete()
#
#
# def create_customer():
#     customer = stripe.Customer.create()
#     customer_id = customer.id
#     return customer_id


# def add_card_to_customer(customer_id):
#     customer = stripe.Customer.retrieve(customer_id)
#     #TODO: figure out how to get the source from swift
#     customer.sources.create(source="?")


def log_info(message):
    print(message)
    sys.stdout.flush()
    return message


# @app.route('/spot_purchase', methods=['POST'])
# def customer_pays_owner():
#     source_id = request.form['source_id']
#     destination_id = request.form['destination_id']
#     amount = request.form['amount']
#
#     log_info("creating charge")
#     stripe.Charge.create(
#         amount=amount,
#         currency="usd",
#         customer=source_id,  # obtained with Stripe.js
#         description="Testing..."
#     )
#     log_info("creating transfer")
#     amount = int(round(amount*0.85)) # take some money for yourself :)
#     stripe.Transfer.create(
#         amount=amount,
#         currency="usd",
#         destination=destination_id
#     )
#     log_info("success")
#     return jsonify(success="success")


def pay_owner(destination, amount_paid):
    destination_id = destination
    amount = amount_paid

    log_info("creating transfer for" + str(amount))
    stripe.Transfer.create(
        amount=amount,
        currency="usd",
        destination=destination_id
    )
    log_info("success")


    

@app.route('/customer_id', methods=['POST'])
def create_customer():
    log_info("Creating a customer ID!!!")
    log_info("start creating customer")
    customer = stripe.Customer.create()
    customer_id = customer.id
    log_info("end creating customer")
    log_info("customer_id: " + customer_id)
    # log_info("jsonify customer ID: " + jsonify(customer_id=customer_id).dumps())
    log_info("now return")
    return jsonify(customer_id=customer_id)


@app.route('/ephemeral_keys', methods=['POST'])
def ephemeral_key():

    api_version = request.form['api_version']
    customer_id = request.form['customer_id']
    log_info(api_version)
    log_info(customer_id)

    print("new API version: " + stripe.api_version)

    log_info("start creating key")
    key = stripe.EphemeralKey.create(
        customer=customer_id,
        stripe_version=api_version)
    log_info("finish creating key")

    log_info(key)

    # log_info(jsonify(key))
    return jsonify(key)


@app.route('/charge', methods=['POST'])
def charge():
    source = request.form['source']
    amount = request.form['amount']
    customer_token = request.form['customer_token']

    # just debug to see what I have so far...
    log_info("This is the source: " + amount)
    log_info("This is the source: " + source)
    log_info("This is the customer token: " + customer_token)
    
    # just put the ruby code from github in python here...
    try:
        # charge = stripe.Charge.create(
        #     amount=amount, # remember that this is in cents
        #     currency="usd",
        #     # customer = customer_token,
        #     source=source,
        #     description="Spotbird Parking Fee"
        # )
        # print(charge.id)
        # testCharge = stripe.Charge.retrieve(charge.id)
        # print(testCharge)

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            customer=customer_token,
            payment_method=source,
            payment_method_types=['card']
        )

        #log_info(intent)
        intent_id = intent["id"]
        payment_method = intent["payment_method"]
        #log_info("ID: " + str(intent_id))

        capture = stripe.PaymentIntent.confirm(
            intent_id,
            payment_method=payment_method
        )
        
    # except stripe.error as e:
    except:
        log_info("PAYMENT FAILED!!!")
        pass
    '''except Exception as e:
        log_info("The exception is: " + str(e))
        return jsonify(message="Error creating charge: " + e.message)'''
    return jsonify(paymentIntent_id = intent_id)


@app.route('/account_id', methods=['POST'])
def create_account():
    log_info("Creating a account ID!!!")
    log_info("start creating account")
    account = stripe.Account.create(
        country="US",
        type="custom",
        requested_capabilities=['platform_payments']
    )
    account_id = account.id
    log_info("end creating account")
    log_info("account id: " + account_id)
    # log_info("jsonify customer ID: " + jsonify(customer_id=customer_id).dumps())
    log_info("now return")
    return jsonify(account_id=account_id)


@app.route('/add_connect_info', methods=['POST'])
def add_connect_info():
    log_info("Adding tokenized connect info")
    log_info(request.form)
    account_id = request.form['account_id']
    log_info("Got the account ID: " + account_id)
    ip_address = request.form['ip_address']
    log_info("Got the ip address: " + ip_address)
    acct_token = request.form['info_token']
    log_info("form info successfully loaded")
    account = stripe.Account.retrieve(account_id)
    log_info("Found associated stripe account")
    log_info(acct_token)
    account.account_token = acct_token
    log_info("Successfully associated account token")

    # dummy code while waiting for stripe
    account.save()
    account.individual.address.city = request.form['city']
    account.individual.address.country = "US"
    account.individual.address.line1 = request.form['line1']
    account.individual.address.line2 = request.form['line2']
    account.individual.address.postal_code = request.form['postalcode']
    account.individual.address.state = request.form['state']


    accept_services_agreement(account_id, ip_address)
    log_info("Successfully accepted TOS")
    log_info(account)
    account.save()
    return jsonify(success="success")


@app.route('/add_bank_info', methods=['POST'])
def add_bank_info():
    log_info("Adding tokenized bank info")
    log_info(request.form)
    account_id = request.form['account_id']
    log_info("Got one form info")
    acct_token = request.form['account_token']
    log_info("form info successfully loaded")
    account = stripe.Account.retrieve(account_id)
    log_info("Found associated stripe account")
    log_info(acct_token)
    account.external_accounts.create(external_account=acct_token, default_for_currency=True)
    log_info("Successfully associated account token")
    delete_all_external_accounts_except_default(account_id)
    log_info("Cleaned up other accounts")
    account.save()
    return jsonify(success="success")


# helper to add_bank_info
def delete_all_external_accounts_except_default(account_id):
    account = stripe.Account.retrieve(account_id)
    accounts = account.external_accounts.list()
    for acct in accounts:
        try:
            account.external_accounts.retrieve(acct.id).delete()
        except stripe.error.InvalidRequestError:
            pass


# should not do anything, just keeping it around in case I need it in the future
@app.route('/recieve_webhook', methods=['POST'])
def recieve_webhook():
    # event_json = json.loads(request.body)
    # log_info(event_json)

    payload = request.data.decode("utf-8")
    log_info("The following is the payload: \n" + payload)

    signature = request.headers.get("Stripe-Signature", None)

    try:
        event = stripe.Webhook.construct_event(payload, signature, webhook_secrat)
    except ValueError:
        log_info("Error when decoding the event!")
        return "Bad payload", 400
    except stripe.error.SignatureVerificationError:
        log_info("Bad Signature!")
        return "Bad signature", 400


    log_info(
        "Received event: id={id}, type={type}".format(
            id=event.id, type=event.type
        )
    )

    return Response(status=200)


@app.route('/check_stripe_account', methods=['POST'])
def check_stripe_account():
    account_id = request.form['account_id']
    account = stripe.Account.retrieve(account_id)
    enabledBool = account["payouts_enabled"]
    log_info("Is the account enabled? : " + str(enabledBool))
    due = account["requirements"]["currently_due"]
    log_info("This is what is due: " + str(due))

    return jsonify(enabled=enabledBool, due=due)


# update this funciton for real encryption
def decrypt_ssn(encrypted_text):
    print(encrypted_text)
    
    aes = AES.new(b'This is a key123', AES.MODE_CFB, b'0000000000000000', segment_size = 128)
    encrypted_text_bytes = binascii.a2b_hex(encrypted_text)
    decrypted_text = aes.decrypt(encrypted_text_bytes)
    return int(decrypted_text)

@app.route('/save_ssn', methods=['POST'])
def save_ssn():
    account_id = request.form['account_id']
    account = stripe.Account.retrieve(account_id)
    encrypted_ssn = request.form['encrypted_ssn']
    decrypted_ssn = decrypt_ssn(encrypted_ssn)
    print("SSN decrypted")
    #account["individual"]["id_number"] = decrypted_ssn
    #account.save()
    return jsonify(success="success")


@app.route('/do_nothing', methods=['POST'])
def do_nothing():
    # do nothing
    return


@app.route('/')
def connect():
    # return render_template('index.html', key=stripe_keys['publishable_key'])
    log_info("We are in the app route main")
    return "Lookit my backend!!! -- I'm Brian!!!"


@app.errorhandler(500)
def log_error(error):
    log_info("yep, here's your error: " + str(error))
    return error


def fetch_picture_from_firebase(img_id):
    # firebase auth and setup storage
    config = {
        "apiKey": os.environ.get("firebase_api"),
        "authDomain": os.environ.get("firebase_auth_domain"),
        "databaseURL": os.environ.get("firabase_database_url"),
        "storageBucket": os.environ.get("firebase_storage_bucket"),
        "serviceAccount": os.environ.get("firebase_services_account")
    }
    fb = pyrebase.initialize_app(config)
    email = os.environ.get("firebase_email")
    pw = os.environ.get("firebase_email_password")
    auth = fb.auth()
    user = auth.sign_in_with_email_and_password(email=email, password=pw)
    # db = fb.database()
    storage = fb.storage()

    # retrieve the file url
    try:
        file_url = storage.child("/temp/" + str(img_id)).get_url(token=None)
        log_info("got file url: " + file_url)
        return file_url
    except Exception as e:
        log_info("ERROR getting picture from firebase: " + str(e))
    # Brian = db.child("User").child("-LbQoDVfuiRm7NBsWOR9").child("id").get(user['idToken']).val()
    # print(Brian)
    return


def save_files_to_stripe(account_id, file_url_front, file_url_back):
    try:
        # create stripe File object
        response = requests.get(file_url_front, stream=True)
        img_file_front = BytesIO(response.content)
        stripe_file_front = stripe.FileUpload.create(
            purpose="identity_document",
            file=img_file_front,
            stripe_account=account_id
        )

        response = requests.get(file_url_back, stream=True)
        img_file_back = BytesIO(response.content)
        stripe_file_back = stripe.FileUpload.create(
            purpose="identity_document",
            file=img_file_back,
            stripe_account=account_id
        )

        # save images
        account = stripe.Account.retrieve(account_id)
        account["individual"]["verification"]["document"]["front"] = stripe_file_front.id
        account["individual"]["verification"]["document"]["back"] = stripe_file_back.id
        account.save()
        log_info("identity documents uploaded and saved")
        return True
    except Exception as e:
        log_info("ERROR saving files to Stripe: " + str(e))
        return False


@app.route('/upload_id_docs', methods=['POST'])
def upload_pictures_to_stripe():
    account_id = request.form['account_id']
    front_image_id = request.form['front_image_id']
    back_image_id = request.form['back_image_id']
    front_url = fetch_picture_from_firebase(front_image_id)
    back_url = fetch_picture_from_firebase(back_image_id)

    # save the files to stripe and check if it worked
    success = save_files_to_stripe(account_id, front_url, back_url)
    if success:
        log_info("identity documents upload complete")
        return jsonify(success="success")
    else:
        response = jsonify(success="failure")
        response.status_code = 400
        return response


@app.route('/send_email', methods=['POST'])
def send_email():
    try:
        message = request.form['message']
        # remove non-ascii char's
        message = ''.join(char for char in message if ord(char) < 128)

        log_info("This is the message: " + str(message))

        import smtplib, ssl
        port = 465
        password = os.environ.get("spotbirdtheapp_password")

        # Create secure SSL context
        context = ssl.create_default_context()

        # send the email
        with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
            server.login("spotbirdtheapp@gmail.com", password)
            server.sendmail("spotbirdtheapp@gmail.com", "spotbirdllc@gmail.com", message)

        log_info("message was sent successfully")
        return jsonify(success='success')
    except Exception as e:
        exc_type, exc_obj, exc_tb = sys.exc_info()
        log_info("This is the error in send_email: " + str(e))
        log_info("This is the error line: " + str(exc_tb.tb_lineno))
        response = jsonify(success="failure")
        response.status_code = 400
        return response

@app.route('/fetch_Balance', methods=['POST'])
def fetch_Balance():
    account_id = request.form['account_id']
    balance = stripe.Balance.retrieve(stripe_account=account_id)
    print("Balance is: " + str(balance.available[0].amount))
    return jsonify(Balance = balance.available[0].amount)

@app.route('/fetch_LifeTimeBalance', methods=['POST'])
def fetch_LifeTimeBalance():
    account_id = request.form['account_id']
    totalTransfer = 0
    transfers = stripe.Transfer.list(destination = account_id, limit = 100)
    for eachTransfer in transfers:
        totalTransfer += int(eachTransfer.amount)
    print("Lifetime total balance: " + str(totalTransfer))
    return jsonify(Transfer = totalTransfer)

@app.route('/test_heroku_backend', methods=['POST'])
def test_heroku_backend():
    return jsonify(success = 'success')

@app.route('/test_stripe', methods=['POST'])
def test_stripe():
    account_id = request.form['account_id']
    balance = stripe.Balance.retrieve(stripe_account=account_id)
    return jsonify(Balance = balance.available[0].amount)

global scheduler
DATABASE_URL = os.environ.get("DATABASE_URL")

def configure_scheduler():
    global scheduler
    
    jobstores = {
        'default': SQLAlchemyJobStore(url=DATABASE_URL)
    }
    executors = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }
    job_defaults = {
        'coalesce': True,
        'max_instances': 3
    }
    scheduler = BackgroundScheduler()
    scheduler.configure(jobstores=jobstores, executors=executors, job_defaults=job_defaults, timezone='America/New_York')


@app.route('/schedule_transfer', methods=['POST'])
def schedule_transfer():
    global scheduler
    destination_id = request.form['destination_id']
    amount = request.form['amount']
    spot_id = request.form['spotID']
    startDateTime = request.form['startDateTime']

    start_date = startDateTime + ":00"

    try:
        scheduler.add_job(pay_owner, 'date', run_date= start_date, args=[destination_id, amount], id = spot_id + start_date, misfire_grace_time = 86400)
        scheduler.print_jobs()
        print("In try method")
    except:
        daily_start_scheduler()
        scheduler.add_job(pay_owner, 'date', run_date= start_date, args=[destination_id, amount], id = spot_id + start_date, misfire_grace_time = 86400)
        scheduler.print_jobs()
        print("In except method")

    return jsonify(success="success")

@app.route('/remove_specified_job', methods=['POST'])
def remove_specified_job():
    global scheduler

    spot_id = request.form['spot_id']
    start_date = request.form['start_date']
    start_date = start_date + ":00"

    print(spot_id + start_date)

    try:
        scheduler.remove_job(spot_id + start_date)
        scheduler.print_jobs()
    except:
        daily_start_scheduler()
        scheduler.remove_job(spot_id + start_date)
        scheduler.print_jobs()
    
    return jsonify(success="success")

@app.route('/refund_charge', methods=['POST'])
def refund_charge():

    paymentIntent_id = request.form['paymentIntent_id']

    print("Intent ID: " + paymentIntent_id)
    
    intent = stripe.PaymentIntent.retrieve(paymentIntent_id)
    intent['charges']['data'][0].refund()

    return jsonify(success="success")

@app.route('/start_scheduler', methods=['POST'])
def start_scheduler():
    global scheduler

    try:
        configure_scheduler()
        scheduler.start()
    except:
        pass
    scheduler.print_jobs()
    
    return jsonify(success="success")


def daily_start_scheduler():
    #This function is for the heroku scheduler add-on
    global scheduler

    try:
        configure_scheduler()
        scheduler.start()
    except:
        pass
    scheduler.print_jobs()

    return None

'''
account_id = "acct_1EKc67BuN2uG9scf"
print(str(account_id))
balance = stripe.Balance.retrieve(
  stripe_account=account_id
)
print("Balance is: " + str(balance))
print("The integer is: " + str(balance.available[0].amount)) 
'''
