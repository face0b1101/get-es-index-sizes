# python-boilerplate

Python Poetry Boilerplate Project Structure

## Folder Structure

```sh
python-poetry-boilerplate
├── .github
│   └── workflows                 # Github Workflows directory
│       ├-- development.yaml      # Production workflow (not in repo, example filename)
│       └-- production.yaml       # Development workflow (not in repo, example filename)
├── conftest.py                   # pytest configuration file
├── notebooks
│   └── test.ipynb                # Test Jupyter notebook
├── src
│   └── python_poetry_boilerplate
│       ├── config
│       │   ├── __init__.py
│       │   └── env.py            # Environment variables python module (using python-decouple)
│       ├── libs                  # Utility libraries
│       │   ├── __init__.py
│       │   └── my_libs.py        # Example library module
│       └── main.py               # Main python module
├── tests
│   ├── __init__.py
│   └── test_my_app.py            # Example pytest
├── .dockerignore                 # Docker ignore file
├── .env.example                  # Environment variables example
├── .flak8                        # flake8 configuration
├── .gitattributes                # Git attributes file
├── .gitignore                    # Git ignore file
├── pre-commit-config.yaml        # git pre-commit configuration
├── conftest.py                   # Test configuration file
├── docker-compose.yml            # Example docker-compose file
├── Dockerfile                    # Dockerfile for building poetry-based python app containers
├── Dockerfile.kubernetes         # Dockerfile for kubernetes (not ready for use, needs updating)
├── Dockerfile.lambda             # Dockerfile for lambda (not ready for use, needs updating)
├── Makefile                      # Example Makefile
├── poetry.lock                   # Poetry lock file
├── pyproject.toml                # Pyproject.toml
└── README.md                     # Readme
```

## How to Create a new Project

There are two ways to create a new Project.

### 1. Create a new Project from the repo as a template

Pretty straightforward. Go to the [repository](https://github.com/face0b1101/python-poetry-boilerplate) and click the green `Use this template` button.

See [here](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-repository-from-a-template) for more details.

### 2. Create a Fork

Alternatively, create a fork the _old-fashioned_ way:

- Create new repository on GitHub (`new-repository-name`)
- Create another folder on local machine
- Bare clone this repository

    ```bash
    git clone --bare https://github.com/face0b1101/python-poetry-boilerplate
    ```

- CD to this folder (with .git suffix) and push mirror to GitHub

    ```bash
    cd python-boilerplate.git
    git push --mirror https://github.com/face0b1101/new-repository-name.git
    ```

- Remove `python-poetry-boilerplate.git` folder from local folder
- Clone `new-repository-name` to local folder

### Housekeeping

When you have your new project set up, a bit of housekeeping is required:

1. Rename `src/python_poetry_boilerplate` to `src/new_repository_name`

2. Update `pyproject.toml`
    - replace `python-poetry-boilerplate` with `new-repository-name`
    - replace `python_poetry_boilerplate` with `new_repository_name`
    - update other items in `[tool.poetry]` as appropriate (e.g. python version)

3. Update pytest scripts
    - update imports in `tests/test_my_app.py`

4. Rename `.env.example` to `.env`

5. Ensure python version is set

    ```bash
    pyenv local 3.11.1

    # check the version
    pyenv version

    python --version
    ```

    `3.11.1 (set by .python-version)`

6. Update dependancies [OPTIONAL]

    ```bash
    poetry update
    ```

   There may be some errors with pyqtwebengine. If so, do this:

    ```bash

    poetry remove pyqtwebengine-qt5
    poetry add pyqtwebengine-qt5@5.15.2
   ```

7. Create a new virtualenv and install code via Poetry

    ```bash
    poetry install
    ```

8. Run pytest

    ```bash
    poetry run pytest
    ```

    If the tests run without error then you have configured your project and you're ready to get coding.

9. Enable git pre-commit hooks
   Some example pre-commit hooks are configured in `.pre-commit-config.yaml`. These can be enabled by running:

   ```bash
   poetry run pre-commit install
   ```

## How to Code

1. Create a new branch

   ```bash
   git branch <new-branch>
   ```

2. Install Poetry

   ```bash
   # creates venv and install application
   poetry install
   poetry shell
   ```

3. Do some coding and stuff...

4. Push the new branch and changes

   ```bash
   git push -u origin <new-branch>
   ```

## How to Commit

- Commit on the branch
- PR if it should be merged
- Specify the type of commit:
  - feat: The new feature you're adding to a particular application
  - fix: A bug fix
  - style: Feature and updates related to styling
  - refactor: Refactoring a specific section of the codebase
  - test: Everything related to testing
  - docs: Everything related to documentation
  - chore: Regular code maintenance.[ You can also use emojis to represent commit types]

## Docker

You can also run the app using [Docker](https://docs.docker.com/get-docker/).

## Building the container

First, build the docker container. There is a Dockerfile in the root of the repository. You can use `docker` or `docker-compose`:

```sh
# docker
DOCKER_BUILDKIT=1 docker build -f Dockerfile --target runtime -t face0b1101/python_poetry_boilerplate:0.1 .

# docker-compose
docker-compose build
```

Once the container is built, you can run it with:

```shell
# docker
docker run --rm --name my-container --env-file .env face0b1101/python_poetry_boilerplate:0.1

# docker-compose
docker-compose up
```
