# <b>SIN Web App: A Work In Progress</b>

This is a sample application that integrates an Angular frontend with a Django WSGI application deployed onto a <i>gunicorn</i> web server. It uses a <b>cloud.gov</b> OAuth2 client and a pre-configured python library specifically for that client, <i>cg-django-uaa</i>, to authenticate users, in addition to regular authentication Django backend plugins. The application has been containerized through a <i>Dockerfile</i> that creates an image of the application.

Note the <i>manifest.yml</i> for CloudFoundry names this app <b>ccda</b>, so when it is pushed to the cloud, it will live at [https://ccda.app.cloud.gov](https://ccda.app.cloud.gov). Edit the application name accordingly, if you need another domain route. 

The application is built from source on the cloud, not the Docker image. The Docker image is soley for ease of local development. 

## Table of Contents

- [Setup](docs/SETUP.md)
- [Development](docs/DEVELOPMENT.md)
- [Frontend](docs/FRONTEND.md)
- [S3](docs/S3.md)
- [API](docs/API.md)
- [Appendix](docs/APPENDIX.md)
