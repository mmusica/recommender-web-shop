import pickle


class PickleUtil:
    def dump_binary_dict(self, name, dict):
        with (open(name, 'wb')) as f:
            pickle.dump(dict, f)

    def load_binary_dict(self, name):
        with (open(name, 'rb')) as f:
            return pickle.load(f)
