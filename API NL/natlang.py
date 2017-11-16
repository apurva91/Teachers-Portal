from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

from oauth2client.client import GoogleCredentials
credentials = GoogleCredentials.get_application_default()


def language_analysis(text):
    client=language.LanguageServiceClient()

    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT
    )
    sentiment = client.analyze_sentiment(document=document).document_sentiment

    print('Text: {}'.format(text))
    print('Sentiment: {}, {}'.format(sentiment.score, sentiment.magnitude))

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
    
    naam=""
    loc=""
    meet=0
    eve=""
    for entity in entities:
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
        print(u'{:<16}: {}'.format('metadata', entity.metadata))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url',
              entity.metadata.get('wikipedia_url', '-')))
        if entity.type==4:
            meet=1
            eve=entity.name
        if entity.type==2:
            loc=entity.name
        if entity.type==1:
        	naam=entity.name
    if(meet==1):
    	print("\n\nHey "+naam+",You have a " +eve+" at "+loc + "\n" )

contents = []
while True:
    try:
        line = input()
    except EOFError:
        break
    contents.append(line)
text = ' '.join(contents)

language_analysis(text)
entities_text(text)