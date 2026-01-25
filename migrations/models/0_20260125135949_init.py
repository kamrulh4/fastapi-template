from tortoise import BaseDBAsyncClient

RUN_IN_TRANSACTION = True


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "users" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "uid" UUID NOT NULL UNIQUE,
    "created_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "email" VARCHAR(255) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(255) NOT NULL,
    "first_name" VARCHAR(100),
    "last_name" VARCHAR(100),
    "kind" VARCHAR(11) NOT NULL DEFAULT 'USER',
    "is_active" BOOL NOT NULL DEFAULT True,
    "is_superuser" BOOL NOT NULL DEFAULT False
);
CREATE INDEX IF NOT EXISTS "idx_users_uid_6b1326" ON "users" ("uid");
CREATE INDEX IF NOT EXISTS "idx_users_email_133a6f" ON "users" ("email");
COMMENT ON COLUMN "users"."kind" IS 'ADMIN: ADMIN\nSUPER_ADMIN: SUPER_ADMIN\nUSER: USER\nOTHER: OTHER';
COMMENT ON TABLE "users" IS 'User model storing authentication and profile data.';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """


MODELS_STATE = (
    "eJztmG1v2jAQgP9KlE+d1KFCaVdV0yRomcpUoOJlm/qiyCQGLBI7jZ22qOK/z+ck5IVACy"
    "20k/hCyPnOuXvO8Tn3rDvMwjYv9Dj29FPtWafIwfJPSr6v6ch1YykIBOrbStGXGkqC+lx4"
    "yBRSOEA2x1JkYW56xBWEUVCFyTQ1hcYF8wgdasgXI0wFMREoaYhamuuxAbGxZiGBCjCxxU"
    "w5s9R+wxw+Jfc+NgQbYqkMod7cSTGhFn7CPLp1x8aAYNtKkSAWTKDkhpi4Slan4qdSBPf6"
    "hsls36GxsjsRI0Zn2oQKkA4xxR4SGKYXng+AqG/bIciIWeBprBK4mLCx8AD5NmAG6znKkT"
    "ABLRSZjEKGpDdcBTiEp3wtFcvfyieHx+UTqaI8mUm+TYPw4tgDQ0Wg2dWnalwiDjQUxpib"
    "nweu16uf55Pzc9H5UlwAoyzACNfbCOrfBz411bJRT4Kf8g99fahLiJ1dVNp7h8dfVJSMi6"
    "GnBhUShTJGZ3oYwjSQmCd4LkcEcXA+xbRlBqYVmhaiP+tAjQQx1fhtf6eFKWOwWtSehBlb"
    "wrRbb9Q63UrjCiJxOL+3FaJKtwYjJSWdZKR7QQqY3KuCHWw2ifan3r3Q4Fa7bjVr2UTN9L"
    "rXOvgk9x1mUPZoICuxuCJpBCaVWN+11kxs2nKX2A9NbOh8okZwQ1YkDLDn8lplzMaILqgX"
    "KcNMWvvSclOZzC/R77HPVVuty1TWqvVuOi/NXqNaa+8VVbqkEhE4WVJirNhBxJ4nejZCXj"
    "7OmUGGpHR9MwXkjS+Eg54MG9OhGEHdPTpagvV3pa0qiNTKLPNmOFQKxtIIR4iP5LbhIs4f"
    "mZezPBfDzDF9H6xb2Gk2D3ZAPC4MdbcC07TVWjjDNfhhNIsHB6+gKbUW0lRjaZo2WgNmym"
    "jHMmI5lt7nY6xR31Eo69InRE08hzSy3d6Lrvc6tfb8iVuvnDfqzVNNXW5pp3dVaxuhLHFz"
    "S8H8VIPfW9rqXsCNumS/HF+VjuJrslFcnIxiNheyvstPYvKQs65fOhfEdls8FswK3Cc+FU"
    "g23Hex54e9idWwpkx3B67pFBofg3HiEx4EfWSOH5FnGXMjrMQW6c4POSUnK0EUDRUiiBOi"
    "CjtNFewRc6Tn9KDCkf1lXSgU67zUhlqMfNck2nqT6AF7HFxaoeonTHbH0RlIeDVWgBiq/5"
    "8AN3Jqkk8UmOb0ZX51Ws0FzbbYJAOyR2WANxYxxb5mEy7uPifWJRQh6lRRieDtNSp/s1zP"
    "LlvVbFMFJqh+dHmZ/gONz/H9"
)
