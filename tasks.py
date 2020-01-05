from invoke import Collection, task


@task
def format_all(ctx):
    ctx.run("black src *.py")


ns = Collection()
ns.add_task(format_all, name="format")
