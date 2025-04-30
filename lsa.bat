echo off
echo Storage Accounts
az storage account list --query "[].{Name:name, ResourceGroup:resourceGroup, Location:location}"