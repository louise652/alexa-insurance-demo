# alexa-insurance-demo
An Alexa skill which asks a series of questions and returns an insurance quote

Idea
Allow a user to get a quote estimate by talking to an Alexa-enabled device

Subtasks:

-Use Alexa Skill Kit to build the JSON interaction model

-Use AWS Lambda services to perform the processing and return a dummy premium

-Test the skill on an Alexa enabled device



Limitations
-Typical voice recognition issues- i.e. mishearing names

-Doesn't seem too good at recognizing large numbers

-Amazon currently do not allow financial transactions to take place via skills. However, it can be used to get a quote and signpost the user to a site so that they can continue to issuance if they want

-Only suitable for policies that do not require a large amount of UW questions

-Questions need to be precise and there should be a limited number of ways that the user can answer the question, all of which need to be programmed for


Future Improvements
-Liaise with insurance pricing platorm to determine what questions are necessary for a quote

-Hook into pricing to return a realistic quote. Currently, the premium returned by the skill is not valid and is only fit for demo/POC purposes. 

-Save quote details to a DynamoDB so that they can be retrieved at a later point

-Amend the response card to include a link where the customer can continue processing their quote
