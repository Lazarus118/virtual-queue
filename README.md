# Demo Endpoints #
For testing use 'scotia.virtualqueue.com' as value for org_domain and '1' as value for queue_id

## Managing Organizations ##
### Endpoint: Organization - `/api/v1/organization/` - method(GET) ###
Possible Request Arguments:

* String: org_domain (required)

### Endpoint: Creating Organization - `/api/v1/organization/` - method(POST) ###
Possible Request Arguments:

* String: org_name (required)
* String: org_domain (required)
* String: org_country (required)
* String: org_address (required)
* String: org_phone
* String: org_email
* String: org_contact


### Endpoint: Updating Organization - `/api/v1/organization/` - method(PUT) ###
Possible Request Arguments:

* String: org_name (required)
* String: org_domain (required) (domain is required for getting the domain info, but cannot be changed)
* String: org_country (required)
* String: org_address (required)
* String: org_phone
* String: org_email
* String: org_contact

### Endpoint: Deleting Organization - `/api/v1/organization/` - method(DELETE) ###
Possible Request Arguments:

* String: org_domain (required)

`TODO: CLEAN UP SCRIPTS ARE NEEDED: ONLY QUEUES AND ORGANIZATION ARE CURRENTLY DELETED, BUT NOT QUEUE DATA`


## Managing Organization Settings ##
### Endpoint: Getting A Specific Setting - `/api/v1/organization/settings/` - method(GET) ###
Possible Request Arguments:

* String: org_domain (required)
* Integer: setting_id (required)

### Endpoint: Creating A New Setting - `/api/v1/organization/settings/` - method(POST) ###
Possible Request Arguments:

* String: org_domain (required)
* String: setting_param (required)
* String: setting_value (required)

### Endpoint: Updating A Setting - `/api/v1/organization/settings/` - method(PUT) ###
Possible Request Arguments:

* String: org_domain (required)
* Integer: setting_id (required)
* String: setting_param (required)
* String: setting_value (required)

### Endpoint: Deleting A Setting - `/api/v1/organization/settings/` - method(DELETE) ###
Possible Request Arguments:

* String: org_domain (required)
* Integer: setting_id (required)

## Managing Queue Groups ##
### Endpoint: Getting A Group - `/api/v1/queue_groups/` - method(GET) ###
Possible Request Arguments:

* String: org_domain (required)
* Integer: group_id

If no group_id received, we send all groups

### Endpoint: Updating A Group - `/api/v1/queue_groups/` - method(PUT) ###
Possible Request Arguments:

* String: org_domain (required)
* Integer: group_id (required)
* String: group_name (required)
* String: group_note - for a description or something

### Endpoint: Deleting A Group - `/api/v1/queue_groups/` - method(DELETE) ###
Possible Request Arguments:

* String: org_domain (required)
* Integer: group_id (required)

### Endpoint: Creating A Group - `/api/v1/queue_groups/` - method(POST) ###
Possible Request Arguments:

* String: org_domain (required)
* String: group_name (required)
* String: group_note - for a description or something


## Managing Queues ##
### Endpoint: Getting A Queue - `/api/v1/queues/` - method(GET) ###
Possible Request Arguments:

* String: org_domain (required)
* Integer: queue_id

If no queue_id received, we return all queues and their data

### Endpoint: Creating A Queue - `/api/v1/queues/` - method(POST) ###
Possible Request Arguments:

* String: org_domain (required)
* String: queue_name (required)
* Integer: queue_group_id (required)

### Endpoint: Updating A Queue - `/api/v1/queues/` - method(PUT) ###
Possible Request Arguments:

* String: org_domain (required)
* String: queue_id (required)
* String: queue_name (required)
* String: queue_group_id - if you want to move a queue to another group

### Endpoint: Deleting A Queue - `/api/v1/queues/` - method(DELETE) ###
Possible Request Arguments:

* String: org_domain (required)
* Integer: queue_id (required)


## Managing Users in Queue ##
### Endpoint: Queue Users - `/api/v1/queues/users/` - method(POST) ###
Possible Request Arguments:

* String: phone_number (required)
* Integer: queue_id (required)

### Endpoint: Dequeue Users - `/api/v1/queues/users/` - method(PUT) ###
Possible Request Arguments:

* String: phone_number (required)
* Integer: queue_id (required)
