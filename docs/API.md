### Documentation Navigation
[<< Frontend](FRONTEND.md) | [^ ReadMe ^](../README.md) | [Appendix >>](APPENDIX.md)

# Routes & Endpoints

Listed below are the current routes used by each component of the application, the Angular frontend and the Django backend,

## Django Static HTML Endpoints
- <i>/</i> - Login Splash Page
- <i>/logout</i> - Logout Splash Page
- <i>/success</i> - Authenticated Login Splash Page. This is where the Angular application enters. 

## Application API Endpoints

You must be logged in and authenticated through <i>cloud.gov</i> in order to access any of the endpoints given below. The backend tracks the user's login session through a cookie called <b>session_id</b>. This cookie is sent in the <i>Set-Cookie</i> response header after the user logs onto the site. 

Note, there are also public available endpoints, <i>/api/v1/sins</i>, <i>/api/v1/search</i> and <i>/api/v1/status/</i>, that no login is required to access. These endpoints are not documented here since they are implemented through <b>django-rest-framework</b> in order to take advantage of OpenAPI/Swagger integration with that package. As such, you can read the auto-generated documentation at the official site [here (Swagger)](https://ccda.app.cloud.gov/api/v1/swagger/)
or [here (Redoc)](https://ccda.app.cloud.gov/api/v1/redoc/). You do not need to be logged into cloud.gov to see the documentation.

### Authentication Endpoints

Note: Roles are the same thing as groups. Both terms are used interchangeably in this documentation, although technically all permissions are handled through Django's concept of a Group. 

- <i>/api/user</i> - <b>GET</b> - retrieves information about the currently signed-in user associated with an incoming request.<br>

> <b>GET RESPONSE FORMAT</b><br><br>
> { <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'id': 'ID', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'email': 'user(at)domain.com', &nbsp;&nbsp;&nbsp;&nbsp;(<i>String</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'groups': 'user_groups_list' &nbsp;&nbsp;&nbsp;&nbsp;(<i>JSON List</i>)<br>
>}<br>

- <i>/api/users</i> - <b>GET</b> - retrieves information about a collection of users identified by the array of IDs provided in the query parameter. The array is specified by repeated instances of the same <i>ids</i> query parameter, i.e.,

> localhost:8000/api/users?ids=3&ids=7&ids=10

will return an array of JSONs containing information on the Users with ID = 3, 7 and 10. 

> <b>GET RESPONSE FORMAT</b><br><br>
> { <br>
> [ <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'id': 'ID', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'email': 'user(at)domain.com', &nbsp;&nbsp;&nbsp;&nbsp;(<i>String</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'groups': 'user_groups_list' &nbsp;&nbsp;&nbsp;&nbsp;(<i>JSON List</i>)<br>
> ]<br>
> }<br>

- <i>/api/sinUser</i> - <b>GET</b> - exchanges a User ID for a response containing the entire User object.

> localhost:8000/api/sinUser?user_id=123

will return a response containing information about the User with ID = 123.

> <b>GET RESPONSE FORMAT</b><br><br>
> { <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'id': 'ID', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'email': 'user(at)domain.com', &nbsp;&nbsp;&nbsp;&nbsp;(<i>String</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'groups': 'user_groups_list' &nbsp;&nbsp;&nbsp;&nbsp;(<i>JSON List</i>)<br>
>}<br>

- <i>/api/groups</i> - <b> GET </b> - returns an array of JSONs containing all available groups/roles a User can belong to.
 
> <b>GET RESPONSE FORMAT</b><br><br>
> { <br>
> [<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'id': 'ID', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'name': 'Status name', &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(<i>String</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'description': 'Status description' &nbsp;&nbsp;&nbsp;&nbsp;(<i>String</i>)<br>
> ]<br>
> }

- <i>/api/userStatuses</i> - <b> GET </b> - returns an array of JSONs for all statuses available to given role. For example, the user requesting the statuses is a <i>submitter</i>, the response will only contain the <b>submitted</b> status. If the user requesting the status is a <i>reviewer</i>, then the response will contain the <b>submitted</b>, <b>reviewed</b> and <b>change</b> statuses. If the user is an <i>approver</i> or <i>admin</i>, the response will contain all statuses. 
> <b>GET RESPONSE FORMAT</b><br><br>
> { <br>
> [<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'id': 'ID', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'name': 'Status name', &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(<i>String</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'description': 'Status description' &nbsp;&nbsp;&nbsp;&nbsp;(<i>String</i>)<br>
> ]<br>
> }

### Model Endpoints

- <i>/api/sin</i> - <b> GET / POST </b> - 

1. The <b>GET</b> endpoint requires a query parameter of ID for a given SIN number and returns its corresponding information. 

For example, the following HTTP request<br>

>localhost:8000/api/sin?id=123456<br>

will return a JSON formatted response containing information about SIN Number 123456 in the following format,

> <b>GET RESPONSE FORMAT</b><br><br>
> { <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'id': 'ID', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'sin_number': 'SIN #', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'user_id': 'user ID', &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>) <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'status_id' 'user status' &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>}<br>

2. The POST endpoint requires a SIN number within the body of the POST. The method will attempt to either create a new entry in the database for the SIN number, or if that SIN number already exists in the database, it will attempt to update that entry if its status is contained in the set (Approved, Denied, Expired). If its status is contained in the set (Submitted, Reviewed, Change), then the method will return an error.

> <b>POST REQUEST FORMAT</b><br><br>
> { <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'sin_number': 'SIN #' &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>}<br><br>
> <b>POST RESPONSE FORMAT</b><br><br>
> { <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'id': 'ID', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'sin_number': 'SIN #', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'user_id': 'user ID', &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>) <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'status_id' 'user status' &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>}<br>

- <i>/api/sins</i> - <b> GET </b> -retrieves a JSON array of all SINs
> <b>GET RESPONSE FORMAT</b><br><br>
> { <br>
>   [ <br>
>       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'id': 'ID', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'sin_number': 'SIN #', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'user_id': 'user ID', &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'status_id' 'user status' &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>   ]<br>
>}

- <i>/api/updateSIN/</i> - <b>POST</b> - update an existing SIN within the database.
> <b>POST REQUEST/RESPONSE FORMAT</b><br><br>
> { <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'id': 'ID', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'sin_number': 'SIN #', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'user_id': 'user ID', &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>) <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'status_id' 'user status' &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>}<br>

- <i>/api/statuses</i> - <b> GET</b> - returns an array of JSONs for all statuses.
> <b>GET RESPONSE FORMAT</b><br><br>
> { <br>
> [<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'id': 'ID', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'name': 'Status name', &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(<i>String</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'description': 'Status description' &nbsp;&nbsp;&nbsp;&nbsp;(<i>String</i>)<br>
> ]<br>
> }

- <i>/api/status</i> - <b> GET </b> - given a query parameter of ID, this method retrieves a Status Name and Description for an ID. For example,

> localhost:8000/api/status?id=3

will return a JSON containing the ID's status name and description in the following format,

> <b>GET RESPONSE FORMAT</b><br><br>
> { <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'id': 'ID', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'name': 'Status name', &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (<i>String</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'description': 'Status description' &nbsp;&nbsp;&nbsp;&nbsp;(<i>String</i>)<br>
>}

### S3 Storage Endpoints

Note: currently the application is only able to associate and store a single file in relation to a given SIN submission. In the future the application will allow multiple files to associated with a single SIN submission. See [S3](S3.md#future-todos) for more details.

- <i>/files/upload</i> - <b>POST</b> - a form-encoded file (an HTML enctype="multipart/form-data" form) can be uploaded to this endpoint. Currently, the endpoint does <i>not</i> check for the mimetype, although in the future, it will only accept form-encoded files that have a mimetype of "application/pdf". See the TODO in <i>/sinwebapp/files/views.py</i> on lines 29-31.

> localhost:8000/api/status?id=3
> <b>POST REQUEST FORMAT</b><br><br>
> { <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'body': 'form-data' &nbsp;&nbsp;&nbsp;&nbsp;<br>
>}

- <i>/files/download</i> - <b>GET</b> - this endpoint accepts a <i>sin_number</i> as a query parameter and returns the attachment associated with that particular submission in the body of the response. Currently, only one attachment can be associated with any given SIN submission. In the future, multiple attachments will be associated with a single SIN, so this endpoint will need to be modified to facilite a response with multiple pdf's in its body. 

In its current implementation the following request,

> localhost:8000/files/download?sin_number=12345

will return a PDF file with the filename "12345.pdf" in the body of the response.

> <b>POST REQUEST FORMAT</b><br><br>
> { <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'body': 'form-data' &nbsp;&nbsp;&nbsp;&nbsp;<br>
>}

- <i>/files/list</i> - <b>GET</b> - this endpoint accepts a <i>sin_number</i> as a query parameter or no query parameters at all. If supplied with a <i>sin_number</i>, the response will contain a list of all the filenames associated with a given SIN. If no query parameter is supplied, all filenames within the S3 storage bucket are listed in the response. 

Keep in mind, multiple file attachments to a given SIN has not yet been implemented. Only a single file can currently be associated with a given SIN, so technically every list return will only be 1 item long.

> localhost:8000/files/list?sin_number=12345

will return a response with all the files associated with SIN # 12345 in the format given below,

> <b>RESPONSEFORMAT</b><br><br>
> { <br>
>   { <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'index': 'filename' &nbsp;&nbsp;&nbsp;&nbsp;<br>
>   } <br>
>}

## Third Party Endpoints
- <i>/auth/login</i> - redirect endpoint for cloud.gov OAuth2 authorization and authentication.<br>
- <i>/auth/callback</i> - callback endpoint for cloud.gov OAuth2 authorization and authentication<br>
- <i>/fake/oauth/authorize</i> - mock authorize endpoint for fake cloud.gov backend<br>
- <i>/fake/oauth/token</i> - mock token generation endpoint for fake cloud.backend<br>

## Frontend Routes
- <i>404</i>: Not yet created. TODO.

### Documentation Navigation
[<< Frontend](FRONTEND.md) | [^ ReadMe ^](../README.md) | [Appendix >>](APPENDIX.md)