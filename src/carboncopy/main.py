from .use_cases import get_local_config, UseCases


def run():
    config = get_local_config()
    use_cases = UseCases(config)

    use_cases.fetch_template_repository_details()

    try:
        use_cases.clone_template_repository()
        paths = use_cases.stage_changes()
        print("Applying changes")
        use_cases.apply_changes(paths)
        print("All done")
    except Exception as e:
        print(e.__class__)
        print(e)
        pass
    finally:
        use_cases.clean_up()
