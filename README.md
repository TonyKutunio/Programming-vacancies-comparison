# Programming vacancies comparison  

This script compares vacancies of TOP10 programming languages in Moscow from the biggest Russian
job-search websites: `HeadHunter and SuperJob`
To get that comparison you will have to go to `GetComparison.py` file and run it.   

## How to install
`Python3` should be already installed. Then use pip (or pip3, if there is a conflict with `Python2`) to install dependencies:   

```
pip install -r requirements.txt
```  
## setting up .env variables   
  You will  have to set your environment variables up, with `.env` file where you going to store
  your `SUPER_JOB_SECRET_KEY` only, as you don't need any keys for Headhunter. 
  

  You can use [Notepad++](https://notepad-plus-plus.org/downloads/) to create this file for Windows,
or [CotEditor](https://coteditor.com/) for MacOS.
  
##### This is an example of how it looks like inside of your .env file. 
(You can choose your own variable names if you want)  
```
SUPER_JOB_SECRET_KEY=Your_SuperJobSecretKey
```

Variables has to be with CAPITAL letters and without any spaces at all!  

### Project Goals  
To make life easier
