class DottedDict(dict):
    __getattr__ = dict.__getitem__
    __setattr__ = dict.__setitem__
    __delattr__ = dict.__delitem__


def main():
    dotted = DottedDict({
        "a": 1,
        "b": 2,
        "c": 3
    })

    print(dotted.a)


if __name__ == "__main__":
    main()
