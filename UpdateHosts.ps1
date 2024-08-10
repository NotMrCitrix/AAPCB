$hostsPath = "C:\Windows\System32\drivers\etc\hosts"
$configPath = "C:\Users\citrix\Documents\hosts\config.txt"

# Read the config file
$config = Get-Content -Path $configPath | ConvertFrom-StringData
$interval = $config.interval * 60  # Convert minutes to seconds
$url = $config.url

$previousContent = ""

while ($true) {
    try {
        $ping = Test-Connection -ComputerName google.com -Count 1 -ErrorAction SilentlyContinue

        if ($ping) {
            $newContent = Invoke-WebRequest -Uri $url -UseBasicParsing | Select-Object -ExpandProperty Content

            if ($newContent -ne $previousContent) {
                Copy-Item -Path $hostsPath -Destination "${hostsPath}.bak" -Force
                Set-Content -Path $hostsPath -Value $newContent -Force
                $previousContent = $newContent
            }
        }

        # Wait for the interval specified in the config file
        Start-Sleep -Seconds $interval
    } catch {
        Write-Output "An error occurred: $_"
    }
}
