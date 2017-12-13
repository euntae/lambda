#!/bin/bash

REGIONS="ap-northeast-2"
OWNERID=$(aws sts get-caller-identity --query Account --output text)
DELETEDATE=$(date +%Y%m%d --date="1week ago")

for REGION in $REGIONS; do
        aws ec2 describe-snapshots --region $REGION --owner-id $OWNERID --query 'Snapshots[*].[StartTime,SnapshotId]' --output text > snapshot-list

        while read STARTTIME SNAPSHOTID; do
                CONVERTTIME=$(date -d $STARTTIME +%Y%m%d)
                if [ "$CONVERTTIME" -gt "$DELETEDATE" ]; then continue;
                else
                        #명령줄 입력
                        aws ec2 delete-snapshot --snapshot-id $SNAPSHOTID
                fi
        done < snapshot-list
done