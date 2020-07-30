[<< Development](DEVELOPMENT.md) |[^ ReadMe ^](../README.md)

# Appendix

## TODO
- [x] reset service-key redirect uri on cloud.gov
- [x] determine how to protect certain endpoints from unauthenticated individuals
- [x] create users with roles in database
- [x] integrate angular frontend application with django backend framework
- [ ] bind roles to html on redirect page after successful login 
- [x] create pipeline to build frontend and deploy to cloud
- [ ] load in database credentials for local deployments through VCAP_SERVICES environment variable to mimic cloud deployments
- [ ] REMOVE <i>crsf_exempt</i> decorate from POST api endpoints that were put in place to test during development!!!

## Useful Links
### Core Application
- [Django: Data Migrations](https://docs.djangoproject.com/en/3.0/topics/migrations/#data-migrations)
- [Django: Authentication Documentation](https://docs.djangoproject.com/en/3.0/topics/auth/default/)<br>
- [Django: Groups Class Documentation](https://docs.djangoproject.com/en/3.0/ref/contrib/auth/#django.contrib.auth.models.Group)<br>
- [Django: Permissions Class Documentation](https://docs.djangoproject.com/en/3.0/topics/auth/default/#permissions-and-authorization)<br>
- [Django: User Class Documentation](https://docs.djangoproject.com/en/3.0/topics/auth/default/#user-objects)<br>
- [Gunicorn: Documentation](https://docs.gunicorn.org/en/stable/run.html)
### Authentication
- [Cloud.gov: Identity Provider](https://cloud.gov/docs/services/cloud-gov-identity-provider/) <br/>
- [Cloud.gov: Service Account](https://cloud.gov/docs/services/cloud-gov-service-account/)
- [Cloud.gov: Leveraging Authentication](https://cloud.gov/docs/management/leveraging-authentication/) <br/>
- [CloudFoundry: Service Keys](https://docs.cloudfoundry.org/devguide/services/service-keys.html) <br/>
- [cg-django-uaa: Documentation](https://cg-django-uaa.readthedocs.io/en/latest/quickstart.html)<br/>
- [Angular: HTTP Interceptor to handle withCredentials Header](https://weblog.west-wind.com/posts/2019/Apr/07/Creating-a-custom-HttpInterceptor-to-handle-withCredentials)<br>
### Security
- [Django: Cross Site Request Forgery Tokens](https://docs.djangoproject.com/en/3.0/ref/csrf/)
### Relevant Stack Discussions
- [Django: Add Auth Groups Programmatically](https://stackoverflow.com/questions/25024795/django-1-7-where-to-put-the-code-to-add-groups-programmatically/25803284#25803284)<br>
- [Django: Creating JSON HttpResponse](https://stackoverflow.com/questions/2428092/creating-a-json-response-using-django-and-python)<br>
- [Django: Add User to Group Via Group Admin](https://stackoverflow.com/questions/39485067/django-add-user-to-group-via-django-admin/39648244)
- [Django: Output QuerySet as Json](https://stackoverflow.com/questions/15874233/output-django-queryset-as-json)
- [Django: CSRF Cookie Not Set](https://stackoverflow.com/questions/17716624/django-csrf-cookie-not-set)
- [Angular: withCredentials Header, What Is It?](https://stackoverflow.com/questions/27406994/http-requests-withcredentials-what-is-this-and-why-using-it)