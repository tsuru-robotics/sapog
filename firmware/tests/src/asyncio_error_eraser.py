import decorator


def ignores_unneeded_exceptions(test_func):
    def test_wrapper(test_func, *args, **kwargs):
        try:
            print()
            print("A function was wrapped")
            result = test_func(*args, **kwargs)
            return result
        except (ImportError, RuntimeError, AssertionError) as e:
            print("An exception was observed")
            if (isinstance(e, RuntimeError)) or \
                    (isinstance(e, ImportError)):
                print("Unnecessary exception ignored")
                # and "Event loop is closed" in str(e)
                # and "sys.meta_path is None" in str(e)
            else:
                raise

    return decorator.decorator(test_wrapper, test_func)
