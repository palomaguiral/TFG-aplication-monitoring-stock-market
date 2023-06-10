# Application for monitoring operations in the securities market 
This repository contains the code and necessary steps to deploy the developed application, which consists of two functionalities: a stock market operation monitoring application and a transaction-executing chatbot.

## Reproducibility of the Application

This document details the steps required for anyone to run the applications locally on their computer.

## General Prerequisites

Before deploying, make sure you meet the following prerequisites on your computer:

- Have Python installed.
- Have a code editor installed that allows you to open Python files (.py), such as Visual Studio Code.
- Clone this GitHub repository, which can be accessed [here](https://github.com/palomaguiral/TFG-aplication-monitoring-stock-market/tree/master).
- Have the Trader Workstation desktop application downloaded.

Within this GitHub repository, you will find two different folders: 'Operational Monitoring Application' and 'Transaction Execution Chatbot,' which correspond to the two developed programs. Below, we explain how to deploy each of these programs separately.

## Operational Monitoring Application

Inside the 'Operational Monitoring Application' folder, you will find all the necessary files to maintain monitoring of the operations carried out by the user in their brokerage account.

### Prerequisites

Before running the application, make sure you meet the following prerequisites:

- Be registered with Interactive Brokers and investing.com.
- Have the Trader Workstation desktop application open during executions.
- Install the dependencies listed in the 'requirements.txt' file.

This application is divided into two programs: one for initialization in the first execution (the 'first execution' folder) and another for the daily monitoring of operations (the 'daily execution' folder). The following steps explain each of these programs.

### First Execution

Inside the 'first execution' folder, you will find the necessary code to initialize the monitoring process. This includes creating the three investing.com portfolios and initializing the positions of portfolio 1.

Follow these steps for the first execution:

1. Create an '.env' file that includes your investing.com user credentials in the following format:
    USER_INVESTING = YOUR_USERNAME
    PASSWORD_INVESTING = YOUR_PASSWORD

2. Execute the 'app_firstExecution.py' file.

### Daily Execution

Inside the 'daily execution' folder, you will find the necessary code to download the daily operations carried out in Interactive Brokers and upload them to the different investing.com portfolios.

Follow the steps corresponding to your operating system to schedule the daily execution of the program:

#### Windows

1. Open the Windows 'Task Scheduler'.
2. Click on 'Create Basic Task' in the right panel to open the task creation wizard.
3. Provide a name and an optional description for the task.
4. Choose the frequency at which you want the task to run (daily).
5. Configure the date and time of task execution.
6. Choose the action 'Start a program'.
7. Specify the program you want to execute ('app_dailyExecution.py') and make sure it runs with Python in the following fields:

   - Program/script: path to the Python executable on your computer (python.exe)
   - Add arguments: app_dailyExecution.py
   - Start in: path to the 'daily execution' folder

8. Finish the wizard.

#### macOS

On macOS, the 'launchd' task scheduler is used. Follow these steps:

1. Create a property list (plist) file specifying the task configuration, including the time interval and the command to execute the Python script.
2. Save the plist file in the '~/Library/LaunchAgents' directory.
3. Load the task into launchd using the command 'launchctl load ~/Library/LaunchAgents/file_name.plist'.

#### Linux

On Linux, the cron task scheduler is used. Follow these steps:

1. Open a terminal and run the command "crontab -e" to edit the scheduled tasks.
2. Add a line to the cron file using the following syntax: "minute hour * * * python_interpreter_path script_path".

## Transaction Execution Chatbot

Inside the 'Transaction Execution Chatbot' folder, you will find all the files necessary to deploy the chatbot for executing transactions.

### Prerequisites

Before running the chatbot, make sure you meet the following prerequisites:

- Be registered with Interactive Brokers.
- Have the Trader Workstation desktop application open during executions.
- Install the dependencies listed in the 'requirements.txt' file.
- Be registered with OpenAI and obtain an API Key.

Follow these steps to run the chatbot locally:

1. Create an '.env' file and include your OpenAI API Key as follows:
      APIKEY_OPENAI = YOUR_OPENAI_API_KEY

2. Execute the 'app.py' script. You can do this from the terminal using the command 'python path/app.py' or through your code editor.

3. Access the Flask application in your web browser by visiting the URL 'http://localhost:5000/' as it will be running locally.

Make sure to replace the paths and credentials with your own information!


