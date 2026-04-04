from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size' # Allows frontend to request ?page_size=20
    max_page_size = 100

    def get_paginated_response(self, data):
        """Customizing the response to include helpful metadata"""
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page_config.paginator.count,
            'total_pages': self.page_config.paginator.num_pages,
            'current_page': self.request.query_params.get('page', 1),
            'results': data
        })