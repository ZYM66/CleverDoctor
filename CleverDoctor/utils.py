from rest_framework.pagination import PageNumberPagination  # 使用分页器
from rest_framework.response import Response


class My_page(PageNumberPagination):  # 分页器
    page_size = 4  # 每一页展示的数据
    page_query_param = 'page'  # 指定页码查询参数

    @property
    def count_pages(self):
        # 计算总页码数
        if self.page.paginator.count // self.page_size == self.page.paginator.count / self.page_size:
            return self.page.paginator.count // self.page_size
        else:
            return self.page.paginator.count // self.page_size + 1

    def get_paginated_response(self, data):
        # 页码详细信息
        return Response(dict([
            ("pages", self.count_pages()),
            ('count', self.page.paginator.count),
            ('next', self.get_next_link()),
            ('previous', self.get_previous_link()),
            ('results', data)
        ]))