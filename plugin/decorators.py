def index_params_handler(request):
        params = {}
        query_dict = dict(request.GET)
        for key in query_keys:
            if key in query_dict.keys() and len(query_dict[key][0]) != 0:
                params[key] = query_dict[key][0]

        if params:
            data = cls.objects.filter(**params)
        else:
            data = cls.objects.all()