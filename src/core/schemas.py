from pydantic._internal._model_construction import ModelMetaclass

class OptionalSchemaMeta(ModelMetaclass):
    def __new__(mcs, name, bases, namespaces, **kwargs):
        annotations = namespaces.get('__annotations__', {})
        for base in bases:
            for key, value in base.__annotations__.items():
                if key not in annotations:
                    annotations[key] = value | None
        namespaces['__annotations__'] = annotations
        return super().__new__(mcs, name, bases, namespaces, **kwargs)