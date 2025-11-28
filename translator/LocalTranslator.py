from googletrans import Translator

class LocalTransor:
    def __init__(self):
        self._translator = Translator()

    def translate(self, input:str, src:str = None, dest:str = None):
        if dest == None:
            result = self._translator.translate(input, dest='zh-cn')
        else:
            result = self._translator.translate(input, dest=dest, src=src)
        return result.text