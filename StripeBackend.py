import sys
import os
import stripe
import time
from flask import Flask, session, jsonify, request, Response
import sys
import json
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


# def accept_services_agreement(id, ip):
#     account = stripe.Account.retrieve(id)
#     account.tos_acceptance.date = int(time.time())
#     account.tos_acceptance.ip = ip
#     account.save()
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

@app.route('/pay_owner', methods=['POST'])
def pay_owner():
    destination_id = request.form['destination_id']
    amount = request.form['amount']

    log_info("creating transfer")
    stripe.Transfer.create(
        amount=amount,
        currency="usd",
        destination=destination_id
    )
    log_info("success")
    return jsonify(success="success")


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
        charge = stripe.Charge.create(
            amount = amount, # remember that this is in cents
            currency = "usd",
            customer = customer_token,
            source = source,
            description = "Spotbird Parking Fee"
        )
    except stripe.error as e:
        return jsonify(message="Error creating charge: " + e.message)
    return jsonify(message="Charge successfully created")


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


# should not do anything, just keepin it around in case I need it in the future
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


@app.route('/save_ssn', methods=['POST'])
def save_ssn():
    account_id = request.form['account_id']
    account = stripe.Account.retrieve(account_id)
    encrypted_ssn = int(request.form['encrypted_ssn'])
    decrypted_ssn = int((encrypted_ssn - 373587911) / 179424691)
    print("SSN decrypted")
    account["individual"]["id_number"] = decrypted_ssn
    account.save()
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


def fetch_picture_from_firebase():
    config = {
        "apiKey": os.environ.get("firebase_api"),
        "authDomain": os.environ.get("firebase_auth_domain"),
        "databaseURL": os.environ.get("firabase_database_url"),
        "storageBucket": os.environ.get("firebase_storage_bucket"),
        "serviceAccount": os.environ.get("firebase_services_account")
    }
    fb = pyrebase.initialize_app(config)
    if fb is None:
        log_info("fb is none: " + str(fb))
    else:
        log_info("fb is not none...")
        log_info("fb is: " + str(fb))
    email = os.environ.get("firebase_email")
    pw = os.environ.get("firebase_email_password")
    auth = fb.auth()
    user = auth.sign_in_with_email_and_password(email=email, password=pw)
    try:
        db = fb.database()
    except Exception as e:
        log_info("exception is: " + str(e))
    storage = fb.storage()
    log_info("Storage works tho...")
    Brian = db.child("User").child("-LbQoDVfuiRm7NBsWOR9").child("id").get(user['idToken']).val()
    print(Brian)
    return


# account_id = createAccount()
# updatePersonalInfo(account_id, "Brian", "Loughran", "42 Ardmore Rd", None, "West Hartford", "CT", "06119",
#               "18", "06", "1995", "2427")

# customer_pays_owner("cus_E9HX8Dbeo9Af77", "acct_1DgdW8IWmP3kfqWG", 1500)

# print(issue_key()) # ????????

# account = stripe.Account.retrieve("acct_1EIRBeFqSeXgmrEv")
# print(account)
# # account.individual.id_number = 123456789
# account["individual"]["id_number"] = 123456789
# account.save()
# print("-------------------------------------------------------------------------\n"
#       + str(account))

# try:
#     import firebase
# except Exception as e:
#     log_info(" This is the exception: \n" + str(e))

fetch_picture_from_firebase()
