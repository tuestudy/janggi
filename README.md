# janggi

## Environment

1. `brew install python3`

2. `pip install virtualenv virtualenvwrapper`

3. .bash_profile, .bashrc, ... 에

4. `export WORKON_HOME=$HOME/.venvs
source /usr/local/bin/virtualenvwrapper.sh`

5. 위에 설치한 파이썬 3설정은 아래와 같이.. ``mkvirtualenv -a `pwd` janggi --python=$(which python3.x)``
설치한 파이썬 버전으로..

6. `workon janggi` 로 어디 디렉토리에서 치시던 바로 가상환경으로 들어갈 수 있습니다.

파이썬 3를 사용합니다.  파이썬 환경은 각자 알아서 준비합니다.


## UI demo

Install requirements:

```
pip install -r requirements.txt
```


---

\*NIX:

```
./run.sh
./run.sh -h
```

Windows:

```
run.bat
run.bat -h
```
