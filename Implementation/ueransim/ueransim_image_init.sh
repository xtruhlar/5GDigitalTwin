#!/bin/bash

if [[ -z "$COMPONENT_NAME" ]]; then
	echo "Error: COMPONENT_NAME environment variable not set"; exit 1;
elif [[ "$COMPONENT_NAME" =~ ^(ueransim-gnb[[:digit:]]*$) ]]; then
	echo "Deploying component: '$COMPONENT_NAME'"
	/mnt/ueransim/${COMPONENT_NAME}_init.sh && \
	./nr-gnb -c ../config/${COMPONENT_NAME}.yaml | tee /mnt/ueransim/gnb.log & \
	bash
elif [[ "$COMPONENT_NAME" =~ ^(ueransim-ue[[:digit:]]*$) ]]; then
	echo "Deploying component: '$COMPONENT_NAME'"
	/mnt/ueransim/init_scripts/${COMPONENT_NAME}_init.sh && \
	./nr-ue -c ../config/${COMPONENT_NAME}.yaml | tee /mnt/ueransim/ue.log & \
	bash
else
	echo "Error: Invalid component name: '$COMPONENT_NAME'"
fi

# BSD 2-Clause License | Copyright © 2020 Supreeth Herle | All rights reserved.