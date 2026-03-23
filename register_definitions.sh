#!/bin/bash

CONDUCTOR_URL="http://localhost:8080/api"

echo "Registering task definitions"

curl -X POST $CONDUCTOR_URL/metadata/taskdefs \
-H "content-Type: application/json" \
-d @workflows/tasks.json

echo ""
echo "task definitions registered"

echo "Registering workflow definitions"

curl -X POST $CONDUCTOR_URL/metadata/workflow \
-H "content-Type: application/json" \
-d @workflows/service_workflow.json

echo ""
echo "workflow definitions registered"
