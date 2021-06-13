from flask.json import JSONEncoder
from bson import ObjectId

class CustomJSONEncoder(JSONEncoder):
    """A Class that inherits the default JSONEncoder class.
    jsonify() function can use this encoder.

    Args:
        JSONEncoder: 
    """
    def default(self, o):
        """This function overrides the default implementation of the JSONEncoder Class.
        This is done to handle encoding of the ObjectId used as a primary key by mongodb.
        """
        if isinstance(o, ObjectId):
            return str(o)
        return JSONEncoder.default(self, o)
