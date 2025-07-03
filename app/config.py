import environ

# reading .env file
environ.Env.read_env()
env = environ.Env()

config = {
    "domain": env.str("DOMAIN"),
    "loki_url": env.str("LOKI_URL"),
    "service_name": env.str("SERVICE_NAME"),
    # "env": env.str("ENV"),
}
