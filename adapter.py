import json


class _InvalidInput(Exception):
    pass


def _reject_constant(value):
    raise _InvalidInput()


def _first_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key not in result:
            result[key] = value
    return result


def _unique_pairs(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise _InvalidInput()
        result[key] = value
    return result


def _decode(raw, **options):
    try:
        return json.loads(raw, **options)
    except ValueError as exc:
        raise _InvalidInput() from exc


def _valid(call):
    if type(call) is not dict or set(call) != {'name', 'arguments'}:
        return False
    if call['name'] not in ('save_draft', 'send_note'):
        return False
    args = call['arguments']
    return (type(args) is dict
            and set(args) == {'folder', 'replace', 'text'}
            and args['folder'] in ('draft', 'outbox')
            and type(args['replace']) is bool
            and type(args['text']) is str
            and 1 <= len(args['text']) <= 128)


def handle(raw, policy, execute):
    if policy not in ('first_then_last', 'strict_unique', 'parse_once'):
        raise ValueError('unknown policy')

    invalid = {'status': 'invalid', 'approved': None, 'executed': None}
    if type(raw) is not str:
        return invalid
    try:
        options = {'parse_constant': _reject_constant}
        if policy == 'first_then_last':
            options['object_pairs_hook'] = _first_pairs
        elif policy == 'strict_unique':
            options['object_pairs_hook'] = _unique_pairs
        approved = _decode(raw, **options)
        if not _valid(approved):
            return invalid
        args = approved['arguments']
        if (approved['name'] != 'save_draft' or args['folder'] != 'draft'
                or args['replace']):
            return {'status': 'denied', 'approved': approved, 'executed': None}
        if policy == 'first_then_last':
            executed = _decode(raw, parse_constant=_reject_constant)
            if not _valid(executed):
                return invalid
        else:
            executed = approved
    except (json.JSONDecodeError, _InvalidInput, RecursionError):
        return invalid

    execute(executed)
    return {'status': 'executed', 'approved': approved, 'executed': executed}
