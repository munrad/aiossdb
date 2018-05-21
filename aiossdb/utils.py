import asyncio
from .log import logger


COMMANDS = {
    'auth': lambda x, **kwargs: x,
    'dbsize': lambda x, **kwargs: x,
    'flushdb': lambda x, **kwargs: x,
    'info': lambda x, **kwargs: x,
    'slaveof': lambda x, **kwargs: x,
    'list_allow_ip': lambda x, **kwargs: x,
    'add_allow_ip': lambda x, **kwargs: x,
    'del_allow_ip': lambda x, **kwargs: x,
    'list_deny_ip': lambda x, **kwargs: x,
    'add_deny_ip': lambda x, **kwargs: x,
    'del_deny_ip': lambda x, **kwargs: x,
    'set': lambda x, **kwargs: x,
    'setx': lambda x, **kwargs: x,
    'setnx': lambda x, **kwargs: x,
    'expire': lambda x, **kwargs: x,
    'ttl': lambda x, **kwargs: x,
    'get': lambda x, **kwargs: x,
    'getset': lambda x, **kwargs: x,
    'del': lambda x, **kwargs: x,
    'incr': lambda x, **kwargs: x,
    'exists': lambda x, **kwargs: x,
    'getbit': lambda x, **kwargs: x,
    'setbit': lambda x, **kwargs: x,
    'bitcount': lambda x, **kwargs: x,
    'countbit': lambda x, **kwargs: x,
    'substr': lambda x, **kwargs: x,
    'strlen': lambda x, **kwargs: x,
    'keys': lambda x, **kwargs: x,
    'rkeys': lambda x, **kwargs: x,
    'scan': lambda x, **kwargs: x,
    'rscan': lambda x, **kwargs: x,
    'multi_set': lambda x, **kwargs: x,
    'multi_get': lambda x, **kwargs: x,
    'multi_del': lambda x, **kwargs: x,
    'hset': lambda x, **kwargs: x,
    'hget': lambda x, **kwargs: x,
    'hdel': lambda x, **kwargs: x,
    'hincr': lambda x, **kwargs: x,
    'hexists': lambda x, **kwargs: to_bool(x),
    'hsize': lambda x, **kwargs: x,
    'hlist': lambda x, **kwargs: x,
    'hrlist': lambda x, **kwargs: x,
    'hkeys': lambda x, **kwargs: x,
    'hgetall': lambda x, **kwargs: list2dict(x, **kwargs),
    'hscan': lambda x, **kwargs: x,
    'hrscan': lambda x, **kwargs: x,
    'hclear': lambda x, **kwargs: x,
    'multi_hset': lambda x, **kwargs: x,
    'multi_hget': lambda x, **kwargs: list2dict(x, **kwargs),
    'multi_hdel': lambda x, **kwargs: x,
    'zset': lambda x, **kwargs: x,
    'zget': lambda x, **kwargs: x,
    'zdel': lambda x, **kwargs: x,
    'zincr': lambda x, **kwargs: x,
    'zexists': lambda x, **kwargs: x,
    'zsize': lambda x, **kwargs: x,
    'zlist': lambda x, **kwargs: x,
    'zrlist': lambda x, **kwargs: x,
    'zkeys': lambda x, **kwargs: x,
    'zscan': lambda x, **kwargs: x,
    'zrscan': lambda x, **kwargs: x,
    'zrank': lambda x, **kwargs: x,
    'zrrank': lambda x, **kwargs: x,
    'zrange': lambda x, **kwargs: x,
    'zrrange': lambda x, **kwargs: x,
    'zclear': lambda x, **kwargs: x,
    'zcount': lambda x, **kwargs: x,
    'zsum': lambda x, **kwargs: x,
    'zavg': lambda x, **kwargs: x,
    'zremrangebyrank': lambda x, **kwargs: x,
    'zremrangebyscore': lambda x, **kwargs: x,
    'zpop_front': lambda x, **kwargs: x,
    'zpop_back': lambda x, **kwargs: x,
    'multi_zset': lambda x, **kwargs: x,
    'multi_zget': lambda x, **kwargs: x,
    'multi_zdel': lambda x, **kwargs: x,
    'qpush_front': lambda x, **kwargs: x,
    'qpush_back': lambda x, **kwargs: x,
    'qpop_front': lambda x, **kwargs: x,
    'qpop_back': lambda x, **kwargs: x,
    'qpush': lambda x, **kwargs: x,
    'qpop': lambda x, **kwargs: x,
    'qfront': lambda x, **kwargs: x,
    'qback': lambda x, **kwargs: x,
    'qsize': lambda x, **kwargs: x,
    'qclear': lambda x, **kwargs: x,
    'qget': lambda x, **kwargs: x,
    'qset': lambda x, **kwargs: x,
    'qrange': lambda x, **kwargs: x,
    'qslice': lambda x, **kwargs: x,
    'qtrim_front': lambda x, **kwargs: x,
    'qtrim_back': lambda x, **kwargs: x,
    'qlist': lambda x, **kwargs: x,
    'qrlist': lambda x, **kwargs: x,
}


def list2dict(value, encoding='utf-8', binary=False, strict=False):
    try:
        return {
            opt_decode(value[i], encoding, strict): opt_decode(value[i + 1], encoding, strict) if not binary else value[i + 1]
            for i in range(0, len(value), 2)
        }
    except UnicodeDecodeError as exc:
        return exc


def to_bool(value):
    try:
        return int(value) == 1
    except ValueError as exc:
        return exc


def opt_decode(value, encoding, strict):
    if encoding is None:
        return value

    try:
        return value.decode(encoding)
    except UnicodeDecodeError:
        if not strict:
            return value
        raise


def set_result(fut, result, *info):
    if fut.done():
        logger.debug("Waiter future is already done %r %r", fut, info)
        assert fut.cancelled(), (
            "waiting future is in wrong state", fut, result, info)
    else:
        fut.set_result(result)


def set_exception(fut, exception):
    if fut.done():
        logger.debug("Waiter future is already done %r", fut)
        assert fut.cancelled(), (
            "waiting future is in wrong state", fut, exception)
    else:
        fut.set_exception(exception)


async def wait_ok(fut):
    await fut
    return True


def format_result(command, obj, **kwargs):
    # TODO: Temporary here for all commands
    # TODO: Some commands need to return a list even for a single value
    if len(obj) == 1:
        obj = obj[0]

    return COMMANDS[command](obj, **kwargs)
