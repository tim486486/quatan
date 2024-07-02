#Release: Quatan 0.0

This was a project I started during lockdown so my wife and I could play our favourite card game while we were stuck in different provinces. (Un?)Fortunately the lockdown ended before I finished the project.

This application was developed on Python 3.8.1 64-bit.

##Installing the dependencies

* Install Postgres and launch pgAdmin	
    * Set the Master Password
    * Create a database
* Populate the ini files with your database information
* Install Python and PIP (included with Python installer available from https://www.python.org/)
* In an elevated command prompt navigate to the orcas directory, enter the following command:
    * pip install -r requirements.txt
___
    
##Database Manager

* Run launch_dbmanager.py from the orcas folder
* If running for the first time, click 'Build Database' to create the Tables and Users required to run the Server 

___

##Client

* Run launch_client.py
