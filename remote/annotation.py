def terminate(final):
    def query_terminator(query_generator):
        def decorated(*args, **kwargs):
            self = args[0]
            for query in query_generator(self):
                yield query + final
        return decorated
    return query_terminator