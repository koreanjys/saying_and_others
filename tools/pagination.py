# tools/pagination.py
"""
페이지 처리
"""
def paging(page, size, Table, statement):  # 페이징 처리 함수
    if page < 1:
        page = 1
    offset = (page - 1) * size
    statement = statement.where(Table.use_yn==1)  # 운영에 사용 여부 확인
    statement = statement.offset(offset).limit(size).order_by(Table.id.desc())
    return statement