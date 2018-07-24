from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import spacy

# port to run the server from
port = 8000

server = SimpleXMLRPCServer(('localhost',port))
server.register_introspection_functions()

# words that should not appear in an imperative sentence
non_imperative_words = {'i', 'please', 'you', 'me'}
# words handled poorly by spacy
problem_words = {'rework', 'update', 'fix', 'terminate'}

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
            return 0

    # check if there is a subject
    for word in out:
        if word.text.lower() in non_imperative_words:
            return 0

    return 1
server.register_function(is_imperative, 'is_imperative')

# main server loop
print('Starting server on port %d...' % port)
server.serve_forever()
