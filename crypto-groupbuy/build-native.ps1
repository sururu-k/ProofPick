$ErrorActionPreference='Stop'
$root=Split-Path -Parent $PSScriptRoot
$vswhere=Join-Path ${env:ProgramFiles(x86)} 'Microsoft Visual Studio/Installer/vswhere.exe'
$installation=& $vswhere -latest -products '*' -requires Microsoft.VisualStudio.Component.VC.Tools.x86.x64 -property installationPath
if(!$installation){throw 'C++ Build Tools required'}
Import-Module (Join-Path $installation 'Common7/Tools/Microsoft.VisualStudio.DevShell.dll')
Enter-VsDevShell -VsInstallPath $installation -SkipAutomaticLocation -DevCmdArguments '-arch=x64 -host_arch=x64'
$source=Join-Path $root '.tools/co-snarks'
$pin=(Get-Content (Join-Path $PSScriptRoot 'upstream.json') -Raw|ConvertFrom-Json).commit
if((& git -C $source rev-parse HEAD) -ne $pin){throw 'Upstream revision mismatch'}
Push-Location $source
try {
 & cargo build --release --locked --bin co-circom -j 2
 if($LASTEXITCODE -ne 0){throw 'co-circom build failed'}
} finally {Pop-Location}
