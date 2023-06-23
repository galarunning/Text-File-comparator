#Parameter Input Values
$SERVER = Get-Content IP_GSS_Win.txt
$username = "gpsadmin"
$password = ConvertTo-SecureString "admin" -AsPlainText -Force

#Power Options
$IP_Power_username = "admin"
$IP_Power_password = "12345678"
$IP_Power_IP = Get-Content IP_Power.txt

$Power_Option_1 = "p61"
$Power_Option_2 = "p62"
$Power_Option_3 = "p63"
$Power_Option_4 = "p64"

$Power_Off = "0"
$Power_On = "1"

#Script Directory Path
$scriptpath = $MyInvocation.MyCommand.Path
$dir = Split-Path $scriptpath
Write-host "My directory is $dir"

#Run the Powershell as admin (without closing it)
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Bypass

#Shutdown Command
#Set-ItemProperty 'HKLM:\SOFTWARE\Microsoft\PowerShell\1\ShellIds' ConsolePrompting $true
Invoke-Command -Computer $SERVER -Credential ($psCred = New-Object System.Management.Automation.PSCredential -ArgumentList ($username, $password)) { shutdown /s /f }
Write-Host "$SERVER - Shutdown Complete"

#Wait for 1 minute until IP power switch off
Write-Host "$IP_Power_IP - IP Power Switch Powering off in 2 Minute"
Start-Sleep -s 120


#IP Power switch off command
$url = "http://${IP_Power_username}:${IP_Power_password}@$IP_Power_IP/Set.cmd?CMD=SetPower+$Power_Option_3=$Power_off"
cmd /c "curl $url"

#Wait for 1 minute until IP power switch off
Write-Host "$IP_Power_IP - IP Power Switch Powered off complete"
Write-Host "Waiting 1 min before powering back ON"
Start-Sleep -s 60

#IP Power switch On command
$url = "http://${IP_Power_username}:${IP_Power_password}@$IP_Power_IP/Set.cmd?CMD=SetPower+$Power_Option_3=$Power_On"
cmd /c "curl $url"
Write-Host "$IP_Power_IP - IP Power Switch Powered On complete"

#Wait until RDP is back online
Write-Host "Waiting 30 seconds until RDP is not back onlin and trying connecting continuously"
Start-Sleep -s 30

Do {Start-Sleep -s 15}
Until ((Test-NetConnection -ComputerName $SERVER -Port 3389).TcpTestSucceeded -eq $true)
Write-Host "Powercycle Script is complete"

############# Total time script Duration 04Minute 30 Seconds ##############

Write-Host "Waiting 60 seconds for Windows to boot up" 

# Sleeping for 60 seconds to wait for Widnows
Start-Sleep -s 60
Write-Host "Wait period complete."

Exit
