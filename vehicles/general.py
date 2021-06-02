import math
def paginate(data, page, per_page=8):
    per_page_data_length = per_page
    data_length = len(data)
    data_page_length = math.ceil(data_length/per_page_data_length)
    if page>data_page_length or page<1:
        result = []
        return result
    else:
        paginated_data = data[(page-1)*per_page_data_length:page*per_page_data_length]
        return paginated_data

