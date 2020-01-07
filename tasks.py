from invoke import Collection, task

TMP_PATH = "/tmp/carboncopy_pytest/"


@task
def format_all(ctx):
    ctx.run("black src *.py")


@task
def typecheck(ctx):
    ctx.run("mypy src")


@task
def package(ctx):
    ctx.run("rm -rf dist && python setup.py sdist bdist_wheel")


@task(optional=["test"])
def publish(ctx, test=False):
    if test:
        ctx.run(
            "twine upload --verbose --repository-url https://test.pypi.org/legacy/ dist/*"
        )
    else:
        ctx.run("twine upload dist/*")


@task
def test(ctx):
    ctx.run("pytest")


ns = Collection()
ns.add_task(format_all, name="format")
ns.add_task(typecheck)
ns.add_task(package)
ns.add_task(publish)
ns.add_task(test)
