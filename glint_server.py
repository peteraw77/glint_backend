from xmlrpc.server import SimpleXMLRPCServer
from xmlrpc.server import SimpleXMLRPCRequestHandler
import spacy

# port to run the server from
port = 8000

server = SimpleXMLRPCServer(('localhost',port))
server.register_introspection_functions()

# words that should not appear in an imperative sentence
non_imperative_words = {'i', 'please', 'you'}

def is_imperative(msg):
    '''
    Check if a message is in the imperative tense
    '''
    nlp = spacy.load('en_core_web_sm')
    out = nlp(msg)

    if out[0].tag_ != 'VB':
        print('%s is not a simple verb' % out[0].text)
        return 0

    # check if there is a word that breaks imperative tense
    for word in out:
        if word.text.lower() in non_imperative_words:
            return 0

    return 1
server.register_function(is_imperative, 'is_imperative')

# main server loop
print('Starting server on port %d...' % port)
server.serve_forever()
