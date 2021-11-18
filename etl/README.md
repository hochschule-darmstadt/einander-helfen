# Info
The scripts which will extract the data from the corresponding websites for the 'einander-helfen' platform.



# Requirements
- Python Version > 3.6 is needed
- Python packages which are required can be found in the requirements.txt



# Execution
- The crawling and enhancement are executed by running:
    ```bash
    # Run german context 
    python3 main.py 
    python3 main.py -c DE
    
    # Run us context 
    python3 main.py -c US
    ```
- The indexing to the post index can be executed by running:
    ```bash
    # Run german context 
    python3 execute_elastic_upload.py 
    python3 execute_elastic_upload.py -c DE
    
    # Run us context 
    python3 execute_elastic_upload.py -c US
    ```
- Both steps are automatically executed by a cron job on the live server which executes the bash script located in the scripts folder:
    ```bash
    # Run german context 
    run_etl.sh 
    run_etl.sh -c DE
    
    # Run us context 
    run_etl.sh -c US
    ```
- **[Deprecated]** At the end of the cron job, the enhanced data is getting archived in a package and made available for file transfer,
    if you want to use this data on the live server, the `get_data_from_staging.sh` script needs to be executed on the live server.
- **[Deprecated]** Afterwards the data can be uploaded to the live index by executing:
    ```bash
    # Run german context 
    upload_to_elastic.sh 
    upload_to_elastic.sh -c DE
    
    # Run us context 
    upload_to_elastic.sh -c US
    ```



# Structure
Folders and scripts are structured by their ETL task.

| Folder                      | Task                                                                 |
| --------------------------- | -------------------------------------------------------------------- |
| data_enhancement            | Data transformations after the extraction                            |
| data_extraction             | Everything related to the extraction of data                         |
| data_management (generated) | Data management for upload and backups                               |
| logs (generated)            | Logs of the execution process                                        |
| scripts                     | Shell scripts to execute the ETL process                             |
| shared                      | Includes a util file with util functions use by all classes          |
| test                        | Unit tests for the python modules                                    |
| upload_to_elasticsearch     | Upload the extracted and transformed data to an ElasticSearch server |
