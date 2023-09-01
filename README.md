# sister-stac

### Purpose: Allow SISTER HySDS system to allow STAC catalogs and items as inputs and outputs for a PGE.

## Requirements:
- Conda (23.1.0+)
    - conda env yml: `sister-stac-env.yml` 
- Python (3.7+)
    - python env requirements.txt: `requirements.txt`

## Scripts:
- ### read_stac.py
    - Purpose: Outline details of STAC Catalog
    - Input: String of remote/local STAC catalog path 
    - Output: Print of Catalog ID, title, description, and items
- ### remote_to_local_stac.py
    - Purpose: Convert remote STAC catalog to local STAC catalog
    - Input: String of remote STAC catalog URL
    - Output: Local STAC Catalog of Input Catalog
- ### local_to_remote_stac.py
    - Purpose: Convert local STAC catalog to remote STAC catalog and store in AWS S3 bucket.
    - Input: String of local STAC catalog path
    - Output: Remote (AWS S3) STAC Catalog of Input Catalog 

## Examples:
### read_stac.py
`$ python read_stac.py https://raw.githubusercontent.com/scottyhq/sentinel1-rtc-stac/main/19TCH/2021/catalog.json`

### local_to_remote_stac.py
`$ python local_to_remote_stac.py -c https://raw.githubusercontent.com/scottyhq/sentinel1-rtc-stac/main/19TCH/2021/catalog.json -s s3://s3.us-west-2.amazonaws.com:80/sister-ops-workspace/stage_out/`

### remote_to_local_stac.py
`$ python remote_to_local_stac.py -c https://raw.githubusercontent.com/scottyhq/sentinel1-rtc-stac/main/19TCH/2021/catalog.json`

## References:

 -  STAC: https://stacspec.org/en/
 -  Osaka: https://github.com/hysds/osaka/blob/develop/osaka/main.py
