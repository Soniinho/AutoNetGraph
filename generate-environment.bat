:: Create venv
python -m venv .\.venv

:: Activate venv
call .\.venv\Scripts\activate

:: Upgrade pip
python.exe -m pip install --upgrade pip

:: Install dependencies
pip install -r requirements.txt

:: Install VirtualBox SDK
cd sdk\installer
python vboxapisetup.py install

echo Environment configured successfully!
