# Zairza Codelabs
Code that powers [Zairza Codelabs](https://codelabs.zairza.in)

Inspired from [Google Developers Codelabs](https://codelabs.developers.google.com/)

## Adding new sessions

1. Add your code under a sub-folder `codelabs`
2. Edit `codelabs.yaml` and reference the sub-folder. Fill in other details such as the title and description.

## Building

We utilize pipenv.

1. Start a pipenv environment with `pipenv shell` and install the requirements with `pipenv install`.
2. Run `python codelabs.py` to generate the codelabs website under `dist`

## Running locally

1. Run `python codelabs.py serve` to start a static web server over generated content.

## LICENSE

Copyright (c) 2018 Zairza Technical Club. Content and code available under the MIT license.
