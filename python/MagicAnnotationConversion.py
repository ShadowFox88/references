import inspect


class ConversionError(Exception):
    pass


def attempt_value_conversion(parameter, value):
    converter = parameter.annotation

    try:
        return converter(value)
    except Exception as error:
        raise error from ConversionError(f"Failed to convert {parameter.name}")


def magic(callback):
    def predicate(*args, **kwargs):
        index = 0
        converted_args = []
        converted_kwargs = {}
        signature = inspect.Signature.from_callable(callback)

        for parameter in signature.parameters.values():
            value: "any" = None
            name = parameter.name
            is_positional = parameter.kind in [parameter.POSITIONAL_ONLY, parameter.POSITIONAL_OR_KEYWORD]
            is_keyword = parameter.kind == parameter.KEYWORD_ONLY

            if is_positional:
                value = args[index]
                index += 1
            elif is_keyword:
                value = kwargs[name]

            converted = attempt_value_conversion(parameter, value)

            if is_positional:
                converted_args.append(converted)
            else:
                converted_kwargs[name] = converted

        return callback(*converted_args, **converted_kwargs)

    return predicate


@magic
def foo(bar: int, *, baz: list):
    print(f"bar ({type(bar)}) = {bar}", f"baz ({type(baz)}) = {baz}", sep="\n")


def main():
    baz =(
        "a",
        "b",
        "c"
    )

    foo("123", baz=baz)


if __name__ == "__main__":
    main()
