from lab_toolkit.decorators.cli import handle_errors
from lab_toolkit.decorators.config import EXCLUDED_MODULES, INCLUDED_MODULES
from lab_toolkit.exceptions import LabToolkitError
from lab_toolkit.logger.pipeline import log_pipeline


def cli_command(
    *,
    action: str,
    target: str,
    included_modules=INCLUDED_MODULES,
    excluded_modules=EXCLUDED_MODULES,
):
    """
    Décorateur central des commandes CLI.

    Orchestre :
    - le suivi des fonctions ;
    - la journalisation ;
    - la gestion des erreurs ;
    - la configuration des modules suivis et exclus.
    """

    def decorator(func):

        decorated_func = log_pipeline(
            action=action,
            target=target,
            included_modules=included_modules,
            excluded_modules=excluded_modules,
            internal_exceptions=(LabToolkitError,),
        )(func)

        return handle_errors((LabToolkitError,))(decorated_func)

    return decorator
