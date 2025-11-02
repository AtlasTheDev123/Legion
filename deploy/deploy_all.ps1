# validate functions.json and create a zip of the repo
Write-Host "Validating JSONs..."
try {
  $s = Get-Content -Path .\schemas\functions.json -Raw | ConvertFrom-Json
  Write-Host "functions.json validated (entries: $($s.Count))"
} catch {
  Write-Host "Validation failed: $_"; exit 1
}
$zip = "nexus_legion_x_omega_package.zip"
if (Test-Path $zip) { Remove-Item $zip }
Write-Host "Compressing repository into $zip (this may include local files)"
Compress-Archive -Path * -DestinationPath $zip -Force
Write-Host "Created $zip"
