import click 
@click.command()
@click.argument("file", type=click.File("r"))
def cli(file):
    """This script prints the contents of a file.
    \b
    Write file to stdout:
        hetionet foo.txt 
    """
    contents = file.read()
    print(contents)
    
if __name__ == '__main__':
    cli()