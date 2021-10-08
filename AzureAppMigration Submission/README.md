# TechConf Registration Website

## Project Overview
The TechConf website allows attendees to register for an upcoming conference. Administrators can also view the list of attendees and notify all attendees via a personalized email message.

The application is currently working but the following pain points have triggered the need for migration to Azure:
 - The web application is not scalable to handle user load at peak
 - When the admin sends out notifications, it's currently taking a long time because it's looping through all attendees, resulting in some HTTP timeout exceptions
 - The current architecture is not cost-effective 

In this project, you are tasked to do the following:
- Migrate and deploy the pre-existing web app to an Azure App Service
- Migrate a PostgreSQL database backup to an Azure Postgres database instance
- Refactor the notification logic to an Azure Function via a service bus queue message

## Dependencies

You will need to install the following locally:
- [Postgres](https://www.postgresql.org/download/)
- [Visual Studio Code](https://code.visualstudio.com/download)
- [Azure Function tools V3](https://docs.microsoft.com/en-us/azure/azure-functions/functions-run-local?tabs=windows%2Ccsharp%2Cbash#install-the-azure-functions-core-tools)
- [Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli?view=azure-cli-latest)
- [Azure Tools for Visual Studio Code](https://marketplace.visualstudio.com/items?itemName=ms-vscode.vscode-node-azure-pack)

## Project Instructions

### Part 1: Create Azure Resources and Deploy Web App
1. Create a Resource group
2. Create an Azure Postgres Database single server
   - Add a new database `techconfdb`
   - Allow all IPs to connect to database server
   - Restore the database with the backup located in the data folder
3. Create a Service Bus resource with a `notificationqueue` that will be used to communicate between the web and the function
   - Open the web folder and update the following in the `config.py` file
      - `POSTGRES_URL`
      - `POSTGRES_USER`
      - `POSTGRES_PW`
      - `POSTGRES_DB`
      - `SERVICE_BUS_CONNECTION_STRING`
4. Create App Service plan
5. Create a storage account
6. Deploy the web app

### Part 2: Create and Publish Azure Function
1. Create an Azure Function in the `function` folder that is triggered by the service bus queue created in Part 1.

      **Note**: Skeleton code has been provided in the **README** file located in the `function` folder. You will need to copy/paste this code into the `__init.py__` file in the `function` folder.
      - The Azure Function should do the following:
         - Process the message which is the `notification_id`
         - Query the database using `psycopg2` library for the given notification to retrieve the subject and message
         - Query the database to retrieve a list of attendees (**email** and **first name**)
         - Loop through each attendee and send a personalized subject message
         - After the notification, update the notification status with the total number of attendees notified
2. Publish the Azure Function

### Part 3: Refactor `routes.py`
1. Refactor the post logic in `web/app/routes.py -> notification()` using servicebus `queue_client`:
   - The notification method on POST should save the notification object and queue the notification id for the function to pick it up
2. Re-deploy the web app to publish changes

## Monthly Cost Analysis
Complete a month cost analysis of each Azure resource to give an estimate total cost using the table below:

| Azure Resource | Service Tier | Monthly Cost |
| ------------ | ------------ | ------------ |
| *Azure Postgres Database* |     |    $0.034/hour compute +  $0.034/hour Storage (1core + 1 Gb month)         |
| *Azure Service Bus*   |    Basic     |      $.05 per million operations        |
| *Azure App Service*   |     Free    |        $0.00      |
|*Azure Web App Service* | Free|$0.00|
|*Azure Function* | Consumption|$0.000016/GB-s execution time(*400,000 GB-s) and $0.20 per million executions *(1 million executions) $0.00 at current usuage (*free grant )|
|*SendGrid* | Free |$0.00 (up to emails a day)|

## Architecture Explanation
---
### Azure Web App 
The Azure Web App Service was a fine solution for this application. This PAAS provides security and service maintenance and updates as part of the service. The PAAS solution allows the developer to focus on developing and not on infrastructure. In addition, the application can be automatically scaled up or down to accommodate more usage. Since this application would see more usage during times when conferences are taking place this would be a great cost-saving and performance enhancing feature. 
### Azure Function
With the ability to automatically scale to meet increase demands and security and maintenance built in, the Azure Function App also allows the developer to not have to focus on infrastructure. Since the Function App is priced per use, it also provides cost savings since the application is not accruing charges when not being used. The function platform makes great sense for emailing since it can be easily and quickly deployed and utilized to send our emails, while not occuring charges when it is not in use.
## Screenshots
---
### Migrate Web Applications

Screenshot of Azure Resource showing the App Service Plan.
![Azure Resource](https://github.com/jmcole/Azure-Migration/blob/main/AzureAppMigration%20Submission/screenshots/1.1.PNG)
Screenshot of the deployed Web App running. The screenshot should be fullscreen showing the URL and application running.
![Azure WebApp](https://github.com/jmcole/Azure-Migration/blob/main/AzureAppMigration%20Submission/screenshots/1.2.PNG)

### Migrate Database

Screenshot of the Azure Resource showing the Azure Database for PostgreSQL server.
![Azure Database](https://github.com/jmcole/Azure-Migration/blob/main/AzureAppMigration%20Submission/screenshots/2.1.PNG)

Screenshot of the Web App successfully loading the list of attendees and notifications from the deployed website.

![Attendees](https://github.com/jmcole/Azure-Migration/blob/main/AzureAppMigration%20Submission/screenshots/2.2.PNG)
![Notifications](https://github.com/jmcole/Azure-Migration/blob/main/AzureAppMigration%20Submission/screenshots/2.3.PNG)

### Migrate Background Process

Screenshot of the Azure Function App running in Azure, showing the function name and the function app plan.
![Azure Function App](https://github.com/jmcole/Azure-Migration/blob/main/AzureAppMigration%20Submission/screenshots/3.1.PNG)

### Submitting a new notification.
Screenshot of filled out Send Notification form.
![Send notification form](https://github.com/jmcole/Azure-Migration/blob/main/AzureAppMigration%20Submission/screenshots/4.1.PNG)
Notification processed after executing the Azure function.
Screenshot of the Email Notifications List showing the notification status as Notifications submitted.
Screenshot of the Email Notifications List showing the notification status as Notified X attendees.
`Notification#43`
![Updated database](https://github.com/jmcole/Azure-Migration/blob/main/AzureAppMigration%20Submission/screenshots/4.2.png)


