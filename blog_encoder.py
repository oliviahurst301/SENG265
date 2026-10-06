import json
from blogging.blog import Blog

# json encoder for Blog
class BlogEncoder(json.JSONEncoder):

    # extended class
    def default(self, obj):
        """
        Encodes collection of Blogs{} to store in a json file.
        Returns desired blog dict
        """

        # return Blog instance for storage
        if isinstance(obj, Blog):
            return {"__type__": "Blog", "id": obj.id, "name": obj.name, "url": obj.url, "email": obj.email}

        return super().default(obj)