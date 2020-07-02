FROM debian

WORKDIR /home/

# Install dependencies
RUN apt-get update -y && apt-get install -y curl 

# Install CloudFoundry Command Line Interface
RUN curl -L "https://packages.cloudfoundry.org/stable?release=linux64-binary&source=github" | tar -zx
RUN mv cf /usr/local/bin

# Install Node
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash - \
    && apt-get install -y nodejs