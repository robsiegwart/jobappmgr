'''
Command-line interface for the jobappmgr program.
'''

import shutil
import yaml
import os
import click
from jobappmgr import (
    get_or_create_output_directory,
    rename_file,
    render_cover_letter,
    add_extension
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
    # ----------------------------
    outdir = get_or_create_output_directory(config)

    # Copy the resume file and rename if a name was given
    # ---------------------------------------------------
    shutil.copy2(config['resume'], outdir)
    click.echo(f'+ Copied resume file "{os.path.basename(config["resume"])}"')
    if config.get('resume-name'):
        dest_resume = os.path.join(outdir, os.path.basename(config['resume']))
        rename_file(dest_resume, os.path.join(outdir, config['resume-name']))
    
    # Copy and render the cover letter template
    # -----------------------------------------
    letter_bn = os.path.basename(config['cover-letter-template'])
    shutil.copy2(config['cover-letter-template'], outdir)
    click.echo(f'+ Copied cover letter file "{letter_bn}"')
    cl_template_path_init = os.path.join(outdir, letter_bn)

    # Rename the cover letter file to the one specified or default generic name
    cover_letter_name = add_extension(config.get('cover-letter-name'), 'docx') or 'Cover letter.docx'
    cl_template_path_final = os.path.join(os.path.split(cl_template_path_init)[0], cover_letter_name)
    rename_file(cl_template_path_init, cl_template_path_final)
    
    # Render cover letter template fields
    render_cover_letter(config, cl_template_path_final)

    click.echo('\nFinished')


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
resume-name: # an alternate name for the destination resume file
cover-letter-name: # an alternate name for the destination cover letter file
''')
    click.echo(f'Created file "{fn}" in directory "{os.getcwd()}"')