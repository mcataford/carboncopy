from .use_cases import get_local_config, UseCases
from .print_utils import pretty_print
from .git_utils import NoTemplateError, NotInAGitRepositoryError


def run():
    config = get_local_config()
    use_cases = UseCases(config)

    try:
        use_cases.fetch_template_repository_details()
    except NotInAGitRepositoryError:
        pretty_print("Not in a git repository.")
        return 1
    except NoTemplateError:
        pretty_print("This repository does not have a template associated with it.")
        return 1

    try:
        use_cases.clone_template_repository()
        paths = use_cases.stage_changes()
        use_cases.apply_changes(paths)
    except Exception as e:
        pretty_print(e.__class__)
        pretty_print(e)
    finally:
        use_cases.clean_up()
