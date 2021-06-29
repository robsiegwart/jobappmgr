'''
Functions for the job app manager program.
'''

import os
import datetime
import shutil
import click
import docx


def create_folder(path):
    os.mkdir(path)
    click.echo(f'Creating directory "{path}"')


def create_publish_dir(name='Publish'):
    '''Create the top-level publish directory if it does not already exist'''
    if not os.path.exists(name):
        create_folder(name)
    return name


def clean(path):
    '''Clean a string for usage as a Windows directory name'''
    return path.replace('/','-')


def get_or_create_output_directory(config):
    '''
    Create the output directory for generated/copied files within the output
    directory.
    '''
    folder_name = f'{clean(config["company"])}-{clean(config["title"])}-{datetime.datetime.today().strftime("%m%d%Y-%H%M%S")}'
    out_path = create_publish_dir()
    folder_path = os.path.join(out_path, folder_name)
    if not os.path.exists(folder_path):
        create_folder(os.path.relpath(folder_path, os.getcwd()))
    return folder_path


def render_cover_letter(config, outdir, cover_letter_name='R. Siegwart cover letter'):
    # Copy the template to the destination folder
    letter_bn = os.path.basename(config['cover-letter-template'])
    shutil.copy2(config['cover-letter-template'], outdir)
    click.echo(f'Copied cover letter file "{letter_bn}"')
    template_path = os.path.join(outdir, letter_bn)

    # Rename the cover letter file
    rn_template_path = os.path.join(os.path.split(template_path)[0], cover_letter_name + '.docx')
    os.rename(template_path, rn_template_path)
    
    # Edit the DOCX file with the substitutions
    docx_file = docx.Document(rn_template_path)
    para = config.get('cover-letter-job-adder')
    para_to_remove = None

    for paragraph in docx_file.paragraphs:
        for each in ['title','company']:
            if paragraph.text == '{{cover-letter-job-adder}}':
                if not para:
                    para_to_remove = paragraph
                    continue
                else:
                    paragraph.text = para
            else:
                paragraph.text = paragraph.text.replace('{{'+each+'}}', config.get(each,''))
    
    if para_to_remove:
        # From https://github.com/python-openxml/python-docx/issues/33#issuecomment-77661907
        p = para_to_remove._element
        p.getparent().remove(p)
        p._p = p._element = None

    docx_file.save(rn_template_path)