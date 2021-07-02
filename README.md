# jobappmgr

A Python command-line program to organize and prepare a resume and cover letter
for a job application based on a YAML configuration file.

A specific resume is copied to the publish folder along with a cover letter
which has been rendered with the copmany name and job title and an optional
additional paragraph.

## Usage

In your project directory, create a YAML file and edit accordingly. Then call
the command line program with your config file as the argument:

`jobappmgr <YAML file>`

After calling this the program reads the config file and copies the resume and
cover letter to an output directory within a new directory `Publish` located in
the current directory. The cover letter is the original .docx which can then be
reviewed and further edited.

## YAML file options

- *company*, the company name
- *title*, the job title
- *resume*, the file path to the resume file to use for this application
- *cover-letter-template*, the file path to the cover letter template file to use for this application
- *cover-letter-job-adder*, a paragraph to insert in the `{{cover-letter-job-adder}}` field

## Sample YAML file

    company: ACME Company
    title: Sales Engineer
    resume: path\to\my\file.pdf
    cover-letter-template: path\to\my\template.docx
    cover-letter-job-adder: >
        <text>

## Word Templates

Word template files are regular Word files but with fields mapping to properties
in the config file having a Jinja-style syntax. E.g.

    To the Search Committee,

    I am writing in regards to the advertisement for the position of {{title}}.

    {{cover-letter-job-adder}}

    I am confident that I would make meaninful contributions to {{company}} and ...
