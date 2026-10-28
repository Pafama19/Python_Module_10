
import time
from collections.abc import Callable
from functools import wraps
from typing import Any


def spell_timer(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        print(f"Casting {func.__name__}...")
        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        elapsed = time.perf_counter() - start_time
        print(f"Spell completed in {elapsed:.3f} seconds")

        return result

    return wrapper


def power_validator(min_power: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            power = kwargs.get(
                "power",
                args[-1] if args else None
            )

            if power is None or power < min_power:
                return "Insufficient power for this spell"

            return func(*args, **kwargs)

        return wrapper

    return decorator


def retry_spell(max_attempts: int) -> Callable:
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            for attempt in range(1, max_attempts + 1):
                try:
                    return func(*args, **kwargs)
                except Exception:
                    if attempt < max_attempts:
                        print(
                            "Spell failed, retrying... "
                            f"(attempt {attempt}/{max_attempts})"
                        )

            return (
                "Spell casting failed after "
                f"{max_attempts} attempts"
            )

        return wrapper

    return decorator


class MageGuild:
    @staticmethod
    def validate_mage_name(name: str) -> bool:
        return len(name) >= 3 and name.replace(" ", "").isalpha()

    @power_validator(min_power=10)
    def cast_spell(self, spell_name: str, power: int) -> str:
        return (
            f"Successfully cast {spell_name} "
            f"with {power} power"
        )


@spell_timer
def fireball() -> str:
    time.sleep(0.1)
    return "Fireball cast!"


@retry_spell(max_attempts=3)
def failing_spell() -> str:
    raise RuntimeError("Spell failed")


@retry_spell(max_attempts=3)
def war_cry() -> str:
    return "Waaaaaaagh spelled !"


if __name__ == "__main__":
    print("Testing spell timer...")
    print(f"Result: {fireball()}")

    print("\nTesting retrying spell...")
    print(failing_spell())
    print(war_cry())

    print("\nTesting MageGuild...")
    guild = MageGuild()

    print(MageGuild.validate_mage_name("Gandalf"))
    print(MageGuild.validate_mage_name("G1"))
    print(guild.cast_spell("Lightning", 15))
    print(guild.cast_spell("Lightning", 5))
