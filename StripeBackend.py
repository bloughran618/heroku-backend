import stripe
# import time
from flask import Flask, session, jsonify, request
import sys


stripe.api_key = "sk_test_BPL2Sy81u9355r3GlN4XKG2t"
stripe.api_version = "2018-05-21"
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
def createAccount():
    account = stripe.Account.create(
        country="US",
        type="custom"
    )
    account_id = account.id
    return account_id


def updatePersonalInfo(id, first, last, addressLine1, addressLine2, city, state, zip, dobDay, dobMonth, dobYear, last4):
    account = stripe.Account.retrieve(id)

    account.legal_entity.type = "individual"
    account.legal_entity.first_name = first
    account.legal_entity.last_name = last
    account.legal_entity.personal_address.line1 = addressLine1
    account.legal_entity.personal_address.line2 = addressLine2
    account.legal_entity.personal_address.city = city
    account.legal_entity.personal_address.state = state
    account.legal_entity.personal_address.postal_code = zip
    account.legal_entity.dob.day = dobDay
    account.legal_entity.dob.month = dobMonth
    account.legal_entity.dob.year = dobYear
    account.legal_entity.ssn_last_4 = last4

    account.save()


def acceptServicesAgreement(id, ip):
    account = stripe.Account.retrieve(id)
    account.tos_acceptance.date = int(time.time())
    account.tos_acceptance.ip = ip
    account.save()


def deleteAccount(id):
    account = stripe.Account.retrieve(id)
    account.delete()


def create_customer():
    customer = stripe.Customer.create()
    customer_id = customer.id
    return customer_id


def add_card_to_customer(customer_id):
    customer = stripe.Customer.retrieve(customer_id)
    #TODO: figure out how to get the source from swift
    customer.sources.create(source="?")


def customer_pays_owner(customer, amount, destination):
    #TODO: Figure out how to get a source to test (see prev TODO)
    stripe.Charge.create(
        amount=amount,
        currency="usd",
        customer=customer,  # obtained with Stripe.js
        description="Testing..."
    )
    amount = int(round(amount*0.85)) # take some money for yourself :)
    stripe.Transfer.create(
        amount=amount,
        currency="usd",
        destination=destination
    )


def log_info(message):
    # sys.stdout.write(message)
    # sys.stdout.write(join("\n", message, "\n"))
    print(message)
    sys.stdout.flush()
    return message


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


@app.route('/account_id', methods=['POST'])
def create_account():
    log_info("Creating a account ID!!!")
    log_info("start creating account")
    account = stripe.Account.create(
        country="US",
        type="custom"
    )
    account_id = account.id
    log_info("end creating account")
    log_info("account id: " + account_id)
    # log_info("jsonify customer ID: " + jsonify(customer_id=customer_id).dumps())
    log_info("now return")
    return jsonify(account_id=account_id)


@app.route('/add_bank_info', methods=['POST'])
def add_bank_info():
    log_info("Adding tokenized bank info")
    log_info(request.form)
    account_id = request.form['account_id']
    log_info("Got one form info")
    account_token = request.form['account_token']
    log_info("form info successfully loaded")
    account = stripe.Account.retrieve(account_id)
    log_info("Found associated stripe account")
    account.account_token = account_token
    log_info("Successfully associated account token")
    return jsonify("success")


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



# account_id = createAccount()
# updatePersonalInfo(account_id, "Brian", "Loughran", "42 Ardmore Rd", None, "West Hartford", "CT", "06119",
#               "18", "06", "1995", "2427")

# customerPaysOwner("cus_E9HX8Dbeo9Af77", 1500, "acct_1DgdW8IWmP3kfqWG")


# print("Create an account and accept agreement")
# ip_address = "172.217.6.196"
# account_id = createAccount()
# updatePersonalInfo(account_id, "Joe", "Schmo", "150 Bishop St", None, "New Haven", "CT", "06119", "01", "01", "1996", "1234")
# acceptServicesAgreement(account_id, ip_address)
# print("done")

# print(issue_key()) # ????????

