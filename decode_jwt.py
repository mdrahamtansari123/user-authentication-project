import jwt

jwt_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTcxOTU1MDczNywiaWF0IjoxNzE5NDY0MzM3LCJqdGkiOiI0OWUwMjI4MTg5YTI0OGRkODQ0Y2VjNDAxMzE0NzY5MSIsInVzZXJfaWQiOjF9.M8zMNsVx2LDqe3cMcU6FRlHQPgTye5ZLs4GsMuX_rI4"
key = "django-insecure-vj%@(7l$#e=e5r&un+l==a(04rzcr2gbl%eh41mq9!z%8^^xjr"

payload = jwt.decode(jwt=jwt_token, key=key, algorithms=["HS256"])
print(payload)