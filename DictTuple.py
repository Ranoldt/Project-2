from mynamedtuple import mynamedtuple
from typing import Tuple, Dict, Any

class DictTuple():
    def __init__(self, dicttuples: Tuple[Dict[str, Any],...]):
        assert type(dicttuples) is tuple, 'Arguments must be tuple.'
        for element in dicttuples:
            assert type(element) is dict
            assert len(element) != 0

        self.dt = dicttuples

    
