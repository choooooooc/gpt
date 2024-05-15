# Health Assistant

## Setup and Configuration:
1. install MySQL, Python and corresponding Python packages in 'requirements.txt'.
2. Modify `config.py` and `openai_config.json`.
3. Add openai API key in openai_config.json

## Run
1. First in MySQL build a new database:
```mysql
create database flaskdb;
```
2. Add the MySQL password, database name in 'config.py' following the instructions
3. Run python:
```python
python3 register.py
```

## Dependencies 
See `requirements.txt`
