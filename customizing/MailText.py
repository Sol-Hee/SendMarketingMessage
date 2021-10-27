import datetime
today = datetime.date.today()

# 메일 제목
mail_subject = '메일 제목'

# 메일 본문
mail_text = '''
안녕하세요. 데이터팀입니다.
요청하신 OOO 자료 첨부 드립니다.

* 본 메일은 매일 오전 9:00 자동 발송 설정 되어있습니다.
'''

# To, From
from_addr = 'from_address'
to_addr = 'to_address'

# 첨부 파일명
file_name = f'마케팅 대상 회원 {today}.xlsx'