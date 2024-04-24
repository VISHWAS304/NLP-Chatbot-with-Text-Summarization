# NLP-Chatbot-with-Text-Summarization
The project aims to develop a Natural Language Processing (NLP) based chatbot designed specifically for restaurant services. This chatbot will assist customers by answering FAQs, helping with table reservations, providing menu details, and accommodating special requests. Additionally, it will summarize conversations to enhance customer service.

Create an folder named chatbot (any name you like) then navigate to that folder using anaconda prompt and create environment
```bash
conda create --name chatbot python

conda create --name chatbot python=3.8   (can specify the python version if required)
```
Activate the environment
```bash
conda activate chatbot
```

To Run the File while developing
1.Run below command to start FastAPI
```bash
uvicorn main:app --reload
```
2.Download the ngrok.exe from ngrok page or go to https://dashboard.ngrok.com/get-started/setup/windows this setup page and follow steps for download as per your os/programming requirements
```bash
choco install ngrok
ngrok config add-authtoken 2eeSxTGVimejOxtIM4hUBusdDnd_75rZxYpbn5F3eGuG6cqXm
```
3.Run below command to start the server
```bash
ngrok http http://localhost:8000  or ngrok http 8000  (in cmd prompt)
```
4.Copy the url provided by server and paste it in fullfillment webhook URL of Dialogflow
```bash
https://69a4-2607-fb91-309b-5ed-1d1a-be1d-3d37-c09b.ngrok-free.app  (example)
```
```


