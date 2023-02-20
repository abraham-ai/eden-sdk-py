# Eden Python SDK

## Notes

put api keys in the .env file

call render create script here:

`render.py
`

### Files

#### render.py

Sample code, use for testing, replace with your own




#### request_creation.py

This is server-ready

#### upload_files.py

Not quite server-ready



### args list, generators is here

[https://github.com/abraham-ai/eden-api/blob/main/mongo-init.js]()

`baseParameters` is for all generators

This shows all your generators, may change, look at js file

`db.generators.insertMany([
  createGenerator,
  interpolateGenerator,
  real2realGenerator,
  remixGenerator,
  interrogateGenerator,
  ttsGenerator,
  wav2lipGenerator,
  completeGenerator,
]);
`
### Install python-dotenv
`pip3 install python-dotenv`