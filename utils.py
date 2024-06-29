import httpx
import config
from KeyStash import KeyStash
from exceptions import (
    GenerationFailedException,
    KeyStashEmptyException,
    RegenerateException,
)


async def generate_image(key_stash: KeyStash, body, max_retries=5):
    print("Starting generation")

    for i in range(max_retries):
        print("Try", i)

        try:
            return await _generate_image(key_stash, body)
        except RegenerateException:
            if i >= max_retries - 1:
                raise GenerationFailedException(config.PLAIN_ERROR)
        except (KeyStashEmptyException, GenerationFailedException) as e:
            raise e
        except Exception as e:
            raise GenerationFailedException(config.PLAIN_ERROR)


async def _generate_image(key_stash: KeyStash, body):
    key = key_stash.next_key()
    if key == None:
        raise KeyStashEmptyException()

    print("Key:", trim_key(key))

    async with httpx.AsyncClient() as client:
        headers = {"Authorization": f"Bearer {key}"}
        response = await client.post(
            config.BASE_URL + "/images/generations",
            json=body,
            headers=headers,
            timeout=config.TIMEOUT,
        )

    try:
        response.raise_for_status()
    except:
        error = response.json().get("error", {})

        code = error.get("code", None)
        detail = error.get("message", None)

        print("Generation failed:", code)

        if code == None:
            raise GenerationFailedException(config.PLAIN_ERROR)

        # TODO отправить запрос заново
        if not is_safe_status(code):
            print(trim_key(key), "press f")

            key_stash.update_status(key, code)
            raise RegenerateException()

        raise GenerationFailedException(detail, response.status_code)

    return response.json()


def is_safe_status(code):
    return code in (
        "empty_array",
        "invalid_type",
        "invalid_value",
        "model_not_found",
        "unsupported_country_region_territory",
        "context_length_exceeded",
        "rate_limit_exceeded",
        "content_policy_violation",
    )


def trim_key(key):
    return "***" + key[-5:]
