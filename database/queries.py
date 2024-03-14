class DB_Queries():
    
    SelectAll='select * from '

    InsertFormDetails = 'insert into form (name,country,email,mobile_number,req_description,synopsis_from_gpt,application_type,created_ts) values (%s,%s,%s,%s,%s,%s,%s,%s)'

    ## chatBot
    SelectAllServices = 'select * from services'
    SelectServiceURL = 'select service_url from services where service_name=%s'
