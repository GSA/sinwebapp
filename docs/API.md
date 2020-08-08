### Documentation Navigation
[<< Development](DEVELOPMENT.md) | [^ ReadMe ^](../README.md) | [Appendix >>](APPENDIX.md)

## Routes & Endpoints

Listed below are the current routes used by each component of the application, the Angular frontend and the Django backend,

# Django Static HTML Endpoints
- <i>/</i> - Login Splash Page
- <i>/logout</i> - Logout Splash Page
- <i>/success</i> - Authenticated Login Splash Page. This is where the Angular application enters. 

# Application API Endpoints
- <i>/api/user</i> - retrieves information about the currently signed-in user associated with an incoming request.<br>
> <b>GET RESPONSE FORMAT</b><br><br>
> { <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'email': 'user(at)domain.com', &nbsp;&nbsp;&nbsp;&nbsp;(<i>String</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'groups': 'user_groups_list' &nbsp;&nbsp;&nbsp;&nbsp;(<i>JSON List</i>)<br>
>}<br>



- <i>/api/users</i> - retrieves information about a collection of users identified by the array of IDs provided in the query parameter. The array is specified by repeated instances of the same <i>ids</i> query parameter, i.e.,

> localhost:8000/api/users?ids=3&ids=7&ids=10

will return an array of JSONs containing information on the Users with ID = 3, 7 and 10. 



- <i>/api/sin</i> - exposes a <b>GET</b> and <b>POST</b> endpoint. 

1. The <b>GET</b> endpoint requires a query parameter of ID for a given SIN number and returns its corresponding information. 

For example, the following HTTP request<br>

>localhost:8000/api/sin?id=123456<br>

will return a JSON formatted response containing information about SIN Number 123456 in the following format,

> <b>GET RESPONSE FORMAT</b><br><br>
> { <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'sin_number': 'SIN #', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'user': 'user ID', &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>) <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'status' 'user status' &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
>}<br>

2. The POST endpoint requires a SIN number within the body of the POST. The method will attempt to either create a new entry in the database for the SIN number, or if that SIN number already exists in the database, it will attempt to update that entry if its status is contained in the set (Approved, Denied, Expired). If its status is contained in the set (Submitted, Reviewed, Change), then the method will return an error.

    > <b>POST REQUEST FORMAT</b><br><br>
    > { <br>
    >   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'sin_number': 'SIN #' &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
    >}<br>




- <i>/api/sins</i> - retrieves a JSON array of all SINs
    > <b>GET RESPONSE FORMAT</b><br><br>
    > { <br>
    >   [ <br>
    >       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'sin_number': 'SIN #', &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
    >       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'user': 'user ID', &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
    >       &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'status' 'user status' &nbsp;&nbsp;&nbsp;&nbsp;(<i>Int</i>)<br>
    >   ]<br>
    >}<br><br>




- <i>/api/updateSIN/</i> - POST endpoint to update an existing SIN within the database.



- <i>/api/sinUser/</i> - GET endpoint that exchanges a User ID for a response containing the entire User object.



- <i>/api/statuses</i> - returns an array of JSONs for all statuses.




- <i>/api/status</i> - given a query parameter of ID, this GET method retrieves a Status Name and Description for an ID. For example,

> localhost:8000/api/status?id=3

will return a JSON containing the ID's status name and description in the following format,

> <b>GET RESPONSE FORMAT</b><br><br>
> { <br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'status': 'Status name', &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; (<i>String</i>)<br>
>   &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'description': 'Status description' &nbsp;&nbsp;&nbsp;&nbsp;(<i>String</i>)<br>
>}<br><br>

# Third Party Endpoints
- <i>/auth/login</i> - redirect endpoint for cloud.gov OAuth2 authorization and authentication.<br>
- <i>/auth/callback</i> - callback endpoint for cloud.gov OAuth2 authorization and authentication<br>
- <i>/fake/oauth/authorize</i> - mock authorize endpoint for fake cloud.gov backend<br>
- <i>/fake/oauth/token</i> - mock token generation endpoint for fake cloud.backend<br>

# Frontend Routes
- <i>404</i>: Not yet created. TODO.