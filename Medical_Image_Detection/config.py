from dotenv import dotenv_values

values_env = dotenv_values('.env')

GOOGLE_API_KEY = values_env['GOOGLE_API_KEY']