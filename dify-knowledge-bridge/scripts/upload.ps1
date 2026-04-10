[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# Dify Upload Script
$filePath = "C:\SL\中设智控\公司本部\会议纪要\纪要_02-26 内部会议_ 2026经营策略与AI赋能.md"
$datasetId = "9c3e5075-386d-49cf-a500-b92705eccdf7"
$apiKey = "dataset-GeVY5VrH2Uu0cgr931oLHaze"
$endpoint = "http://160.0.6.9/v1"

Write-Host "==============================================="
Write-Host "Dify Knowledge Base Upload Tool"
Write-Host "==============================================="
Write-Host "File: $filePath"
Write-Host "Dataset ID: $datasetId"
Write-Host ""

if (-Not (Test-Path $filePath)) {
    Write-Host "[ERROR] File not found: $filePath"
    exit 1
}

$fileInfo = Get-Item $filePath
Write-Host "[INFO] File size: $($fileInfo.Length) bytes"
Write-Host "[INFO] File name: $($fileInfo.Name)"
Write-Host ""

Write-Host "[UPLOAD] Starting upload..."
$uploadUrl = "$endpoint/datasets/$datasetId/documents/upload"

try {
    $headers = @{
        "Authorization" = "Bearer $apiKey"
    }
    
    $response = Invoke-RestMethod -Uri $uploadUrl -Method Post -Headers $headers -ContentType "multipart/form-data" -InFile $filePath
    
    Write-Host ""
    Write-Host "[SUCCESS] Upload completed!"
    Write-Host "==============================================="
    
    $response | ConvertTo-Json -Depth 10
    
    Write-Host ""
    Write-Host "[INFO] Document added to knowledge base!"
    
} catch {
    Write-Host ""
    Write-Host "[ERROR] Upload failed!"
    Write-Host "Message: $($_.Exception.Message)"
}
