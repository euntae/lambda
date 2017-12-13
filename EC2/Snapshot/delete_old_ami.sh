#!/bin/bash

REGIONS="ap-northeast-2" #복수 리전 사용 시 공백으로 구분
OWNERID=$(aws sts get-caller-identity --query Account --output text)
FILTER="Name=name,Values=*csy*" #Image 조회 시 --filter에 사용될 내용
DELETEDATE=$(date +%Y%m%d) #--date="1week ago") #삭제 기준 날짜 설정

for REGION in $REGIONS; do
  aws ec2 describe-images --region $REGION --owners $OWNERID --filter $FILTER --query 'Images[*].[CreationDate,ImageId]' --output text > ami_list

  while read CREATIONDATE IMAGEID; do
    CONVERTTIME=$(date -d $CREATIONDATE +%Y%m%d)
    SNAPSHOTS=$(aws ec2 describe-images --region $REGION --image-id $IMAGEID --query 'Images[*].BlockDeviceMappings[*].[Ebs.SnapshotId]' --output text) #AMI 삭제 시 스냅샷도 삭제하기 위해 사용
    if [ "$CONVERTTIME" -gt "$DELETEDATE" ] #AMI 생성 일자와 삭제 기준 날짜를 비교하여 생성 일이 더 최신인 경우 패스
    then
      echo "$IMAGEID will not remove"
      continue
    else
      aws ec2 deregister-image --image-id $IMAGEID #AMI 삭제

      until [ -z $(aws ec2 describe-images --region $REGION --image-id $IMAGEID --query 'Images[*].[ImageId]' --output text) ]
      do
        sleep 10
      done

      for SNAPSHOT in $SNAPSHOTS; do
        aws ec2 delete-snapshot --snapshot-id $SNAPSHOT
      done
    fi
  done < ami_list
done