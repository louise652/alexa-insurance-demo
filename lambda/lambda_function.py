import logging
import decimal

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

##############################
# Builders
##############################


def build_PlainSpeech(body):
    speech = {}
    speech['type'] = 'PlainText'
    speech['text'] = body
    return speech


def build_response(message, session_attributes={}):
    response = {}
    response['version'] = '1.0'
    response['sessionAttributes'] = session_attributes
    response['response'] = message
    return response


def build_SimpleCard(title, body):
    card = {}
    card['type'] = 'Simple'
    card['title'] = title
    card['content'] = body
    return card


##############################
# Responses
##############################


def conversation(title, body, session_attributes):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = False
    return build_response(speechlet, session_attributes=session_attributes)


def statement(title, body):
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(body)
    speechlet['card'] = build_SimpleCard(title, body)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)


def continue_dialog():
    message = {}
    message['shouldEndSession'] = False
    message['directives'] = [{'type': 'Dialog.Delegate'}]
    return build_response(message)


##############################
# Custom Intents
##############################

def get_quote(event, context):
    
    dialog_state = event['request']['dialogState']
    logger.debug(dialog_state)
    
    if dialog_state in ("STARTED", "IN_PROGRESS"):
        return continue_dialog()

    elif dialog_state == "COMPLETED":
        return statement("Your quote", getMsg(event))

    else:
        return statement("get_quote", "No dialog")

def validate_numbers(income, liability, deductible):
    
    error_msg = ''
    
    if liability<=0:
        
        error_msg += 'Liability must be greater than zero. '
     
    if deductible<=0:
        
        error_msg += 'Deductible must be greater than zero. '
       
    if income<=0:
        
        error_msg += 'Income must be greater than zero. '
    
    if liability>25000:
        
        error_msg += 'We cannot provide an estimate for a liability of $' + str(int(liability)) + '. Please try reducing your liability or contact an agent. '
        
    if liability-deductible <= 0:
        error_msg += 'Your deductible is greater than your liability. '
    
    if (error_msg):
        error_msg +=  'Please check values and try again'
        return error_msg
    


def getMsg(event):

    user_input = event['request']['intent']['slots']
    name = user_input['Name']['value']
    businessType = user_input['BusinessType']['value']
    deductible = float(user_input['Deductible']['value'])
    income = float(user_input['Income']['value'])
    liability = float(user_input['Liability']['value'])
    location = user_input['Location']['value']

    logger.debug(
        'Name: %s, BusinessType: %s, Deductible: %s, Income: %s, Liability: %s, Location: %s'
            ,
        name,
        businessType,
        deductible,
        income,
        liability,
        location,
        )
    
      
    error_msg = validate_numbers(income, liability, deductible)
    
    if (error_msg):
        return error_msg
        
    else:
        premium = ((liability - deductible) /10) 
        
        #Rounding up premium to nearest dollar
        premium = decimal.Decimal(premium).quantize(decimal.Decimal('1'), rounding=decimal.ROUND_UP)
        return 'Thank you. Your annual quote is approximately $' + str(premium) + '. Please contact your agent to confirm pricing.'
    

##############################
# Required Intents
##############################


def default_intent(command):
    
    speechlet = {}
    speechlet['outputSpeech'] = build_PlainSpeech(command)
    speechlet['shouldEndSession'] = True
    return build_response(speechlet)

##############################
# Routing
##############################


def intent_router(event, context):
    intent = event['request']['intent']['name']

    # Required Intents

    if intent == "AMAZON.CancelIntent":
        return default_intent('Your quote has been cancelled.')

    if intent == "AMAZON.HelpIntent":
        return default_intent('Please ring your agent for help')

    if intent == "AMAZON.StopIntent":
        return default_intent('Your quote has been cancelled.')
    
    else:
        return get_quote(event, context)



##############################
# Program Entry
##############################


def lambda_handler(event, context):
    
    
    logger.debug( event['request']['type'])
    if event['request']['type'] == "LaunchRequest":
        return default_intent("To get a quote, please say: 'Alexa, ask insurance quick quote to get a quote'")

    elif event['request']['type'] == "IntentRequest":
        return intent_router(event, context)
