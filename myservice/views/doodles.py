from flakon import JsonBlueprint
from flask import request, jsonify, abort
from myservice.classes.poll import Poll, NonExistingOptionException, UserAlreadyVotedException

doodles = JsonBlueprint('doodles', __name__)

_ACTIVEPOLLS = {} # list of created polls
_POLLNUMBER = 0 # index of the last created poll

@doodles.route() #TODO: complete the decoration
def all_polls():

    if request.method == 'POST':
        result = create_doodle(request)

    elif request.method == 'GET':
        result = get_all_doodles(request)
    
    return result


@doodles.route() #TODO: complete the decoration
def single_poll(id):
    global _ACTIVEPOLLS
    result = ""

    exist_poll(id) # check if the Doodle is an existing one

    if request.method == 'GET': # retrieve a poll
        result = jsonify(_ACTIVEPOLLS[id].serialize())

    elif request.method == 'DELETE': 
        #TODO: delete a poll and get back winners

    elif request.method == 'PUT': 
        #TODO: vote in a poll


    return result

@doodles.route() #TODO: complete the decoration
def person_poll(id, person):
    
    #TODO: check if the Doodle exists
    
    if request.method == 'GET':
        #TODO: retrieve all preferences cast from <person> in poll <id>
    if request.method == 'DELETE':
        #TODO: delete all preferences cast from <person> in poll <id>

    return result
       

def vote(id, request):
    result = ""
    #TO DO: extract person and option fields from the JSON request

    try:
        # TODO: cast a vote from person in  _ACTIVEPOLLS[id]
    except UserAlreadyVotedException:
        abort(400) # Bad Request
    except NonExistingOptionException:
        # TODO: manage the NonExistingOptionException

    return result


def create_doodle(request):
    global _ACTIVEPOLLS, _POLLNUMBER
    #TODO: create a new poll in _ACTIVEPOLLS based on the input JSON. Update _POLLNUMBER by incrementing it.
    
    return jsonify({'pollnumber': _POLLNUMBER})


def get_all_doodles(request):
    global _ACTIVEPOLLS
    return jsonify(activepolls = [e.serialize() for e in _ACTIVEPOLLS.values()])

def exist_poll(id):
    if int(id) > _POLLNUMBER:
        abort(404) # error 404: Not Found, i.e. wrong URL, resource does not exist
    elif not(id in _ACTIVEPOLLS):
        abort(410) # error 410: Gone, i.e. it existed but it's not there anymore