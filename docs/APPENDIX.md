(Development <<)[DEVELOPMENT.md] 

## TODO
- [x] reset service-key redirect uri on cloud.gov
- [x] determine how to protect certain endpoints from unauthenticated individuals
- [x] create users with roles in database
- [x] integrate angular frontend application with django backend framework
- [ ] bind roles to html on redirect page after successful login 
- [x] create pipeline to build frontend and deploy to cloud
- [ ] load in database credentials for local deployments through VCAP_SERVICES environment variable to mimic cloud deployments

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
- [Python Library, cg-django-uaa: Documentation](https://cg-django-uaa.readthedocs.io/en/latest/quickstart.html)<br/>
### Relevant Stack Discussions
- [Django Add Auth Groups Programmatically](https://stackoverflow.com/questions/25024795/django-1-7-where-to-put-the-code-to-add-groups-programmatically/25803284#25803284)<br>
- [Creating JSON HttpResponse In Django](https://stackoverflow.com/questions/2428092/creating-a-json-response-using-django-and-python)