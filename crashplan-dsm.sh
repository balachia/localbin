#!/bin/sh

echo "Cloning DSM configuration"
cp /Library/Application\ Support/CrashPlan/.ui_info.dsm /Library/Application\ Support/CrashPlan/.ui_info

echo "Opening tunnel"
#ssh -N -L 4200:localhost:4243 root@Diskstation.local
#ssh -N -L 4200:localhost:4243 root@dsm
ssh -N -L 4200:diskstation.local:4243 home

echo "Restoring local configuration"
cp /Library/Application\ Support/CrashPlan/.ui_info.local /Library/Application\ Support/CrashPlan/.ui_info

