#!/bin/bash

gcloud app create --region us-central
gcloud app deploy

PROJECT=$(gcloud config get-value project)
echo "Visit https://${PROJECT}.appspot.com"
