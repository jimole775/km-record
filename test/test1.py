from datetime import datetime
import re
str_date = str(datetime.now())
res = re.sub(r'[-:\.]', '', str_date).replace(r' ', '-')
print(res)