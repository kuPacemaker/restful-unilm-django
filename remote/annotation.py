def terminate(final):
    def query_terminator(query_generator):
        def decorated(*args, **kwargs):
            for query in query_generator():
                yield query + final
        return decorated
    return query_terminator