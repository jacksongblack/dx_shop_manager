def handler(func):
    def index_params_handler(cls, request):
        query_keys = func(cls, request)
        params = {}
        query_dict = dict(request.GET)
        for key in query_keys:
            if key in query_dict.keys() and len(query_dict[key][0]) != 0:
                params[key] = query_dict[key][0]

        if params:
            data = cls.objects.filter(**params)
        else:
            data = cls.objects.all()
        return data

    return index_params_handler