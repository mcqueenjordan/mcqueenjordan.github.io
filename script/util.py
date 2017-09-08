#!/usr/bin/python3
import click
import time
import sys
import re

URI_REGEX_PATTERN = re.compile('[^0-9a-zA-Z -]+')
POST_TEMPLATE = '''\
---
layout: thought
title: "{title}"
subtitle: "{subtitle}"
name: "{name}"
published_date: "{published_date}"
category: post
---

'''

@click.group()
def main() -> None:
    pass

def infer_default_name(ctx: object, param: str, value: None) -> str:
    if ctx.params.get('title') is None:
        ctx.params['title'] = input('Title: ')

    return format_as_uri(ctx.params['title'])

@main.command('create-post')
@click.option('-t', '--title', type = str, default = None)
@click.option('-s', '--subtitle', type = str, default = None)
@click.option('-d', '--published-date', type = str, default = time.strftime('%Y-%m-%d'))
@click.option('-n', '--name', type = str, callback = infer_default_name)
def create_post(**create_post_request: dict) -> None:
    '''Client-exposed API to create a post.'''
    prompt_for_and_set_missing(create_post_request)
    _create_post(create_post_request)

def _create_post(create_post_request: dict) -> None:
    '''Logical implementation for creating a post locally.'''
    file_contents = POST_TEMPLATE.format(**create_post_request)
    file_location = '_thought/{name}.md'.format(**create_post_request)
    chars_written = write_file(file_contents, file_location)
    print("Wrote {} characters to {}.".format(chars_written, file_location))

def prompt_for_and_set_missing(cli_request: dict) -> None:
    '''Prompts for and sets missing vals in the dictionary.
    Note:
        Side-effects.
    '''
    for arg, val in cli_request.items():
        if val is None:
            cli_request[arg] = input(arg + ': ')

def write_file(file_contents: str, file_location: str) -> None:
    with open(file_location, 'w') as f:
        chars_written = f.write(file_contents)
    return chars_written

def format_as_uri(string: str) -> str:
    return '-'.join(re.sub(URI_REGEX_PATTERN, '', string).split()).lower()

if __name__ == '__main__':
    main()

