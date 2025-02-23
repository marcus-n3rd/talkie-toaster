# Talkie Toaster

## Setup

### Prerequisites

- [Python 3.13+](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/installation.html)
- [Ollama](https://ollama.com/)
  - [gemma2](https://ollama.com/library/gemma2)

Be sure to run Ollama to install the cli, `ollama`.

### Install Project Dependencies

```sh
pipenv install
ollama pull gemma2
```

## Run

```sh
pipenv run streamlit run app/talkie.py
```

## Disclaimer

I'm obviously just a fan of the show and don't own any rights to Red Dwarf property nor am I making any claims here.
Simply using the tools available to run a tutorial in an interesting way.
