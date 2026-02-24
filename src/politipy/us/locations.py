# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Imports                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
import pygris
import numpy as np

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                              Types                              <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                           Definitions                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
fips_codes = pygris.fips_codes()
state_name2code = {name.lower(): int(fips_codes[fips_codes.state_name==name].state_code.array[0]) for name in np.unique(fips_codes.state_name.array.astype(str))}
state_abbreviation2code = {abr.lower(): int(fips_codes[fips_codes.state==abr].state_code.array[0]) for abr in np.unique(fips_codes.state.array.astype(str))}
state2code = state_name2code | state_abbreviation2code
alternative_state_names = {
    "hawai'i": "hi",
    "hawaiian kingdom": "hi",
    "hawaiian islands": "hi",
    "virgin islands": "vi",
    "us virgin islands": "vi",
    "mariana islands": "mp",
    "mariana": "mp",
    "north mariana": "mp",
    "northern mariana": "mp",
    "samoa": "as",
    "d.c.": 'dc',
    "d.c": "dc",
    "us minor outlying islands": "um",
    "minor outlying islands": "um",
    "us minor": "um",
    "outlying islands": "um"
}

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Functions                            <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
def get_state_code(name: str):
    name = name.lower().strip()
    try:
        return state2code[name]
    except KeyError:
        if name in alternative_state_names.keys(): return state2code[alternative_state_names[name]]
        else: raise KeyError(f"{name} not an accepted name")

# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                            Decorators                           <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
# >-|===|>                             Classes                             <|===|-<
# !==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==!==
class State:
    def __init__(self, name: str):
        self.name = name
        self.code = get_state_code(name)
        self.counties = []
        self.house_districts = []
        self.senate_districts = []
        self.state_house_districts = []
        self.state_senate_districts = []
class County:
    def __init__(self, name: str, state = None):
        self.name = name
        self.state = State(state) if state else None
        self.code: tuple[int, int] = (self.state.code, )
oahu = County("Honolulu", state="HI")