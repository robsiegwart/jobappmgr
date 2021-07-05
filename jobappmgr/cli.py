'''
Command-line interface for the app-mgr program.
'''

import shutil
import yaml
import os
import click
from jobappmgr import (
    get_or_create_output_directory,
    render_cover_letter
)


@click.group()
def cli():
    pass


@cli.command(help='Construct a resume and cover letter')
@click.argument('config_file')
def build(config_file):
    '''Run the generation routine'''
    # Load config file
    with open(config_file) as f:
        config = yaml.safe_load(f.read())

    # Establish output directories
    outdir = get_or_create_output_directory(config)

    # Copy the resume file
    shutil.copy2(config['resume'], outdir)
    click.echo(f'Copied resume file "{os.path.basename(config["resume"])}"')
    
    # Render the cover letter template
    cl = render_cover_letter(config, outdir)

    click.echo('Finished')


@cli.command(help='Create a sample YAML file in the current directory')
def init():
    '''Create a sample YAML file in the current directory'''
    fn = 'Sample.yaml'
    with open(fn,'w') as f:
        f.write('''company: # company name
title: # the job title
resume: # the/path/to/the/resume.pdf
cover-letter-template: # the/path/to/the/cover letter template.docx
cover-letter-job-adder: >
  # content for a paragraph to inject
''')
    click.echo(f'Created file "{fn}"')