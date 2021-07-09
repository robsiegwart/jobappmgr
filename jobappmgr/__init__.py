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


def rename_file(from_name, to_name):
    '''
    Rename a file on the disk.
    
    :param path from:  The file path to the file to rename
    :param path to:    The renamed file path
    '''
    os.rename(from_name, to_name)
    click.echo(f'Renamed file "{os.path.basename(from_name)}" to "{os.path.basename(to_name)}"')


def add_extension(str_name, ext):
    '''Append an extension to a filename if it doesn't already have it'''
    return str_name if str_name.lower().endswith(f'.{ext}') else str_name + f'.{ext}'


def render_cover_letter(config, outdir):
    '''
    Copy the cover letter template to the output directory and substitute the
    template fields with data from the config file.
    '''
    # Copy the cover letter template file to the destination folder
    letter_bn = os.path.basename(config['cover-letter-template'])
    shutil.copy2(config['cover-letter-template'], outdir)
    click.echo(f'Copied cover letter file "{letter_bn}"')
    cl_template_path_init = os.path.join(outdir, letter_bn)

    # Rename the cover letter file to the one specified or a generic name
    cover_letter_name = add_extension(config.get('cover-letter-name'), 'docx') or 'Cover letter.docx'
    cl_template_path_final = os.path.join(os.path.split(cl_template_path_init)[0], cover_letter_name)
    rename_file(cl_template_path_init, cl_template_path_final)
    
    # Edit the DOCX file with the substitutions
    docx_file = docx.Document(cl_template_path_final)
    para = config.get('cover-letter-job-adder')
    para_to_remove = None

    for paragraph in docx_file.paragraphs:
        if paragraph.text == '{{cover-letter-job-adder}}':
            if not para:
                para_to_remove = paragraph
                continue
            else:
                paragraph.text = para
        else:
            for each in ['title','company']:
                paragraph.text = paragraph.text.replace('{{'+each+'}}', config.get(each,''))
    
    if para_to_remove:
        # From https://github.com/python-openxml/python-docx/issues/33#issuecomment-77661907
        p = para_to_remove._element
        p.getparent().remove(p)
        p._p = p._element = None

    docx_file.save(cl_template_path_final)