from invoke import Collection, task


@task
def format_all(ctx):
    ctx.run("black src *.py")


@task
def typecheck(ctx):
    ctx.run("mypy src")


ns = Collection()
ns.add_task(format_all, name="format")
ns.add_task(typecheck)
