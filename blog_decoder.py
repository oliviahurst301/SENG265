import json
from blogging.blog import Blog

# json decoder for Blog
class BlogDecoder(json.JSONDecoder):

    # constructor for the extended class
    def __init__(self, *args, **kwargs):
        super().__init__(object_hook=self.object_hook, *args, **kwargs)


    def object_hook(self, dct):
        """
        Decodes collection of blogs dict in a json file.
        Returns Blog() object.
        """

        # return instance of Blog
        if '__type__' in dct and dct['__type__'] == 'Blog':
            return Blog(dct['id'], dct['name'], dct['url'], dct['email'])

        return dct