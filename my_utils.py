#!/usr/bin/env python3
import argparse
import sys

try:
    from loguru import logger
except ImportError:
    print("Please install the 'loguru' package by running 'pip install loguru'")
    sys.exit(1)


def parse_args() -> argparse.Namespace:
    """
    Parses debug and test arguments.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Parse command line arguments.")
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable debug logging",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        default=False,
        help="Run tests",
    )
    return parser.parse_args()


def setup_logging(log_level: str = "INFO") -> logger:
    """
    Setup loguru logging.

    Args:
        log_level (str): The log level to be set. Default = "INFO"

    Returns:
        logger: Loguru logger object.
    """
    # Define valid log levels
    valid_log_levels = [
        "TRACE",
        "DEBUG",
        "INFO",
        "SUCCESS",
        "WARNING",
        "ERROR",
        "CRITICAL",
    ]

    # Validate the log level
    if log_level.upper() not in valid_log_levels:
        raise ValueError(
            f"Invalid log level: {log_level}. Valid log levels are: {', '.join(valid_log_levels)}"
        )

    # Remove all built-in handlers
    logger.remove()
    # Set custom loguru format
    fmt = (
        "<level>{time:YYYY-MM-DD hh:mm:ss A}</level> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{"
        "function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level> "
    )
    # Set the log level
    logger.add(sys.stderr, format=fmt, level=log_level.upper())

    # Test logging
    logger.debug("Logging setup complete with level: {}", log_level.upper())

    return logger


if __name__ == "__main__":
    args = parse_args()
    logger = setup_logging("DEBUG" if args.debug else "INFO")
    if args.test:
        logger.info("Running tests...")
