Push-Location -Path src

$env:GOOS="windows"; $env:GOARCH="amd64"; go build -o ../ua3f-0.7.3-windows-amd64.exe -trimpath -ldflags="-s -w" main.go

Pop-Location