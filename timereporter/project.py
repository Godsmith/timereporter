from timereporter.camel_registry import camelRegistry


class Project:
    def __init__(self, name, work=True):
        self.name = name
        self.work = work

    def __str__(self):
        return self.name


@camelRegistry.dumper(Project, 'project', version=1)
def _dump_project(project):
    return dict(
        name=project.name,
        work=project.work
    )


@camelRegistry.loader('project', version=1)
def _load_project(data, version):
    return Project(**data)
