# write to registry
New-ItemProperty -Path "HKCU:Software\Microsoft\Office\Common" -Name {{Ready}} -Value '{{PAYLOAD}}'  -PropertyType "String"