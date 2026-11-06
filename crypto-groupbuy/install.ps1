param([switch]$BuildNative)
$ErrorActionPreference='Stop'
$projectRoot=Split-Path -Parent $PSScriptRoot
$runtime=Join-Path $projectRoot '.tools/fhe-runtime'
New-Item -ItemType Directory -Force $runtime | Out-Null
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'package.json') -Destination (Join-Path $runtime 'package.json')
Copy-Item -LiteralPath (Join-Path $PSScriptRoot 'package-lock.json') -Destination (Join-Path $runtime 'package-lock.json')
& npm.cmd ci --prefix $runtime --ignore-scripts --no-audit --no-fund
if($LASTEXITCODE -ne 0){throw 'Node dependency installation failed'}
& python -m pip install 'cryptography==49.0.0'
if($LASTEXITCODE -ne 0){throw 'Python dependency installation failed'}
if($BuildNative){
 $source=Join-Path $projectRoot '.tools/co-snarks'
 $pin=(Get-Content (Join-Path $PSScriptRoot 'upstream.json') -Raw|ConvertFrom-Json).commit
 if(!(Test-Path -LiteralPath $source)){
  & git clone --filter=blob:none --no-checkout https://github.com/TaceoLabs/co-snarks.git $source
  if($LASTEXITCODE -ne 0){throw 'Clone failed'}
  & git -C $source checkout $pin
  if($LASTEXITCODE -ne 0){throw 'Pinned checkout failed'}
 }
 & (Join-Path $PSScriptRoot 'build-native.ps1')
}
