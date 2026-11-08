def format_api_error(response, operation):
    try:
        error_data = response.json()
    except ValueError:
        error_data = response.text.strip()

    details = []
    if isinstance(error_data, dict):
        message = error_data.get("message")
        errors = error_data.get("errors")
        if message:
            details.append(str(message))
        if isinstance(errors, dict):
            for field, messages in errors.items():
                if not isinstance(messages, list):
                    messages = [messages]
                details.extend(f"{field}: {error}" for error in messages)
        elif errors:
            details.append(str(errors))
        if not details:
            details.append(str(error_data))
    elif error_data:
        details.append(str(error_data))

    summary = f"Falha ao {operation} (HTTP {response.status_code})"
    if details:
        summary += ":\n" + "\n".join(details)
    return summary
