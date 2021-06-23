#!/bin/bash

git reset --hard
git pull

gcloud app create --region us-central
gcloud app deploy -q

PROJECT=$(gcloud config get-value project)
echo "Visit https://${PROJECT}.appspot.com"
