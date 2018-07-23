from SimpleXMLRPCServer import SimpleXMLRPCServer
from SimpleXMLRPCServer import SimpleXMLRPCRequestHandler
import spacy

server = SimpleXMLRPCServer(('localhost',8000))
server.register_introspection_functions()

# words that should not appear in an imperative sentence
non_imperative_words = {'i', 'please', 'you'}
# words handled poorly by spacy
problem_words = {'rework', 'update', 'fix'}

def is_imperative(msg):
    '''
    Check if a message is in the imperative tense
    '''
    nlp = spacy.load('en_core_web_sm')
    out = nlp(msg)

    #TODO find a more elegant solution for problem words
    if out[0].tag_ != 'VB':
        text = out[0].text.lower()
        if text not in problem_words:
            print('%s is not a simple verb' % text)
            return False

    # check if there is a subject
    for word in out:
        if word.text.lower() in non_imperative_words:
            return False

    return True
server.register_instance(is_imperative)

# main server loop
server.serve_forever()
