''' 
Utility functions for interfacing with the HIEv application

Author: Gerry Devine
'''


import os
import urllib2
import requests
import json
import time


# BASE_URL = 'https://hiev.uws.edu.au/'
BASE_URL = 'https://ic2-diver-staging-vm.intersect.org.au/'
# AUTH_TOKEN = os.environ['HIEV_API_KEY']
AUTH_TOKEN = os.environ['STAGING_HIEV_API_KEY']


def searchHiev(full_records         = True,
                from_date           = '',
                to_date             = '',
                filename            = '',
                description         = '',
                file_id             = '',
                id                  = '',
                stati               = None,
                automation_stati    = None,
                access_rights_types = None,
                file_formats        = None,
                published           = None,
                unpublished         = None,
                published_date      = None,
                tags                = None,
                labels              = None,
                grant_numbers       = None,
                related_websites    = None,
                facilities          = None,
                experiments         = None, 
                variables           = None,
                uploader_id         = '',
                upload_from_date    = '',
                upload_to_date      = ''):

    '''
    Return a list of full file records (or their IDs) matching a set of input search parameters
    (see https://github.com/IntersectAustralia/dc21-doc/blob/2.3/Search_API.md)
    
    Input
    -----
    - full_records - Boolean value dictating whether to return full records or just IDs,
    - from_date - This is "Date->From Date" in search box of WEB UI: "from_date"=>"2013-01-01"
    - to_date - This is "Date->To Date" in search box of WEB UI: "to_date"=>"2013-01-02"
    - filename - This is "Filename" in search box of WEB UI: "filename"=>"test"
    - description - This is "Description" in search box of WEB UI: "description"=>"test"
    - file_id - This is "File ID" in search box of WEB UI: "file_id"=>"test"
    - id - This is "ID" in search box of WEB UI: "id"=>"26"
    - stati - This is "Type" in search box of WEB UI: "stati"=>["RAW", "CLEANSED"]
    - automation_stati - This is "Automation Status" in search box of WEB UI, "automation_stati"=>["COMPLETE", "WORKING"]
    - access_rights_types - This is the "Access Rights Type" in the search box of the WEB UI: "access_rights_types"=>["Open", "Conditional", "Restricted"]
    - file_formats - This is "File Formats" in search box of WEB UI, "file_formats"=>["TOA5", "Unknown", "audio/mpeg"]
    - published - This is "Type->PACKAGE->Published" in search box of WEB UI: "stati"=>["PACKAGE"], "published"=>["true"].
    - unpublished - This is "Type->PACKAGE->Published" in search box of WEB UI: "stati"=>["PACKAGE"], "unpublished"=>["true"].
    - published_date - This is "Type->PACKAGE->Published Date" in search box of WEB UI: "stati"=>["PACKAGE"], "published_date"=>"2013-01-01"
    - tags - This is "Tags" in search box of WEB UI: "tags"=>["4", "5"]
    - labels - This is "Labels" in search box of WEB UI, "labels"=>["label_name_1", "label_name_2"]
    - grant_numbers - This is the "Grant Numbers" in search box of WEB UI, "grant_numbers"=>["grant_number_1", "grant_number_2"]
    - related_websites - This is the "Related Websites" in the search box of WEB UI, "related_websites"=>["http://www.intersect.org.au"]
    - facilities - This is "Facility" in search box of WEB UI, ask system administrator to get facility ids : "facilities"=>["27"]
    - experiments - This is "Facility" in search box of WEB UI, when one facility is clicked, experiments of this facility are selectable, ask system administrator to get experiment ids: "experiments"=>["58", "54"]
    - variables - This is "Columns" in search box of WEB UI, when one group is clicked, columns of this group are selectable: "variables"=>["SoilTempProbe_Avg(1)", "SoilTempProbe_Avg(3)"]
    - uploader_id - This is "Added By" in search box of WEB UI, ask system administrator to get uploader ids: "uploader_id"=>"83"
    - upload_from_date - This is "Date Added->From Date" in search box of WEB UI, "upload_from_date"=>"2013-01-01"
    - upload_to_date - This is "Date Added->To Date" in search box of WEB UI, "upload_to_date"=>"2013-01-02"
    
    Returns
    -------
    List of matching hiev search results (with file download url included) OR List of matching file IDs 
    
    Example
    -------
    myfiles = searchHiev(full_records = False, experiments=['39'], from_date="2016-08-01")
     
    '''
    
    request_url = BASE_URL + 'data_files/api_search'
    
    # -- Set up the http search request and handle the returned response
    request_headers = {'Content-Type' : 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
    request_data = json.dumps({ 'auth_token'          : AUTH_TOKEN, 
                                'experiments'         : experiments, 
                                'filename'            : filename,
                                'from_date'           : from_date,
                                'upload_to_date'      : upload_to_date,
                                'description'         : description,
                                'file_id'             : file_id,
                                'id'                  : id,
                                'stati'               : stati,
                                'automation_stati'    : automation_stati,
                                'access_rights_types' : access_rights_types,
                                'file_formats'        : file_formats,
                                'published'           : published,
                                'unpublished'         : unpublished,
                                'published_date'      : published_date,
                                'tags'                : tags,
                                'labels'              : labels,
                                'grant_numbers'       : grant_numbers,
                                'related_websites'    : related_websites,
                                'facilities'          : facilities,
                                'experiments'         : experiments, 
                                'variables'           : variables,
                                'uploader_id'         : uploader_id,
                                'upload_from_date'    : upload_from_date,
                                'upload_to_date'      : upload_to_date
                              })
    requests.packages.urllib3.disable_warnings()   # ignore ssl warnings from python 2.7.5
    request  = urllib2.Request(request_url, request_data, request_headers)
    response = urllib2.urlopen(request)
    
    if full_records == True:    
        return json.load(response)
    else:
        records_list = json.load(response)
        # Create an empty list to hold our IDs
        ids = []
        # Loop over each record and pull out the ID field
        for rec in records_list:
            ids.append(rec['file_id'])
            
        return ids 
    
    
    
def updateHiev(file_ids                           = None,
                name                              = None,
                experiment_id                     = None,
                description                       = None,
                tag_names                         = None,
                parent_filenames                  = None,
                label_names                       = None,
                creator_email                     = None,
                contributors_names                = None,
                title                             = None,
                grant_numbers                     = None,
                related_websites                  = None,
                access_rights_types               = None,
                license                           = None,
                access                            = None,
                access_to_all_institutional_users = None,
                access_to_user_groups             = None,
                access_groups                     = None,
                start_time                        = None,
                end_time                          = None
                ):

    '''
    Update a list of file metadata records (or their IDs)
    (see https://github.com/IntersectAustralia/dc21-doc/blob/master/File_Update_API.md)
    
    Input
    -----
    - file_ids - List of file IDs on which to update metadata,
    - name - the name of the file
    - experiment_id (or org_level2_id) - the numeric ID of the experiment this file belongs to - you can find the numeric ID on the 'view experiment page'
    - description - a description of the file
    - tag_names - a quoted, comma separated list of tags to apply to the file, must be from the set of legal tag names
    - parent_filenames - an array of parent file names, which must exist on the server prior to update
    - label_names - a quoted, comma separated list of labels to apply to the file
    - creator_email - a string of creator's email to apply to the file, must be from the email list of approved users
    - contributor_names - a string array of contributors to apply to the file
    - title - the title of the package
    - grant_numbers - a quoted, comma separated list of grant numbers to apply to the package
    - related_websites - a quoted, comma separated list of related websites to apply to the package
    - access_rights_type - the access rights type, must be one of "Open", "Conditional" or "Restricted"
    - license - the license, must be one of "CC-BY", "CC-BY-SA", "CC-BY-ND", "CC-BY-NC", "CC-BY-NC-SA", "CC-BY-NC-ND" or "All rights reserved"
    - access - access level for the file is either 'Public' or 'Private' (default is 'Private' unless otherwise specified)
    - access_to_all_institutional_users - an option for private access for Institutional Users, which can be set either true or false
    - access_to_user_groups - an option for private access for certain groups of users, which can be set to true or false
    - access_groups - an array of names of access groups, which must exist on the server prior to update
    - start_time - The start time to use if one could not be extracted from the file's metadata. Must be in the format 'yyyy-mm-dd hh:mm:ss'
    - end_time - The end time to use if one could not be extracted from the file's metadata. Must be in the format 'yyyy-mm-dd hh:mm:ss'
    
    Returns
    -------
    None. File records in HIEv will be updated in place.
    
    Example
    -------
    updateHiev(file_ids=['197', '198'], description='this has been updated using the API')
     
    '''
    
    update_url = BASE_URL + 'data_files/api_update?auth_token=' + AUTH_TOKEN

    #Pass the file id to the update API as well as the updated metadata
    for file_id in file_ids:
        payload = {
            'file_id'                           : file_id,                         
            'name'                              : name,                             
            'experiment_id'                     : experiment_id,                    
            'description'                       : description,                      
            'tag_names'                         : tag_names,                        
            'parent_filenames'                  : parent_filenames,                 
            'label_names'                       : label_names,                      
            'creator_email'                     : creator_email,                    
            'contributors_names'                : contributors_names,               
            'title'                             : title,                            
            'grant_numbers'                     : grant_numbers,                    
            'related_websites'                  : related_websites,                 
            'access_rights_types'               : access_rights_types,              
            'license'                           : license,                          
            'access'                            : access,                           
            'access_to_all_institutional_users' : access_to_all_institutional_users,
            'access_to_user_groups'             : access_to_user_groups,            
            'access_groups'                     : access_groups,                    
            'start_time'                        : start_time,                       
            'end_time'                          : end_time                         
        }
        requests.packages.urllib3.disable_warnings()   # ignore ssl warnings from python 2.7.5
        # Update current file with the new file metadata
        r = requests.post(update_url, data=payload, verify=False)

        if r.status_code != 200:
            print 'ERROR - There was a problem updating the file in HIEv'
    
    
    

def getLatestFile(filename):
    ''' 
    Return a single file from HIEv. If the filename supplied matches multiple 
    files, the most recent file will be returned.
    
    Input
    -----
    Filename: string
    
    Returns
    -------
    Single file object
    '''
     
    request_url = BASE_URL + 'data_files/api_search'
    
    # --Set up the http request
    request_headers = {'Content-Type' : 'application/json; charset=UTF-8', 'X-Accept': 'application/json'}
    request_data = json.dumps({'auth_token': AUTH_TOKEN, 
                               'filename': filename})
    
    # --Handle the returned response from the HIEv server
    requests.packages.urllib3.disable_warnings()   # ignore ssl warnings from python 2.7.5
    request  = urllib2.Request(request_url, request_data, request_headers)
    response = urllib2.urlopen(request)
    js = json.load(response)
    
    # --Grab the latest - in those cases where there are multiple results returned
    latest_file = (sorted(js, key=lambda k: k['updated_at'], reverse=True))[0] 
    download_url = latest_file['url']+'?'+'AUTH_TOKEN=%s' %AUTH_TOKEN
    request = urllib2.Request(download_url)
    
    return urllib2.urlopen(request)
    


def getUserDetails(user_id):
    ''' 
    Return details of a single HIEv user
    
    Input
    -----
    user_id : Integer value representing user ID in HIEv
    
    Returns
    -------
    Single dictionary with details of user
    '''
    
    # Get the most recent list of users
    users_list = getLatestFile('HIEv_User_List_') 
    # Convert the file object to string and split by line
    users_list = users_list.read().splitlines()
    # --Set up global values
    user_line = [i for i in users_list if i.startswith(str(user_id)+',')][0].split(',')  
    user_details = {
      "id":        user_line[0],
      "email":     user_line[1],
      "firstname": user_line[2],
      "lastname":  user_line[3]
    }
    
    return user_details



def downloadFiles(file_ids):
    '''
    Downloads hiev files identified by file ID to a local dated directory
    
    Input
    -----
    array of HIEv file IDs in HIEv
    
    Returns
    -------
    Downloaded files into a folder matching today's date
    
    '''
    
    download_dir = os.path.join(os.getcwd(), 'data_downloads', time.strftime("%Y%m%d"))
    if not os.path.exists(download_dir):
        os.makedirs(download_dir)
    for file_id in file_ids: 
        download_url = BASE_URL+'data_files/'+file_id+'/download.json?'+'auth_token=%s' %AUTH_TOKEN
        request = urllib2.Request(download_url)
        
        try: 
            response = urllib2.urlopen(request)
        except urllib2.HTTPError, e:
            print 'HTTPError = ' + str(e.code)
        except urllib2.URLError, e:
            print 'URLError = ' + str(e.reason)
        except httplib.HTTPException, e:
            print 'HTTPException'
        except Exception:
            import traceback
            print 'generic exception: ' + traceback.format_exc()
    
        # --Write the file and close it
        with open(os.path.join(download_dir, response.info()['Content-Disposition'].split('"')[1]), 'w') as local_file:
            local_file.write(response.read())
        local_file.close()
       
       
        

updateHiev(file_ids=['197', '198'], description='this has been updated using the API across multiple files')

