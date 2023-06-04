# elisseeff-avatar

virtualenv venv
source venv/bin/activate

#Your current project is [zinc-fusion-386715]
gcloud config set project analog-grin-386707
gcloud config list
gcloud auth login --cred-file=CONFIGURATION_FILE

export PROJECT_ID="analog-grin-386707"

#from google.cloud import dialogflow_v2beta1 as dialogflow



pip install google-cloud-dialogflow
pip install aiogram
#pip install openai
#pip install aiogram
#pip install pyyaml
#pip install pandas
#pip install grpcio-tools
#pip install pydub
#pip install yandex-speechkit
