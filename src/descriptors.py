class ValidatedAttribute:
    """
    Data descriptor для валидации атрибутов
    """

    def __init__(self, validator):
        self.validator = validator
        self.data = {}

    def __get__(self, obj, objtype=None):
        if obj is None:
            return self
        return self.data.get(id(obj), None)

    def __set__(self, obj, value):
        # Валидация значения перед установкой
        validated_value = self.validator(value)
        self.data[id(obj)] = validated_value

    def __delete__(self, obj):
        raise AttributeError("Атрибут не может быть удален")
