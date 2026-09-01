import io
import importlib
import logging

import telegram_test_bot as bot


def _synthetic_token() -> tuple[str, str, str]:
    numeric_part = "123456789"
    secret_part = "SyntheticSecretPart_" + "x" * 24
    return f"{numeric_part}:{secret_part}", numeric_part, secret_part


def test_http_client_loggers_are_warning_or_higher():
    bot.configure_secure_logging()
    assert logging.getLogger("httpx").getEffectiveLevel() >= logging.WARNING
    assert logging.getLogger("httpcore").getEffectiveLevel() >= logging.WARNING


def test_httpx_info_is_suppressed_but_redacted_warning_is_preserved():
    token, _, _ = _synthetic_token()
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    logger = logging.getLogger("httpx")
    logger.addHandler(handler)
    try:
        logger.info("GET https://api.telegram.org/bot%s/getUpdates", token)
        assert stream.getvalue() == ""
        logger.warning("Telegram transport warning for %s", token)
    finally:
        logger.removeHandler(handler)

    output = stream.getvalue()
    assert "Telegram transport warning" in output
    assert "[REDACTED]" in output
    assert token not in output


def test_error_arguments_and_exception_traceback_are_redacted():
    token, numeric_part, secret_part = _synthetic_token()
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    logger = logging.getLogger("tests.secure_logging")
    logger.handlers = [handler]
    logger.propagate = False
    logger.setLevel(logging.INFO)

    try:
        raise RuntimeError(f"request failed for {token}")
    except RuntimeError:
        logger.exception("Telegram ERROR token=%s", token)

    output = stream.getvalue()
    assert output.count("[REDACTED]") >= 2
    assert "Telegram ERROR" in output
    assert "RuntimeError" in output
    assert token not in output
    assert numeric_part not in output
    assert secret_part not in output


def test_structured_handler_receives_no_raw_exception_state():
    token, numeric_part, secret_part = _synthetic_token()

    class StructuredHandler(logging.Handler):
        record = None

        def emit(self, record):
            self.record = record

    handler = StructuredHandler()
    logger = logging.getLogger("tests.secure_logging.structured")
    logger.handlers = [handler]
    logger.propagate = False
    logger.setLevel(logging.ERROR)

    try:
        raise RuntimeError(f"structured exception for {token}")
    except RuntimeError:
        logger.exception("structured error token=%s", token)

    record = handler.record
    assert record is not None
    assert record.exc_info is None
    assert record.exc_text is not None
    assert "Traceback" in record.exc_text
    assert "RuntimeError" in record.exc_text
    assert "[REDACTED]" in record.exc_text
    serialized_fields = repr(record.__dict__)
    assert token not in serialized_fields
    assert numeric_part not in serialized_fields
    assert secret_part not in serialized_fields


def test_reload_keeps_one_factory_and_one_filter_per_root_handler():
    stream = io.StringIO()
    handler = logging.StreamHandler(stream)
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    factory = logging.getLogRecordFactory()
    try:
        for _ in range(3):
            importlib.reload(bot)
            assert logging.getLogRecordFactory() is factory

        for root_handler in root_logger.handlers:
            filters = [
                active_filter
                for active_filter in root_handler.filters
                if getattr(
                    active_filter,
                    bot.TELEGRAM_REDACTION_FILTER_MARKER,
                    False,
                )
            ]
            assert len(filters) == 1

        token, _, _ = _synthetic_token()
        root_logger.warning("single reload warning token=%s", token)
        output = stream.getvalue()
        assert output.count("single reload warning") == 1
        assert output.count("[REDACTED]") == 1
        assert token not in output
    finally:
        root_logger.removeHandler(handler)
