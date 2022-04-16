class EventHook(object): # вынести в отдельный модуль
    def __init__(self):
        self.__handlers = []

    def __iadd__(self, handler):
        self.__handlers.append(handler)
        return self

    def __isub__(self, handler):
        self.__handlers.remove(handler)
        return self

    def fire(self, *args, **keywargs):
        for handler in self.__handlers:
            handler(*args, **keywargs)

    def clearObjectHandlers(self, inObject):
        for theHandler in self.__handlers:
            if theHandler.im_self == inObject:
                self -= theHandler

"""
class Torpeda(): # модуль торпеда
    def __init__(self):
        self.onBaraBoom = EventHook()

def change_count(): # главный модуль
  print ('Cчет изменился !!!')

ObJ_Torpeda = Torpeda() # главный модуль
ObJ_Torpeda.onBaraBoom += change_count # главный модуль


ObJ_Torpeda.onBaraBoom.fire() # модуль торпеда - должен вызвать пересчет 
"""

