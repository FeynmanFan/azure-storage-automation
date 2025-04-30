$resourceGroupName = "cbb-storage"
$storageAccountName = "cbbbackups"
$containerName = "backups"  
$localFolder = "C:\Backups" 

$context = Get-AzContext
if (-not $context) {
    Connect-AzAccount -ErrorAction Stop
} else {
    Write-Host "Already connected to Azure as $($context.Account.Id)"
}

$storageAccount = Get-AzStorageAccount -ResourceGroupName $resourceGroupName -Name $storageAccountName -ErrorAction Stop
if (-not $storageAccount) {
    throw "Storage account '$storageAccountName' not found in resource group '$resourceGroupName'."
}

$storageContext = $storageAccount.Context

$blobs = Get-AzStorageBlob -Container $containerName -Context $storageContext -ErrorAction Stop | 
            Sort-Object -Property LastModified -Descending
if (-not $blobs) {
    throw "No blobs found in container '$containerName'."
}

$latestBlob = $blobs[0]
$blobName = $latestBlob.Name
$lastModified = $latestBlob.LastModified
Write-Host "Latest blob: '$blobName' (Last Modified: $lastModified)"

if (-not (Test-Path -Path $localFolder)) {
    Write-Host "Creating local folder '$localFolder'..."
    New-Item -Path $localFolder -ItemType Directory -ErrorAction Stop | Out-Null
}

$destinationPath = Join-Path -Path $localFolder -ChildPath $blobName
Write-Host "Downloading blob '$blobName' to '$destinationPath'..."
Get-AzStorageBlobContent -Container $containerName -Blob $blobName -Context $storageContext -Destination $destinationPath -Force -ErrorAction Stop

Write-Host "Download completed successfully! File saved to '$destinationPath'."
