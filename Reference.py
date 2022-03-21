# class setup
class Reference:
    def __init__(self, attr):
        self.attr = attr

class ReferenceList:
    def __init__(self):
        self.allClasses = []

    def construct(self, refinstance):
        target_class = getattr(Reference, refinstance)
        instance = target_class()
        self.allClasses.append(instance)
