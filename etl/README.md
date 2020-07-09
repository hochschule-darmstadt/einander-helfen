## Info
The scripts which will extract the data from the corresponding websites for the 'einander-helfen' platform.

## Requirements
- Python Version > 3.6 is needed
- Python packages which are required can be found in the requirements.txt

## Execution
- The crawling and enhancement are executed by running:
    `python3 main.py` from the etl directory
- The indexing to the post index can be executed by running:
    `python3 -c 'from upload_to_elasticsearch.elastic import run_elastic_upload; run_elastic_upload()'`
    from the etl directory
- Both steps are automatically executed by a cron job which executes the bash script:
    `run_complete_etl.sh`
- If you would like to run the indexing process inside of the main for debugging reasons,
   you can add the run_elastic_upload() method to the main.py

## Structure
Folders ans scripts are structured by their ETL task.

| Folder                  | Task                                                                     |
| ----------------------- | ------------------------------------------------------------------------ |
| data_extraction         | Everything related to the extraction of data                             |
| data_enhancement        | Data transformations after the extraction                                |
| upload_to_elasticsearch | Upload the extracted and transformed data to an ElasticSearch server     |
| shared                  | Includes a util file with util functions use by all classes              |

## Output

- Inside the data_extraction folder, a data folder gets created and every domain gets a output file
in the JSON format with the filename of its corresponding scraper.

- Inside the data_enhancement folder, a data folder gets created and a JSON file for each enhanced domain is written.
A output folder gets created with a file called new_tags.json which lists all new found tags which are not yes in 
the tag ontology. Furthermore a ranked_tags.json file gets created with the ranked tag_ontology.