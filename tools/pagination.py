# tools/pagination.py
"""
페이지 처리
"""
def paging(page, size, Table, statement):  # 페이징 처리 함수
    if page < 1:
        page = 1
    offset = (page - 1) * size
    # statement = statement.where(Table.use_yn==1)  # 운영에 사용 여부 확인
    statement = statement.offset(offset).limit(size).order_by(Table.id.desc())
    return statement


"""
# 토탈 페이지 확인(추후 도구로 만들기)
    total_record = session.exec(select(func.count()).select_from(statement)).one()
    total_page = (total_record // size) + bool(total_record % size)
    if p > total_page:
        p = total_page
"""