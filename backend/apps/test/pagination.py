from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class CustomPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

    def get_paginated_response(self, data):
        return Response({
            'data': {
                'tests': data,          # se renombrará en la vista según el tipo
                'total_tests': self.page.paginator.count,
                'total_pages': self.page.paginator.num_pages,
                'current_page': self.page.number,
                'page_size': self.page.paginator.per_page,
                'has_more': self.page.has_next(),
                'main_topics': [],
            },
            'stats': {
                'total_filtered_tests': self.page.paginator.count,
                'total_by_level': {},
            }
        })