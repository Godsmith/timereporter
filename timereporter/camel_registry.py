from camel import CamelRegistry
from collections import defaultdict

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


@camelRegistry.dumper(type, 'type', version=1)
def _dump_type(type_):
    return dict(
        name=type_.__name__,
        module=type_.__module__
    )


@camelRegistry.loader('type', version=1)
def _load_type(data, version):
    import importlib
    module_ = importlib.import_module(data['module'])
    return getattr(module_, data['name'])
