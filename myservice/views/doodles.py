from flakon import JsonBlueprint
from flask import request, jsonify, abort, json
from myservice.classes.poll import (
    Poll,
    NonExistingOptionException,
    UserAlreadyVotedException)

doodles = JsonBlueprint('doodles', __name__)

_ACTIVEPOLLS = {}   # list of created polls
_POLLNUMBER = 0  # index of the last created poll


@doodles.route('/doodles', methods=['GET', 'POST'])
def all_polls():
    if request.method == 'POST':
        result = create_doodle(request)

    elif request.method == 'GET':
        result = get_all_doodles(request)

    return result


@doodles.route('/doodles/<id>', methods=['GET', 'DELETE', 'PUT'])
def single_poll(id):
    global _ACTIVEPOLLS

    exist_poll(id)  # check if the Doodle is an existing one

    if request.method == 'GET':  # retrieve a poll
        result = jsonify(_ACTIVEPOLLS[id].serialize())

    elif request.method == 'DELETE':
        winners = _ACTIVEPOLLS[id].get_winners()
        del _ACTIVEPOLLS[id]
        result = jsonify(winners=winners)

    elif request.method == 'PUT':
        result = jsonify(winners=vote(id, request))

    return result


@doodles.route('/doodles/<id>/<person>', methods=['GET', 'DELETE'])
def person_poll(id, person):
    global _ACTIVEPOLLS

    exist_poll(id)  # check if the Doodle is an existing one
    poll = _ACTIVEPOLLS[id]

    if request.method == 'GET':
        result = jsonify(votedoptions=poll.get_voted_options(person))

    elif request.method == 'DELETE':
        result = jsonify(removed=poll.delete_voted_options(person))

    return result


def vote(id, request):
    global _ACTIVEPOLLS

    data_dict = json.loads(request.data)
    try:
        person = data_dict['person']
        option = data_dict['option']
        result = _ACTIVEPOLLS[id].vote(person, option)

    except KeyError:
        abort_bad_request()
    except UserAlreadyVotedException:
        abort_bad_request()
    except NonExistingOptionException:
        abort_bad_request()

    return result


def create_doodle(request):
    global _ACTIVEPOLLS, _POLLNUMBER

    data_dict = json.loads(request.data)
    try:
        title = data_dict['title']
        options = data_dict['options']

    except KeyError:
        abort_bad_request()

    _POLLNUMBER += 1
    _ACTIVEPOLLS[str(_POLLNUMBER)] = Poll(_POLLNUMBER, title, options)

    return jsonify({'pollnumber': _POLLNUMBER})


def get_all_doodles(request):
    global _ACTIVEPOLLS

    return jsonify(activepolls=[e.serialize() for e in _ACTIVEPOLLS.values()])


def exist_poll(id):
    if int(id) > _POLLNUMBER:
        abort_not_found()

    elif not(id in _ACTIVEPOLLS):
        abort_gone()


def abort_bad_request():
    abort(400)


def abort_not_found():
    abort(404)


def abort_gone():
    abort(410)
