
# Setup
#### Provide Environment variables
rename .env_template to .env

replace variables in .env
```
SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
ROOT_NAME = "secret_name"
ROOT_PASSWORD = secret_password
```

#### Create database: 
```
python setup_database.py
```


# Start Server:
```
python -m uvicorn main:app --reload
```