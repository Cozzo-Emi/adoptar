def send_recovery_email(email: str, token: str) -> bool:
    """Envía email de recuperación. Por ahora loggea a consola."""
    print(f"EMAIL DE RECUPERACIÓN para {email}: token={token}")
    return True
