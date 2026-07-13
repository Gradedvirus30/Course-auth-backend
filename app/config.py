"""Authentication configuration.

Replace ``SECRET_KEY`` with a long, randomly generated value before deploying.
"""

SECRET_KEY = "change-this-to-a-long-random-secret-before-production"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30