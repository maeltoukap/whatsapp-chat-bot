GOOGLE_PROJECT_ID=whatsapp-chat-bot-377200
CLOUD_RUN_SERVICE=chat-bot-responder
REGION=southamerica-west1


gcloud builds submit --tag gcr.io/$GOOGLE_PROJECT_ID/$CLOUD_RUN_SERVICE \
    --project $GOOGLE_PROJECT_ID


# gcloud run deploy $CLOUD_RUN_SERVICE \
#   --image gcr.io/$GOOGLE_PROJECT_ID/$CLOUD_RUN_SERVICE \
#   --platform managed \
#   --region $REGION \
#   --allow-unauthenticated \
#   --project=$GOOGLE_PROJECT_ID