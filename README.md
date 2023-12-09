# AudioMixer

<p align="center">
    <img src="https://img.shields.io/badge/python-3.11-green?logo=python&logoColor=white&style=for-the-badge">
    <img src="https://img.shields.io/badge/LICENSE-MIT-green?style=for-the-badge">
    <img src="https://img.shields.io/github/languages/code-size/Zwylair/AudioMixer?style=for-the-badge">
</p>

AudioMixer is an audio files "joiner" program.

#### Features:
* Supported formats: `OGG`, `MP3`, `WAV`
* Unlimited files count
* Unlimited audio length

# Installation


The first step of installation is cloning the `AudioMixer` repository. You can do it with:

```
git clone https://github.com/Zwylair/AudioMixer
```

# Running

You can download [release](https://github.com/Zwylair/AudioMixer/releases) for Windows (>=10) or download the source code and run it manually.

## Setting up virtualenv environment

If you don't have the virtualenv package, you need to install it:

#### Linux
```bash
python3 -m pip install virtualenv
```

#### Windows
```bash
py -m pip install virtualenv
```

---

`AudioMixer` uses python version 3.11, make sure your python version is the same as the required version.

Go to the folder where you are going to run the program and write in the console:

#### Linux
```bash
python3 -m virtualenv venv
```

#### Windows
```bash
py -m virtualenv venv
```

---

The next step is activating virtualenv environment:

#### Linux
```bash
venv/Scripts/activate
```

#### Windows
```bash
venv\Scripts\activate
```


## Installing dependencies

#### Linux
```bash
python3 -m pip install -r requirements.txt
```

#### Windows
```bash
py -m pip install -r requirements.txt
```

## Running

#### Linux
```bash
python3 main.py
```

#### Windows
```bash
py main.py
```

# License

This project is under the [MIT license](./LICENSE).
