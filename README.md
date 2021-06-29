# app-mgr

A Python command-line program to organize and prepare a resume and cover letter
for a job application based on a YAML config file.

Substitutes the company name and title and an additional paragraph based on
the content in the YAML file.

## Usage

Usage is via the command line interface. In your project directory, place the
YAML file and edit accordingly. Then call the command line program:

`jobappmgr <YAML file>`

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

Word template files are regular Word files but with these keywords placed where
they should be using the Jinja syntax. E.g.

    To the Search Committee,

    I am writing in regards to the advertisement for the position of {{title}}.

    {{cover-letter-job-adder}}

    Based on my ability to ...