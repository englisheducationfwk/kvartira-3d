$ws = New-Object -ComObject WScript.Shell
$desk = [Environment]::GetFolderPath('Desktop')
$cyr = [char]0x41A + [char]0x423 + [char]0X425 + [char]0x41D + [char]0x42F
$root = 'C:\Users\Admin\Desktop\school\wall-master'
$lnk = $ws.CreateShortcut((Join-Path $desk 'KUHNYA 3D.lnk'))
$lnk.TargetPath = (Join-Path $root 'kuhnya.bat')
$lnk.WorkingDirectory = $root
$lnk.IconLocation = (Join-Path $root 'kuhnya.ico')
$lnk.Description = 'Kuhnya 3D - remont i pokraska (game window)'
$lnk.Save()
Write-Output ('target=[' + $lnk.TargetPath + ']')
