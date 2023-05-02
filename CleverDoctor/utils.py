from rest_framework.pagination import PageNumberPagination  # 使用分页器
from rest_framework.response import Response


class My_page(PageNumberPagination):  # 分页器
    page_size = 5  # 每一页展示的数据
    page_query_param = 'page'  # 指定页码查询参数
    page_size_query_param = 'page_size'

    def get_page_size_from_query_param(self, request):
        page_size = request.query_params.get(self.page_size_query_param)
        return int(page_size) if page_size else self.page_size

    @property
    def count_pages(self):
        page_size = self.get_page_size_from_query_param(self.request)
        # 计算总页码数
        if self.page.paginator.count // page_size == self.page.paginator.count / page_size:
            return self.page.paginator.count // page_size
        else:
            return self.page.paginator.count // page_size + 1

    def get_paginated_response(self, data):
        # 页码详细信息
        return Response(dict([
            ("pages", self.count_pages()),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))