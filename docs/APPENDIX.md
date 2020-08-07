[<< Development](DEVELOPMENT.md) |[^ ReadMe ^](../README.md)

# Appendix

## TODO
- [x] reset service-key redirect uri on cloud.gov
- [x] determine how to protect certain endpoints from unauthenticated individuals
- [x] create users with roles in database
- [x] integrate angular frontend application with django backend framework
- [x] bind roles to html on redirect page after successful login 
- [x] create pipeline to build frontend and deploy to cloud
- [ ] load in database credentials for local deployments through VCAP_SERVICES environment variable to mimic cloud deployments

## Useful Links
### Core Application
- [Django: Data Migrations](https://docs.djangoproject.com/en/3.0/topics/migrations/#data-migrations)
- [Django: Authentication Documentation](https://docs.djangoproject.com/en/3.0/topics/auth/default/)<br>
- [Django: Groups Class Documentation](https://docs.djangoproject.com/en/3.0/ref/contrib/auth/#django.contrib.auth.models.Group)<br>
- [Django: Permissions Class Documentation](https://docs.djangoproject.com/en/3.0/topics/auth/default/#permissions-and-authorization)<br>
- [Django: User Class Documentation](https://docs.djangoproject.com/en/3.0/topics/auth/default/#user-objects)<br>
- [Gunicorn: Documentation](https://docs.gunicorn.org/en/stable/run.html)<br><br>
### Authentication
- [Cloud.gov: Identity Provider](https://cloud.gov/docs/services/cloud-gov-identity-provider/) <br/>
- [Cloud.gov: Service Account](https://cloud.gov/docs/services/cloud-gov-service-account/)
- [Cloud.gov: Leveraging Authentication](https://cloud.gov/docs/management/leveraging-authentication/) <br/>
- [CloudFoundry: Service Keys](https://docs.cloudfoundry.org/devguide/services/service-keys.html) <br/>
- [cg-django-uaa: Documentation](https://cg-django-uaa.readthedocs.io/en/latest/quickstart.html)<br/>
- [Angular: HTTP Interceptor to handle withCredentials Header](https://weblog.west-wind.com/posts/2019/Apr/07/Creating-a-custom-HttpInterceptor-to-handle-withCredentials)<br><br>
### Security
- [Django: Cross Site Request Forgery Tokens](https://docs.djangoproject.com/en/3.0/ref/csrf/)<Br>
- [Angular: XRSF Security Protection](https://angular.io/guide/http#security-xsrf-protection)<br>
- [Angular: HttpClient XSRF Module](https://angular.io/api/common/http/HttpClientXsrfModule)<br><br>
### Relevant Stack Discussions
- [Django: Add Auth Groups Programmatically](https://stackoverflow.com/questions/25024795/django-1-7-where-to-put-the-code-to-add-groups-programmatically/25803284#25803284)<br>
- [Django: Creating JSON HttpResponse](https://stackoverflow.com/questions/2428092/creating-a-json-response-using-django-and-python)<br>
- [Django: Add User to Group Via Group Admin](https://stackoverflow.com/questions/39485067/django-add-user-to-group-via-django-admin/39648244)<br>
- [Django: Output QuerySet as Json](https://stackoverflow.com/questions/15874233/output-django-queryset-as-json)<br>
- [Django: CSRF Cookie Not Set](https://stackoverflow.com/questions/17716624/django-csrf-cookie-not-set)<br>
- [Django: Serializing Objects with Many-to-Many relations](https://stackoverflow.com/questions/34474893/django-serializer-manyrelatedmanager-object-at-xx-is-not-json-serializable)<br>
- [Django: values_list() vs. values()](https://stackoverflow.com/questions/37205793/django-values-list-vs-values)
- [Angular: withCredentials Header, What Is It?](https://stackoverflow.com/questions/27406994/http-requests-withcredentials-what-is-this-and-why-using-it)<br>
- [Angular: Service Not Sending XSRF Token Header With HTTP Request](https://stackoverflow.com/questions/50510998/angular-6-does-not-add-x-xsrf-token-header-to-http-request)<br>
- [Docker: Apt Repository is Not Signed](https://stackoverflow.com/questions/59139453/repository-is-not-signed-in-docker-build)<br>