#!/bin/bash

if [ -z "$NODE_ENV" ]
then
  NODE_ENV="default"
  export $NODE_ENV
fi

GIT_HASH=`git log --format="%H" --max-count=1 less/*`;
GIT_HASH=z$GIT_HASH;
export $GIT_HASH;

rm public/css/client.css;
forever stop client-app.js; rm ~/.forever/dome-client.js.log; forever start -l dome-client.js.log client-app.js $GIT_HASH;
