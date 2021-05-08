from rest_framework.pagination import BasePagination, _positive_int
from rest_framework.response import Response


class Paginator(BasePagination):
    '''scroll pager
    the limit or all parameters are required
    when setting the limit parameter it is optional to set offset
    the parameter all has priority, when putting it it shows the records there
    '''
    param_limit = 'limit'
    param_offset = 'offset'
    param_all = 'all'
    total = 25
    limit = 100
    offset = 100
    all = False

    def paginate_queryset(self, queryset, request, view=None):
        self.total = queryset.count()
        self.all = self.get_all(request)
        if self.all:
            return list(queryset)

        self.limit = self.get_limit(request)

        if self.limit is None:
            return None

        self.offset = self.get_offset(request)

        if self.total == 0 or self.offset > self.total:
            return []

        return list(queryset[self.offset:self.offset + self.limit])

    def get_offset(self, request):
        try:
            return _positive_int(request.query_params[self.param_offset],)
        except (KeyError, ValueError):
            return 0

    def get_limit(self, request):
        try:
            return _positive_int(request.query_params[self.param_limit], )
        except (KeyError, ValueError):
            return 0

    def get_paginated_response(self, data):
        return Response(data={
            'total': self.total,
            'results': data
        })

    def get_all(self, request):
        try:
            return (request.query_params[self.param_all] == 'true' or
                    request.query_params[self.param_all] == 'True')
        except KeyError:
            return False


class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator
    def paginate_queryset(self, queryset):
        
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                   self.request, view=self)
    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)
