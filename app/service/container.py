from dependency_injector import containers
from dependency_injector import providers

from app.service.jwt import JWTService
from app.service.mail.user import UserMailService
from app.service.mailer.smtp.client import SMTPClient
from app.service.templater import Templater


class ServiceContainer(containers.DeclarativeContainer):
    project_name = providers.Dependency(instance_of=str)
    project_url = providers.Dependency(instance_of=str)
    project_email = providers.Dependency(instance_of=str)

    smtp_host = providers.Dependency(instance_of=str)
    smtp_port = providers.Dependency(instance_of=int)
    smtp_username = providers.Dependency(instance_of=str)
    smtp_password = providers.Dependency(instance_of=str)
    smtp_use_tls = providers.Dependency(instance_of=bool)

    jwt_algorithm = providers.Dependency(instance_of=str)
    jwt_secret = providers.Dependency(instance_of=str)
    jwt_ttl = providers.Dependency(instance_of=int)

    jwt = providers.Factory(
        JWTService, algorithms=jwt_algorithm, secret=jwt_secret, ttl=jwt_ttl
    )

    templater = providers.Factory(Templater, project_url=project_url)

    mailer = providers.Factory(
        SMTPClient,
        host=smtp_host,
        port=smtp_port,
        username=smtp_username,
        password=smtp_password,
        use_tls=smtp_use_tls,
        templater=templater,
        from_email=project_email,
        from_name=project_name,
    )

    user_mailer = providers.Factory(UserMailService, mailer=mailer)
