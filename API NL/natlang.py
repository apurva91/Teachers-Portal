from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from oauth2client.client import GoogleCredentials
credentials = GoogleCredentials.get_application_default()

contents = []
while True:
    try:
        line = input()
    except EOFError:
        break
    contents.append(line)
text = ' '.join(contents)

def language_analysis(text):
    client=language.LanguageServiceClient()

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT
    )
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    global sent_score 
    global sent_mag
    sent_score=sentiment.score
    sent_mag=sentiment.magnitude

def entities_text(text):
    """Detects entities in the text."""
    client = language.LanguageServiceClient()

    # if isinstance(text, six.binary_type):
    #     text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    # entity types from enums.Entity.Type
    entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                   'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')
    
    isMeeting=0
    isReview=0
    isDoubt=0
    isPromotion=0

    naam=""
    loc=""
    eve=""
    course=""
    post=""
    for entity in entities:
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
        print(u'{:<16}: {}'.format('metadata', entity.metadata))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-')))
    #     if entity.type==4:
    #         meet=1
    #         eve=entity.name
    #     if entity.type==2:
    #         loc=entity.name
    #     if entity.type==1:
    #     	naam=entity.name
    # if(meet==1):
    # 	print("\n\nHey "+naam+",You have a " +eve+" at "+loc + "\n" )
        if entity.name.lower()=='review' or entity.name.lower()=='feedback':
            isReview=1
        if entity.name.lower()=='meeting':
            isMeeting=1
        if entity.name.lower()=='doubt':
            isDoubt=1
        if entity.name.lower()=='promotion':
            isPromotion=1
        if entity.type==1 and entity.salience>0.1:
            naam=entity.name
        if entity.type==4:
            eve=entity.name
        if entity.type==2:
            loc=entity.name
        if entity.type==1 and 0.04<entity.salience<0.06:
            post=entity.name

    if isReview==1:
        if sent_score<0:
            print('You have a Critical Review from '+naam)
        if sent_score>0.40 and sent_mag>1:
            print('You have 1 Positive review from '+naam)

    if isMeeting==1:
        print("Hey "+naam+",You have a " +eve+" at "+loc + " on 29/11/2017 ")
    if isDoubt==1:
        print('You have 1 doubt')
    if isPromotion==1 and sent_score>0.35:
        print(naam)
        print('Congratulations,'+naam+' you have been promoted to '+post)
     




language_analysis(text)
entities_text(text)
print(sent_score)
print(sent_mag)