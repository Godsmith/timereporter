from camel import CamelRegistry
from collections import defaultdict
from mydatetime import timedelta

camelRegistry = CamelRegistry()


@camelRegistry.dumper(defaultdict, 'defaultdict', version=1)
def _dump_defaultdict(defaultdict_):
    return dict(
        default_factory=defaultdict_.default_factory,
        dict_=dict(defaultdict_)
    )


@camelRegistry.loader('defaultdict', version=1)
def _load_defaultdict(data, version):
    return defaultdict(data['default_factory'], data['dict_'])


@camelRegistry.dumper(type, 'defaultdict', version=1)
def _dump_defaultdict(defaultdict_):
    return dict(
        default_factory=defaultdict_.default_factory,
        dict_=dict(defaultdict_)
    )


@camelRegistry.loader('defaultdict', version=1)
def _load_defaultdict(data, version):
    return defaultdict(data['default_factory'], data['dict_'])
